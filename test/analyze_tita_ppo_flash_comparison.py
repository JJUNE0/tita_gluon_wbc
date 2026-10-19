"""DESKTOP_DRY_RUN: summarize native comparisons and export learning curves."""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evaluation", type=Path, nargs="+", required=True)
    parser.add_argument("--ppo_metrics", type=Path, required=True)
    parser.add_argument("--sac_metrics", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    outputs = []
    for path in args.evaluation:
        raw = json.loads(path.read_text())
        assert raw["evidence_status"] == "PASS"
        policies = sorted({case["policy"] for case in raw["cases"]})
        aggregate, arrays = {}, {}
        for policy in policies:
            cases = sorted((c for c in raw["cases"] if c["policy"] == policy), key=lambda c: c["seed"])
            life = np.array([c["life_steps"] for c in cases])
            fell = np.array([c["fell"] for c in cases])
            sums = np.array([c["per_env_sums"] for c in cases])
            drift = np.array([c["final_drift_m"] for c in cases])
            assert len(cases) == len(raw["args"]["seeds"])
            assert all(c["initial_max_difference"] <= 1e-5 for c in cases)
            assert life.shape[1] % 4 == 0 and np.isfinite(sums).all()
            dt = cases[0]["horizon_s"] / raw["args"]["steps"]
            horizon = raw["args"]["steps"]
            reached = (life >= horizon) & ~fell
            arrays[policy] = (life * dt, sums[:, :, 1] / horizon)
            aggregate[policy] = {
                "trials": life.size, "reset_seeds": [c["seed"] for c in cases],
                "mean_survival_s": float(life.mean() * dt),
                "survival_at_horizon": float(reached.mean()),
                "tracking_integral_fixed_horizon": float(sums[:, :, 1].mean() / horizon),
                "time_weighted_conditional_metrics": dict(zip(cases[0]["fields"], (sums.sum((0, 1)) / life.sum()).tolist())),
                "groups": [],
            }
            width = life.shape[1] // 4
            for group, target in enumerate((0.0, 0.4, 0.8, -0.8)):
                sl = slice(group * width, (group + 1) * width)
                stable = drift[:, sl][reached[:, sl]]
                aggregate[policy]["groups"].append({
                    "target_vx": target,
                    "mean_survival_s": float(life[:, sl].mean() * dt),
                    "survival_at_horizon": float(reached[:, sl].mean()),
                    "tracking_integral_fixed_horizon": float(sums[:, sl, 1].mean() / horizon),
                    "time_weighted_conditional_metrics": dict(zip(cases[0]["fields"], (sums[:, sl].sum((0, 1)) / life[:, sl].sum()).tolist())),
                    "mean_final_drift_m_among_horizon_survivors": float(stable.mean()) if len(stable) else None,
                    "horizon_survivors": len(stable),
                })
        pairs = []
        if "ppo" in policies:
            pairs = [(name, "ppo") for name in policies if name != "ppo"]
        else:
            pairs = [(name, "ppo_2000") for name in policies if name.endswith("cap_1")]
            pairs += [(name, base) for name, base in (("flash_sac_45000", "ppo_1875"),
                                                     ("flash_sac_50000", "ppo_2000"),
                                                     ("flash_sac_70000", "ppo_2000"))
                      if name in policies and base in policies]
        rng = np.random.default_rng(42)
        indices = np.concatenate([rng.integers(g * width, (g + 1) * width, (10000, width)) for g in range(4)], axis=1)
        paired = []
        for other, base in pairs:
            entry = {"other": other, "reference": base}
            for number, metric in enumerate(("survival_s", "tracking_integral_fixed_horizon")):
                difference = (arrays[other][number] - arrays[base][number]).mean(0)
                draws = difference[indices].mean(1)
                entry[metric] = {"mean_difference": float(difference.mean()),
                                 "cluster_bootstrap_95_interval": np.quantile(draws, [.025, .975]).tolist()}
            paired.append(entry)
        outputs.append({"evaluation": str(path), "policy_checkpoint_sha256": raw["policy_checkpoint_sha256"],
                        "aggregate": aggregate, "paired": paired})

    summary = {
        "execution_domain": "DESKTOP_DRY_RUN", "evidence_status": "PASS",
        "policy_checkpoint_sha256": {entry["evaluation"]: entry["policy_checkpoint_sha256"] for entry in outputs},
        "evaluations": outputs,
        "limitations": ["One training seed, two matched reset seeds; intervals do not represent training-seed uncertainty.",
                        "Cluster bootstrap groups physical environment ID across reset seeds and stratifies by velocity command.",
                        "Cap probes intervene on a fixed policy; they do not predict learning with that cap.",
                        "Training return/episode logs have different collection windows and initial episode-length handling.",
                        "PPO loop and wall time include its suspension for the early evaluation; no wall-time benchmark is claimed."],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"execution_domain": "DESKTOP_DRY_RUN", "evidence_status": "PASS",
                      "summaries": [{"source": x["evaluation"], "aggregate": x["aggregate"], "paired": x["paired"]}
                                    for x in outputs]}, indent=2))

    ppo = [json.loads(line) for line in args.ppo_metrics.read_text().splitlines()]
    sac = [json.loads(line) for line in args.sac_metrics.read_text().splitlines()]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
    for data, xfield, label, color in ((ppo, "vector_steps", "PPO (33 inputs)", "#2474b5"),
                                      (sac, "step", "FlashSAC (33 inputs)", "#e07a24")):
        valid = [row for row in data if "episode_length_mean" in row and "episode_return_mean" in row]
        x = np.array([row[xfield] for row in valid])
        window = max(1, round(1000 / np.median(np.diff(x)))) if len(x) > 1 else 1
        for axis, field, factor in ((axes[0], "episode_length_mean", .02), (axes[1], "episode_return_mean", 1)):
            y = np.array([row[field] for row in valid]) * factor
            if len(y) >= window:
                smooth = np.convolve(y, np.ones(window) / window, mode="valid")
                axis.plot(x[window - 1:], smooth, label=label, color=color)
            axis.set_xlabel("Collected vector steps")
            axis.grid(alpha=.2)
    axes[0].set_ylabel("Logged mean episode duration (s)")
    axes[0].set_ylim(0, 21)
    axes[1].set_ylabel("Logged mean episode return")
    axes[0].legend()
    fig.suptitle("Training logs (1000-step smoothing; collection windows differ)")
    fig.savefig(args.output.with_name("tita_ppo_flash_learning_curves.png"), dpi=160)
    plt.close(fig)
    last = outputs[-1]["aggregate"]
    names = list(last)
    iterations = {p["policy"]: p["iterations_completed"] for p in raw.get("ppo_checkpoints", [])}
    if "ppo" not in iterations and "ppo_iterations_completed" in raw:
        iterations["ppo"] = raw["ppo_iterations_completed"]
    labels = []
    for name in names:
        if name.startswith("flash_sac_"):
            labels.append("FlashSAC\n" + name.removeprefix("flash_sac_") + " steps")
        elif name.endswith("_wheel_cap_1"):
            labels.append("PPO\nwheel cap ±1")
        elif name.endswith("_cap_1"):
            labels.append("PPO\nall cap ±1")
        else:
            labels.append(f"PPO\n{iterations.get(name, '')} iterations")
    colors = ["#e07a24" if name.startswith("flash") else "#8baecb" if "cap_1" in name else "#2474b5" for name in names]
    fig, axes = plt.subplots(2, 1, figsize=(11, 7), constrained_layout=True)
    for axis, key, ylabel, limit in ((axes[0], "mean_survival_s", "Mean survival, capped at 20 s", 21),
                                     (axes[1], "tracking_integral_fixed_horizon", "Tracking integral / 20 s", 1)):
        values = [last[name][key] for name in names]
        axis.bar(labels, values, color=colors)
        axis.set_ylabel(ylabel)
        axis.set_ylim(0, limit)
        axis.grid(axis="y", alpha=.2)
        for i, value in enumerate(values):
            axis.text(i, value + limit * .015, f"{value:.3f}", ha="center", fontsize=9)
    fig.suptitle("Matched first episodes; deterministic policies; two reset seeds")
    fig.savefig(args.output.with_name("tita_ppo_flash_native_comparison.png"), dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
