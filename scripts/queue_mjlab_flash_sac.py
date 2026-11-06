"""TRAINING_SIM: wait for identified predecessor runs, then run mjlab jobs.

The manifest contains complete argv lists. This process runs in detached tmux;
it never signals the predecessor and waits for video/W&B cleanup to finish.
"""

import argparse
from datetime import datetime
import fcntl
import hashlib
import json
from pathlib import Path
import subprocess
import time


def process_identity(pid):
    """Linux start ticks + boot ID distinguish a completed PID from PID reuse."""
    try:
        stat = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
        if stat[0] == "Z":
            return None
        return {"pid": pid, "start_ticks": stat[19],
                "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip()}
    except FileNotFoundError:
        return None


def verified_checkpoint(path, steps):
    path = Path(path)
    meta = json.loads((path / "ddt.json").read_text())
    digest = hashlib.sha256((path / "actor.pt").read_bytes()).hexdigest()
    if meta["step"] != steps or meta["actor_sha256"] != digest:
        raise RuntimeError(f"Incomplete or corrupt checkpoint: {path}")
    return digest


def save_state(path, state):
    state["updated_at"] = datetime.now().astimezone().isoformat()
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2) + "\n")
    temporary.replace(path)


def find_result(repo, run_name):
    matches = []
    for path in (repo / "docs/exp").glob("*/tita_mjlab_*_args.json"):
        if json.loads(path.read_text()).get("run_name") == run_name:
            matches.append(path)
    if len(matches) != 1:
        raise RuntimeError(f"Expected one training record for {run_name}, found {len(matches)}")
    args_file = matches[0]
    run_id = args_file.name.removesuffix("_args.json")
    result_file = args_file.with_name(run_id + "_result.json")
    result = json.loads(result_file.read_text())
    return result_file, args_file.with_name(run_id + "_metrics.jsonl"), result


def run_queue(manifest, state_path):
    repo = Path(manifest["repo"])
    if manifest.get("once") and state_path.exists():
        previous = json.loads(state_path.read_text())
        if previous.get("queue_id") == manifest["queue_id"] and any(
                job["status"] != "pending" for job in previous.get("jobs", [])):
            print("[TRAINING_SIM] Queue has already started; duplicate execution skipped.", flush=True)
            return
    multiple = "dependencies" in manifest
    dependencies = manifest["dependencies"] if multiple else [manifest["dependency"]]
    if not dependencies:
        raise ValueError("At least one predecessor is required")
    state = {"execution_domain": "TRAINING_SIM", "evidence_status": "NOT_TESTED",
             "status": "waiting_for_dependencies" if multiple else "waiting_for_isaac", "queue_id": manifest["queue_id"],
             "jobs": [{"task": job["task"], "status": "pending"} for job in manifest["jobs"]]}
    state["dependencies" if multiple else "dependency"] = dependencies if multiple else dependencies[0]
    save_state(state_path, state)
    print(f"[TRAINING_SIM] Waiting for predecessor PIDs {[d['identity']['pid'] for d in dependencies]} to exit.", flush=True)
    while True:
        active = [d["identity"]["pid"] for d in dependencies
                  if process_identity(d["identity"]["pid"]) == d["identity"]]
        if not active:
            break
        state["waiting_pids"] = active
        save_state(state_path, state)
        time.sleep(manifest.get("poll_seconds", 20))
    # A crash or cancelled training must not be described as a finished 100k run.
    for dependency in dependencies:
        steps = dependency.get("steps", manifest["steps"])
        digest = verified_checkpoint(dependency["checkpoint"], steps)
        if dependency.get("result_json"):
            result = json.loads(Path(dependency["result_json"]).read_text())
            if (result.get("evidence_status") not in ("PASS", "SUSPICIOUS")
                    or result.get("step") != steps or result.get("checkpoint_sha256") != digest
                    or Path(result.get("checkpoint", "")).resolve() != Path(dependency["checkpoint"]).resolve()):
                raise RuntimeError(f"Predecessor did not finish successfully: {dependency['result_json']}")
        dependency["checkpoint_sha256"] = digest
    state["waiting_pids"] = []
    print("[TRAINING_SIM] All predecessor checkpoints verified; processes have exited.", flush=True)
    for job, entry in zip(manifest["jobs"], state["jobs"]):
        state["status"] = f"running_{job['task']}"
        evidence = repo / "docs/exp" / datetime.now().strftime("%Y-%m-%d")
        evidence.mkdir(parents=True, exist_ok=True)
        console = evidence / f"{manifest['queue_id']}_{job['task']}_console.log"
        entry.update(status="running", started_at=datetime.now().astimezone().isoformat(), console=str(console), argv=job["argv"])
        save_state(state_path, state)
        try:
            with console.open("w") as stream:
                process = subprocess.Popen(job["argv"], cwd=repo, stdout=stream, stderr=subprocess.STDOUT)
                entry["pid"] = process.pid
                save_state(state_path, state)
                return_code = process.wait()
            entry["return_code"] = return_code
            if return_code:
                raise RuntimeError(f"Training exited {return_code}; see {console}")
            result_path, metrics, result = find_result(repo, job["run_name"])
            digest = verified_checkpoint(result["checkpoint"], manifest["steps"])
            if result["evidence_status"] not in ("PASS", "SUSPICIOUS"):
                raise RuntimeError(f"Training result is {result['evidence_status']}")
            entry.update(status="completed", evidence_status=result["evidence_status"],
                         checkpoint=result["checkpoint"], checkpoint_sha256=digest,
                         metrics=str(metrics), result_json=str(result_path), wandb_url=result["wandb_url"])
        except Exception as error:
            entry.update(status="failed", evidence_status="FAIL", detail=f"{type(error).__name__}: {error}")
        entry["finished_at"] = datetime.now().astimezone().isoformat()
        save_state(state_path, state)
        print(f"[TRAINING_SIM] {job['task']}: {entry['status']}", flush=True)
    state["comparison_return_code"] = 0
    if manifest.get("comparison_argv"):
        state["status"] = "making_comparison"
        save_state(state_path, state)
        command = manifest["comparison_argv"] + ["--manifest", manifest["manifest_path"], "--state", str(state_path)]
        state["comparison_return_code"] = subprocess.run(command, cwd=repo, check=False).returncode
        reports = list((repo / "docs/exp").glob(f"*/{manifest['queue_id']}_comparison.json"))
        if reports:
            report = max(reports, key=lambda path: path.stat().st_mtime)
            state["comparison_result"] = str(report)
            state["comparison"] = json.loads(report.read_text())
    complete = all(job["status"] == "completed" and job["evidence_status"] == "PASS" for job in state["jobs"])
    state["status"] = "completed" if complete and state["comparison_return_code"] == 0 else "finished_with_errors"
    state["evidence_status"] = "PASS" if state["status"] == "completed" else "SUSPICIOUS"
    save_state(state_path, state)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    state_path = Path(manifest["state_path"])
    lock_path = Path(manifest["lock_path"])
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            run_queue(manifest, state_path)
        except BaseException as error:
            state = json.loads(state_path.read_text()) if state_path.exists() else {}
            state.update(execution_domain="TRAINING_SIM", status="failed", evidence_status="FAIL", detail=f"{type(error).__name__}: {error}")
            save_state(state_path, state)
            raise


if __name__ == "__main__":
    main()
