"""VALIDATION_SIM: compare saved Isaac/mjlab learning curves after queued runs."""

import argparse
import csv
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from queue_mjlab_flash_sac import verified_checkpoint

METRICS = {
    "episode_return_mean": "Episode return (reward dependent)",
    "episode_length_mean": "Episode length [control steps]",
    "env/Metrics/base_velocity/error_vel_xy": "Linear tracking error (logged)",
    "env/Metrics/base_velocity/error_vel_yaw": "Yaw tracking error (logged)",
    "reward_mean": "Mean reward / control step",
    "transitions_per_second": "Transitions / s (shared host)",
}


def read_metrics(path):
    rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
    if not rows or any(a["step"] >= b["step"] for a, b in zip(rows, rows[1:])):
        raise ValueError(f"Missing or non-monotonic learning metrics: {path}")
    return rows


def series(rows, key):
    points = [(r["step"], float(r[key])) for r in rows if key in r and math.isfinite(float(r[key]))]
    return np.asarray(points, dtype=float).reshape(-1, 2)


def smooth(values, window=20):
    total = np.concatenate(([0.], np.cumsum(values)))
    end = np.arange(1, len(values) + 1)
    start = np.maximum(0, end - window)
    return (total[end] - total[start]) / (end - start)


def compare(manifest, state, output):
    output.mkdir(parents=True, exist_ok=True)
    evidence = {"execution_domain": "VALIDATION_SIM", "evidence_status": "PASS", "sources": [], "figures": [], "summary": []}
    csv_rows = []
    for task in ("flat", "walk"):
        reference = manifest["references"][task]
        queued = next(job for job in state["jobs"] if job["task"] == task)
        if queued["status"] != "completed":
            raise RuntimeError(f"Cannot claim a completed comparison: {task} is {queued['status']}")
        sources = (("Isaac Lab", reference), ("mjlab", queued))
        figure, axes = plt.subplots(3, 2, figsize=(13, 11), constrained_layout=True)
        for engine, source in sources:
            checkpoint = Path(source["checkpoint"])
            digest = verified_checkpoint(checkpoint, manifest["steps"])
            rows = read_metrics(source["metrics"])
            if rows[-1]["step"] != manifest["steps"]:
                raise ValueError(f"{task}/{engine} did not reach {manifest['steps']} vector steps")
            meta = json.loads((checkpoint / "ddt.json").read_text())
            evidence["sources"].append({"task": task, "engine": engine, "checkpoint": str(checkpoint),
                "checkpoint_sha256": digest, "metrics": source["metrics"],
                "metrics_sha256": hashlib.sha256(Path(source["metrics"]).read_bytes()).hexdigest(),
                "actor_obs_dim": meta.get("actor_obs_dim"), "critic_obs_dim": meta.get("critic_obs_dim"),
                "seed": meta.get("agent", {}).get("seed")})
            summary = {"task": task, "engine": engine, "step": rows[-1]["step"]}
            color = "#2563eb" if engine == "Isaac Lab" else "#ea580c"
            for axis, (key, title) in zip(axes.flat, METRICS.items()):
                points = series(rows, key)
                if len(points):
                    x, y = points.T
                    axis.plot(x, y, color=color, alpha=.16, linewidth=.7)
                    axis.plot(x, smooth(y), color=color, linewidth=1.8, label=engine)
                    summary[key] = float(np.mean(y[-20:]))
                else:
                    axis.plot([], [], color=color, label=engine + " (not logged)")
                    summary[key] = None
                axis.set(title=title, xlabel="Vector control steps", xlim=(0, manifest["steps"]))
                axis.grid(alpha=.2)
                axis.legend(fontsize=8)
            evidence["summary"].append(summary)
            for row in rows:
                csv_rows.append({"task": task, "engine": engine, "step": row["step"], **{key: row.get(key) for key in METRICS}})
        figure.suptitle(f"TITA {task}: FlashSAC — Isaac Lab vs mjlab\nRaw curves + trailing 20 log samples; one seed, different contact physics", fontsize=13)
        destination = output / f"{manifest['queue_id']}_{task}_comparison.png"
        figure.savefig(destination, dpi=160)
        plt.close(figure)
        evidence["figures"].append(str(destination))
    csv_path = output / f"{manifest['queue_id']}_comparison_metrics.csv"
    with csv_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["task", "engine", "step", *METRICS])
        writer.writeheader()
        writer.writerows(csv_rows)
    evidence["csv"] = str(csv_path)
    return evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--wandb", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    state = json.loads(args.state.read_text())
    output = Path(manifest["repo"]) / "docs/exp" / datetime.now().strftime("%Y-%m-%d")
    output.mkdir(parents=True, exist_ok=True)
    result_path = output / f"{manifest['queue_id']}_comparison.json"
    try:
        evidence = compare(manifest, state, output)
        if args.wandb:
            import wandb
            with wandb.init(project=manifest["wandb_project"], name=manifest["queue_id"] + "_comparison",
                            job_type="comparison", mode="online", dir=str(output), config={"sources": evidence["sources"]}) as run:
                run.log({f"comparison/{task}": wandb.Image(path) for task, path in zip(("flat", "walk"), evidence["figures"])})
                columns = ["task", "engine", "step", *METRICS]
                run.log({"comparison/final_20_log_samples": wandb.Table(columns=columns, data=[[r.get(k) for k in columns] for r in evidence["summary"]])})
                evidence["wandb_url"] = run.url
                run.summary["evidence_status"] = evidence["evidence_status"]
    except Exception as error:
        evidence = locals().get("evidence", {"execution_domain": "VALIDATION_SIM", "sources": []})
        evidence.update(evidence_status="FAIL", detail=f"{type(error).__name__}: {error}")
    result_path.write_text(json.dumps(evidence, indent=2, allow_nan=False) + "\n")
    report = output / f"{manifest['queue_id']}_comparison.md"
    lines = ["# mjlab / Isaac Lab FlashSAC comparison", "", "Execution Domain: VALIDATION_SIM", "",
             f"Evidence Status: {evidence['evidence_status']}", "", "Policy Checkpoint SHA256:"]
    for source in evidence["sources"]:
        lines.append(f"- {source['task']} / {source['engine']}: `{source['checkpoint_sha256']}`")
    if not evidence["sources"]:
        lines.append("N/A (comparison failed before loading checkpoints)")
    lines += ["", "Observed metrics / behavior / log summary:", "",
              "Learning curves use each engine's own training environment. This is a one-seed comparison, not a controlled claim that one simulator is better.",
              "Reward totals depend on episode length and reward design. Contact friction/damping and some randomization differ; throughput includes shared-host load.",
              "Solid curves average the trailing 20 logged samples; faint curves show raw samples. The CSV preserves the unaligned original step samples.", ""]
    for path in evidence.get("figures", []):
        lines.append(f"![{Path(path).stem}]({Path(path).name})")
    for row in evidence.get("summary", []):
        lines.append(f"- {row['task']} / {row['engine']}, final 20 log samples: return={row.get('episode_return_mean')}, episode length={row.get('episode_length_mean')}, linear error={row.get('env/Metrics/base_velocity/error_vel_xy')}, yaw error={row.get('env/Metrics/base_velocity/error_vel_yaw')}")
    lines += ["", f"Full metrics and source hashes: `{result_path}`", f"W&B: {evidence.get('wandb_url', 'N/A')}", evidence.get("detail", "")]
    report.write_text("\n".join(lines) + "\n")
    print(f"[VALIDATION_SIM] {evidence['evidence_status']}: {report}", flush=True)
    return 0 if evidence["evidence_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
