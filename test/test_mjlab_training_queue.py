"""DESKTOP_DRY_RUN: real process handoff and saved-learning-curve comparisons."""

from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from queue_mjlab_flash_sac import process_identity, verified_checkpoint


def load_analysis():
    spec = importlib.util.spec_from_file_location("mjlab_training_comparison", REPO / "test/analyze_mjlab_isaac_training.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def checkpoint(path, steps=2):
    path.mkdir(parents=True)
    (path / "actor.pt").write_bytes(b"queue-test-actor")
    digest = hashlib.sha256((path / "actor.pt").read_bytes()).hexdigest()
    (path / "ddt.json").write_text(json.dumps({"step": steps, "actor_sha256": digest, "actor_obs_dim": 35,
                                             "critic_obs_dim": 39, "agent": {"seed": 42}}))
    return digest


class TrainingQueueTest(unittest.TestCase):
    def test_process_identity_and_corrupt_checkpoint(self):
        self.assertEqual(process_identity(999999999), None)
        self.assertEqual(process_identity(__import__("os").getpid())["pid"], __import__("os").getpid())
        with tempfile.TemporaryDirectory(dir=REPO / "test") as temp:
            path = Path(temp) / "model_2"
            expected = checkpoint(path)
            self.assertEqual(verified_checkpoint(path, 2), expected)
            with self.assertRaises(RuntimeError):
                verified_checkpoint(path, 3)
            (path / "actor.pt").write_bytes(b"tampered")
            with self.assertRaises(RuntimeError):
                verified_checkpoint(path, 2)

    def test_waits_for_parent_then_runs_flat_walk_and_comparison(self):
        with tempfile.TemporaryDirectory(dir=REPO / "test") as temp:
            root = Path(temp)
            evidence = root / "docs/exp" / datetime.now().strftime("%Y-%m-%d")
            evidence.mkdir(parents=True)
            predecessor = root / "old/model_2"
            checkpoint(predecessor)
            parent = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(1.2)"])
            identity = process_identity(parent.pid)
            jobs = []
            for task in ("flat", "walk"):
                target = root / task / "model_2"
                checkpoint(target)
                run_id = "tita_mjlab_test_" + task
                code = (
                    "import json,time; from pathlib import Path; "
                    f"e=Path({str(evidence)!r}); "
                    f"(e/{(run_id + '_args.json')!r}).write_text(json.dumps({{'run_name':{task!r}}})); "
                    f"(e/{(run_id + '_metrics.jsonl')!r}).write_text('{{\"step\":2}}\\n'); "
                    f"(e/{(run_id + '_result.json')!r}).write_text(json.dumps({{'checkpoint':{str(target)!r},'evidence_status':'PASS','wandb_url':None}})); "
                    f"(e/{(task + '_started')!r}).write_text(str(time.time()))"
                )
                jobs.append({"task": task, "run_name": task, "argv": [sys.executable, "-c", code]})
            plan = {"repo": str(root), "queue_id": "test_queue", "steps": 2,
                    "dependency": {"identity": identity, "checkpoint": str(predecessor)},
                    "jobs": jobs, "poll_seconds": .05, "state_path": str(evidence / "state.json"),
                    "lock_path": str(root / "queue.lock"), "manifest_path": str(evidence / "plan.json"),
                    "comparison_argv": [sys.executable, "-c", f"from pathlib import Path; Path({str(evidence / 'comparison_started')!r}).touch()"]}
            Path(plan["manifest_path"]).write_text(json.dumps(plan))
            queue = subprocess.Popen([sys.executable, str(REPO / "scripts/queue_mjlab_flash_sac.py"), "--manifest", plan["manifest_path"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            try:
                time.sleep(.25)
                self.assertIsNone(parent.poll())
                self.assertFalse((evidence / "flat_started").exists())
                self.assertEqual(json.loads(Path(plan["state_path"]).read_text())["status"], "waiting_for_isaac")
                parent.wait(timeout=5)
                output = queue.communicate(timeout=10)[0].decode()
                self.assertEqual(queue.returncode, 0, output)
                state = json.loads(Path(plan["state_path"]).read_text())
                self.assertEqual(state["status"], "completed")
                self.assertEqual([x["task"] for x in state["jobs"]], ["flat", "walk"])
                self.assertTrue(all(x["status"] == "completed" for x in state["jobs"]))
                self.assertLess(float((evidence / "flat_started").read_text()), float((evidence / "walk_started").read_text()))
                self.assertTrue((evidence / "comparison_started").is_file())
            finally:
                for process in (queue, parent):
                    if process.poll() is None:
                        process.kill()
                        process.wait()

    def test_comparison_uses_original_step_samples_and_checkpoint_hashes(self):
        analysis = load_analysis()
        with tempfile.TemporaryDirectory(dir=REPO / "test") as temp:
            root = Path(temp)
            manifest = {"queue_id": "test", "steps": 2, "references": {}}
            state = {"jobs": []}
            for task in ("flat", "walk"):
                for engine in ("isaac", "mjlab"):
                    path = root / task / engine / "model_2"
                    checkpoint(path)
                    metrics = path.parent / "metrics.jsonl"
                    metrics.write_text('\n'.join(json.dumps({"step": s, **{key: float(s) for key in analysis.METRICS}}) for s in (1, 2)))
                    source = {"task": task, "status": "completed", "checkpoint": str(path), "metrics": str(metrics)}
                    if engine == "isaac":
                        manifest["references"][task] = source
                    else:
                        state["jobs"].append(source)
            result = analysis.compare(manifest, state, root / "plots")
            self.assertEqual(result["evidence_status"], "PASS")
            self.assertEqual(len(result["sources"]), 4)
            self.assertEqual(len(result["figures"]), 2)
            self.assertTrue(all(Path(path).read_bytes().startswith(b'\x89PNG') for path in result["figures"]))
            self.assertEqual(len(Path(result["csv"]).read_text().splitlines()), 9)
            for row in result["summary"]:
                self.assertEqual(row["episode_return_mean"], 1.5)
            state["jobs"][0]["status"] = "failed"
            with self.assertRaises(RuntimeError):
                analysis.compare(manifest, state, root / "bad_plots")
            metrics.write_text('{"step": 2}\n{"step": 1}\n')
            with self.assertRaises(ValueError):
                analysis.read_metrics(metrics)


if __name__ == "__main__":
    unittest.main()
