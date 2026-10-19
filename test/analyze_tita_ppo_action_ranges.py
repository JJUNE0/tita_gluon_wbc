"""DESKTOP_DRY_RUN: quantify signed PPO distributions and candidate range effects."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--distribution", type=Path, required=True)
    parser.add_argument("--caps", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    raw = json.loads(args.distribution.read_text())
    assert raw["evidence_status"] == "PASS"
    baseline = [c for c in raw["cases"] if c["name"] == "baseline"]
    histories = [dict(np.load(ROOT / c["history"])) for c in baseline]
    joints = raw["joint_order"]
    quantiles = [.001, .005, .01, .05, .5, .95, .99, .995, .999]
    absolute_quantiles = [.5, .9, .95, .99, .995, .999]

    def statistics(values):
        values = values[np.isfinite(values)]
        assert len(values) and np.isfinite(values).all()
        return {"samples": len(values), "mean": float(values.mean()), "std": float(values.std()),
                "minimum": float(values.min()), "maximum": float(values.max()),
                "signed_quantiles": dict(zip(map(str, quantiles), np.quantile(values, quantiles).tolist())),
                "absolute_quantiles": dict(zip(map(str, absolute_quantiles), np.quantile(abs(values), absolute_quantiles).tolist())),
                "fraction_abs_gt_1": float((abs(values) > 1).mean())}

    summary = {
        "execution_domain": "DESKTOP_DRY_RUN", "evidence_status": "PASS",
        "policy_checkpoint_sha256": raw["policy_checkpoint_sha256"],
        "distribution_source": str(args.distribution),
        "limits": {k: raw[k] for k in ("native_action_scale", "native_action_offset", "joint_pos_limits_rad",
                                       "soft_joint_pos_limits_rad", "joint_vel_limits_rad_s",
                                       "soft_joint_vel_limits_rad_s", "actuator_limits", "policy_sigma_raw")},
        "joints": {}, "candidates": {},
        "limitations": ["Distribution is measured from one trained PPO checkpoint, not multiple training seeds.",
                        "Counterfactual Gaussian samples share deterministic visited states; actual Gaussian rollout distributions are reported separately.",
                        "Rare startup and recovery actions may matter despite a small pooled frequency.",
                        "Fixed-policy caps do not predict fresh SAC training convergence.",
                        "Command bounds and measured physical joint velocity are different quantities."],
    }
    mean_arrays = [h["mean_action"] for h in histories]
    for number, name in enumerate(joints):
        entry = {}
        for source in ("mean_action", "gaussian_sample"):
            full = np.concatenate([h[source][:, :, number].ravel() for h in histories])
            entry[source] = statistics(full)
        for phase, start, end in (("startup_0_2s", 0, 100), ("steady_4_10s", 200, 500),
                                  ("later_13_20s", 650, 1000)):
            values = np.concatenate([h["mean_action"][start:end, :, number].ravel() for h in histories])
            entry[phase] = statistics(values)
        stop_values = np.concatenate([h["mean_action"][500:650, h["profile_index"] >= 11, number].ravel() for h in histories])
        entry["stop_transition_10_13s"] = statistics(stop_values)
        velocity = np.concatenate([h["joint_vel"][:, :, number].ravel() for h in histories])
        entry["actual_joint_velocity_rad_s"] = statistics(velocity)
        finite = velocity[np.isfinite(velocity)]
        entry["fraction_actual_speed_above_actuator_nominal"] = float((abs(finite) > raw["soft_joint_vel_limits_rad_s"][number] + 1e-3).mean())
        clipped = np.concatenate([h["torque_clipped"][:, :, number].ravel() for h in histories])
        entry["torque_clip_fraction"] = float(np.nanmean(clipped))
        offset, scale = raw["native_action_offset"][number], raw["native_action_scale"][number]
        if number not in (3, 7):
            commands = np.concatenate([h["mean_action"][:, :, number].ravel() for h in histories]) * scale + offset
            commands = commands[np.isfinite(commands)]
            soft_low, soft_high = raw["soft_joint_pos_limits_rad"][number]
            hard_low, hard_high = raw["joint_pos_limits_rad"][number]
            entry["fraction_nominal_target_outside_soft_position_limits"] = float(((commands < soft_low) | (commands > soft_high)).mean())
            entry["fraction_nominal_target_outside_hard_position_limits"] = float(((commands < hard_low) | (commands > hard_high)).mean())
        summary["joints"][name] = entry

    if args.caps:
        caps = json.loads(args.caps.read_text())
        assert caps["evidence_status"] == "PASS" and caps["policy_checkpoint_sha256"] == raw["policy_checkpoint_sha256"]
        summary["caps_source"] = str(args.caps)
        arrays = {}
        for name in sorted({c["name"] for c in caps["cases"]}):
            cases = sorted((c for c in caps["cases"] if c["name"] == name), key=lambda c: c["seed"])
            counts = np.array([c["life_steps"] for c in cases])
            fell = np.array([c["fell"] for c in cases])
            sums = np.array([c["per_env_sums"] for c in cases])
            horizon = caps["args"]["steps"]
            dt = np.load(ROOT / cases[0]["history"])["dt"].item()
            arrays[name] = np.stack([counts * dt, sums[:, :, 0] / horizon, sums[:, :, 1] / horizon], axis=-1)
            item = {"trials": counts.size, "reset_seeds": [c["seed"] for c in cases],
                    "mean_survival_s": float(counts.mean() * dt), "survival_at_horizon": float(((counts >= horizon) & ~fell).mean()),
                    "tracking_xy_fixed_horizon": float(sums[:, :, 0].mean() / horizon),
                    "tracking_yaw_fixed_horizon": float(sums[:, :, 1].mean() / horizon),
                    "raw_lower": cases[0]["raw_lower"], "raw_upper": cases[0]["raw_upper"], "groups": []}
            width = caps["args"]["envs_per_profile"]
            for group, profile in enumerate(caps["profiles"]):
                sl = slice(group * width, (group + 1) * width)
                item["groups"].append({"profile": profile["name"], "mean_survival_s": float(counts[:, sl].mean() * dt),
                                        "survival_at_horizon": float(((counts[:, sl] >= horizon) & ~fell[:, sl]).mean()),
                                        "tracking_xy_fixed_horizon": float(sums[:, sl, 0].mean() / horizon),
                                        "tracking_yaw_fixed_horizon": float(sums[:, sl, 1].mean() / horizon)})
            if name == "gaussian_baseline":
                distributions = [np.load(ROOT / c["history"])["applied_action"] for c in cases]
                summary["actual_gaussian_rollout_distribution"] = {joint: statistics(np.concatenate([h[:, :, i].ravel() for h in distributions])) for i, joint in enumerate(joints)}
            if item["raw_lower"] is not None:
                lower, upper = np.array(item["raw_lower"]), np.array(item["raw_upper"])
                means = np.concatenate([a.reshape(-1, 8) for a in mean_arrays])
                valid = np.isfinite(means).all(-1)
                item["baseline_action_samples_clipped_fraction_per_joint"] = (((means[valid] < lower) | (means[valid] > upper)).mean(0)).tolist()
                item["physical_lower"] = (np.array(raw["native_action_offset"]) + np.array(raw["native_action_scale"]) * lower).tolist()
                item["physical_upper"] = (np.array(raw["native_action_offset"]) + np.array(raw["native_action_scale"]) * upper).tolist()
            summary["candidates"][name] = item
        rng = np.random.default_rng(42)
        indices = np.concatenate([rng.integers(g * width, (g + 1) * width, (10000, width)) for g in range(len(caps["profiles"]))], axis=1)
        for name, item in summary["candidates"].items():
            difference = (arrays[name] - arrays["baseline"]).mean(0)
            draws = difference[indices].mean(1)
            item["paired_difference_vs_baseline"] = {
                field: {"mean": float(difference[:, number].mean()),
                        "cluster_bootstrap_95_interval": np.quantile(draws[:, number], [.025, .975]).tolist()}
                for number, field in enumerate(("survival_s", "tracking_xy", "tracking_yaw"))}

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    print("DESKTOP_DRY_RUN PASS:", args.output)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    for joint_number, axis in enumerate(axes.flat):
        for side, color, label in ((0, "#2474b5", "Left"), (4, "#e07a24", "Right")):
            values = np.concatenate([a[:, :, joint_number + side].ravel() for a in mean_arrays])
            values = values[np.isfinite(values)]
            axis.hist(values, bins=120, density=True, histtype="step", color=color, label=label)
        axis.set_title(("Hip position", "Shoulder position", "Knee position", "Wheel velocity")[joint_number])
        axis.set_xlabel("Native PPO raw action (signed)")
        axis.set_ylabel("Density (log scale)")
        axis.set_yscale("log")
        axis.axvline(-1, color="gray", linestyle="--", linewidth=1)
        axis.axvline(1, color="gray", linestyle="--", linewidth=1)
        axis.grid(alpha=.2)
        axis.legend()
    fig.suptitle("PPO 2000-iteration mean actions; 13 profiles × 3 reset seeds")
    fig.savefig(args.output.with_name("tita_ppo_signed_action_distribution.png"), dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    for joint_number, axis in enumerate(axes.flat):
        for side, color, label in ((0, "#2474b5", "Left"), (4, "#e07a24", "Right")):
            values = np.concatenate([abs(a[:, :, joint_number + side]).ravel() for a in mean_arrays])
            values = np.sort(values[np.isfinite(values)])
            tail_counts = np.unique(np.rint(np.geomspace(1, len(values), 2500)).astype(int))
            index = np.sort(len(values) - tail_counts)
            axis.plot(values[index], (len(values) - index) / len(values), color=color, label=label)
        axis.set_title(("Hip position", "Shoulder position", "Knee position", "Wheel velocity")[joint_number])
        axis.set_xlabel("Absolute native raw action")
        axis.set_ylabel("Empirical upper-tail fraction")
        axis.set_yscale("log")
        axis.set_ylim(1e-5, 1)
        axis.grid(alpha=.2)
        axis.legend()
    fig.suptitle("Action tails; rare startup/recovery excursions retained")
    fig.savefig(args.output.with_name("tita_ppo_action_tail_distribution.png"), dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
