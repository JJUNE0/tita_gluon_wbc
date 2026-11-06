"""TRAINING_SIM / VALIDATION_SIM: render saved policies outside the learner.

Only subprocess orchestration runs on the background thread. W&B calls stay
on the training thread. Videos use their checkpoint step as a separate axis,
so delayed rendering cannot send training history backwards.
"""

from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys

from runtime import REPO_ROOT


class CheckpointVideoLogger:
    def __init__(self, run, wandb, directory, device, length, player_script=None):
        self.run, self.wandb = run, wandb
        self.directory = Path(directory).resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.device, self.length = device, length
        self.player_script = Path(player_script) if player_script else Path(__file__).with_name("play.py")
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="checkpoint-video")
        self.jobs = []
        self.closed = False
        self.failures = 0
        run.define_metric("video/checkpoint_step")
        run.define_metric("video/*", step_metric="video/checkpoint_step")

    def submit(self, checkpoint, metadata):
        step = metadata["step"]
        job = {
            "execution_domain": "VALIDATION_SIM", "step": step,
            "checkpoint": str(Path(checkpoint).resolve()),
            "checkpoint_sha256": metadata["actor_sha256"],
            "video": str(self.directory / f"model_{step}.mp4"),
            "result": str(self.directory / f"model_{step}_render.json"),
            "log": str(self.directory / f"model_{step}_render.log"),
            "upload_record": str(self.directory / f"model_{step}_wandb.json"),
        }
        self.jobs.append((self.executor.submit(self._render, job), job))
        print(f"[VALIDATION_SIM] Queued checkpoint video: step={step}", flush=True)

    def _render(self, job):
        command = [
            sys.executable, str(self.player_script),
            "--checkpoint", job["checkpoint"], "--num_envs", "1",
            "--steps", str(self.length), "--device", self.device, "--headless",
            "--video", job["video"], "--video_result", job["result"],
        ]
        with Path(job["log"]).open("w") as stream:
            subprocess.run(command, cwd=REPO_ROOT, stdout=stream, stderr=subprocess.STDOUT,
                           check=True, timeout=300)
        result = json.loads(Path(job["result"]).read_text())
        if (result["evidence_status"] != "PASS" or result["frames"] != self.length
                or result["checkpoint_sha256"] != job["checkpoint_sha256"]
                or not Path(job["video"]).is_file() or Path(job["video"]).stat().st_size == 0):
            raise RuntimeError("Video/result is incomplete or checkpoint hash does not match")
        return result

    def poll(self):
        pending = []
        for future, job in self.jobs:
            if not future.done():
                pending.append((future, job))
                continue
            record = {**job, "wandb_run_id": self.run.id}
            try:
                result = future.result()
                self.run.log({
                    "video/checkpoint_step": job["step"],
                    "video/checkpoint_sha256": job["checkpoint_sha256"],
                    "video/rollout": self.wandb.Video(job["video"], format="mp4"),
                })
                record.update(evidence_status="PASS", frames=result["frames"],
                              detail="Video logged to W&B SDK; online sync follows run mode.")
                print(f"[VALIDATION_SIM] Video logged to W&B: step={job['step']}", flush=True)
            except Exception as error:
                self.failures += 1
                record.update(evidence_status="FAIL", detail=f"{type(error).__name__}: {error}")
                print(f"[VALIDATION_SIM] FAIL video step={job['step']}: {error}; log={job['log']}", flush=True)
            Path(job["upload_record"]).write_text(json.dumps(record, indent=2) + "\n")
        self.jobs = pending
        self.run.summary["video/failures"] = self.failures

    def close(self):
        if not self.closed:
            self.closed = True
            # Complete the final clip before ExitStack finishes the W&B run.
            self.executor.shutdown(wait=True)
            self.poll()
