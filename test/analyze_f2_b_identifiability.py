"""DESKTOP_DRY_RUN: diagnose frozen F-2 least squares; no controller/model export.

Only archived data are read. Conditional regressions below are loss-profile and
identifiability diagnostics, never replacement dynamics or deployable gains.
"""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[1]
OLD = REPO / 'docs/exp/2026-10-15/flash_torque_residual'
RESPONSE = REPO / 'docs/exp/2026-10-15/f2_response_validation'
NAMES = ['path', 'velocity', 'pitch', 'pitch_rate']
FLOOR = np.array([1e-7, 1e-5, 1e-7, 1e-5])
INPUTS = {}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remember(path):
    INPUTS[str(path.relative_to(REPO))] = digest(path)
    return path


def load_json(path):
    return json.loads(remember(path).read_text())


def load_npz(path):
    with np.load(remember(path)) as data:
        return {k: data[k] for k in data.files}


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def rms(x):
    return np.sqrt(np.mean(np.asarray(x) ** 2, axis=0))


def residualize(x, controls):
    return x - controls @ np.linalg.lstsq(controls, x, rcond=None)[0]


def fwl(states, target, u):
    """Exact no-intercept Frisch-Waugh-Lovell calculation for original design."""
    ru = residualize(u, states)
    ry = residualize(target, states)
    energy = float(ru @ ru)
    B = ru @ ry / energy
    return dict(B=B.tolist(), input_rms=float(rms(u)), innovation_rms=float(rms(ru)),
        innovation_energy_fraction=energy / float(u @ u),
        input_predictable_energy_fraction=1. - energy / float(u @ u),
        uncentered_input_vif=float(u @ u) / energy,
        partial_output_correlation=(ru @ ry / np.sqrt(energy * np.sum(ry ** 2, axis=0))).tolist()), ru


def fit_diagnostic(x, y, u):
    target = y.copy()
    target[:, 0] -= x[:, 0]
    z = np.column_stack([x[:, 1:], u])
    coefficient = np.linalg.lstsq(z, target, rcond=None)[0]
    return coefficient, target, z


def original_episodes():
    baseline = {(r['seed'], r['pitch_delta_rad']): r for r in map(json.loads,
        remember(OLD / 'f1_nominal/results.jsonl').read_text().splitlines()) if r['label'] == 'A'}
    rows = list(map(json.loads, remember(OLD / 'f2_closed/probe_results.jsonl').read_text().splitlines()))
    episodes = []
    for row in rows:
        trace = load_npz(OLD / 'f2_closed' / row['trace'])
        base = load_npz(OLD / 'f1_nominal' / baseline[(row['seed'], row['pitch_delta_rad'])]['trace'])
        delta = trace['synchronized_state'] - base['synchronized_state']
        u = (trace['command_substeps'][1:, :, [3, 7]] - trace['flash_substeps'][1:, :, [3, 7]]).sum(2).mean(1)
        time = trace['time'][:-1]
        mask = (time >= 2.) & (time < 10.5) & ~((time >= 2.96) & (time <= 3.3))
        x, y, u, time = delta[:-1][mask], delta[1:][mask], u[mask], time[mask]
        coefficient, target, z = fit_diagnostic(x, y, u)
        info, _ = fwl(x[:, 1:], target, u)
        episodes.append(dict(seed=row['seed'], pitch=row['pitch_delta_rad'], amplitude=row['alpha'],
            x=x, y=y, u=u, time=time, target=target, z=z, diagnostic=info,
            trace=trace, base=base, mask=mask, B=coefficient[-1]))
    return episodes


def stack(episodes):
    return tuple(np.concatenate([e[k] for e in episodes]) for k in ['x', 'y', 'u'])


def lag_diagnostics(episodes, A, B):
    records = []
    for lag in [1, 2, 5, 10, 25]:
        errors, past_u, controls, innovation, previous_innovation = [], [], [], [], []
        for e in episodes:
            z = e['z']
            err = e['y'] - e['x'] @ A.T - e['u'][:, None] * B
            # Never cross the omitted disturbance interval or episode boundaries.
            valid = abs(e['time'][lag:] - e['time'][:-lag] - lag * .02) < 1e-8
            errors.append(err[lag:][valid]); past_u.append(e['u'][:-lag][valid])
            controls.append(z[lag:][valid])
            _, ru = fwl(e['x'][:, 1:], e['target'], e['u'])
            innovation.append(ru[lag:][valid]); previous_innovation.append(ru[:-lag][valid])
        z = np.concatenate(controls)
        ep = residualize(np.concatenate(errors), z)
        up = residualize(np.concatenate(past_u), z)
        partial = up @ ep / np.sqrt((up @ up) * np.sum(ep ** 2, axis=0))
        records.append(dict(lag_steps=lag, lag_s=lag * .02, transitions=len(up),
            residual_error_vs_past_u_partial_correlation=partial.tolist(),
            input_innovation_serial_correlation=float(np.corrcoef(
                np.concatenate(innovation), np.concatenate(previous_innovation))[0, 1])))
    return records


def history_diagnostics(episodes, A, B):
    """Association tests only: no expanded-state dynamics are fitted."""
    groups = {'previous_raw_action': [], 'joint_position': [], 'joint_velocity': []}
    z, errors = [], []
    for e in episodes:
        # Row k policy_action is the output of transition k-1 -> k and therefore
        # the actor's last_action when choosing transition k -> k+1. The saved
        # history_input at row k belongs to the previous inference (one older).
        for key, channel in [('previous_raw_action', 'policy_action'),
                             ('joint_position', 'joint_position'), ('joint_velocity', 'joint_velocity')]:
            groups[key].append((e['trace'][channel][:-1] - e['base'][channel][:-1])[e['mask']])
        z.append(e['z'])
        errors.append(e['y'] - e['x'] @ A.T - e['u'][:, None] * B)
    z = np.concatenate(z)
    errors = residualize(np.concatenate(errors), z)
    records = {}
    for name, values in groups.items():
        h = residualize(np.concatenate(values), z)
        corr = h.T @ errors / np.maximum(np.sqrt(np.sum(h ** 2, axis=0)[:, None] *
            np.sum(errors ** 2, axis=0)[None, :]), 1e-30)
        records[name] = dict(channel_partial_correlations=corr.tolist(),
            conditional_channel_rms=rms(h).tolist(), channels='native 8 channels; wheel indices 3,7')
    return records


def pulse_a_only(A):
    records = []
    example = None
    for path in sorted((RESPONSE / 'primary').glob('*/results.json')):
        info = load_json(path)
        for row in info['responses']:
            if row['family'] not in ('pulse_pos', 'pulse_neg'):
                continue
            trace = load_npz(path.parent / row['trace'])
            base = load_npz(path.parent / row['baseline'])
            u = trace['actual_u'] - base['actual_u']
            # Preserve original pulse+slew. Begin after the actual residual is zero.
            start = int(np.flatnonzero(abs(u) > 1e-7)[-1] + 1)
            assert np.max(abs(u[start:])) <= 1e-7
            for source in ['sensor', 'gt']:
                delta = trace[source] - base[source]
                one = delta[start:-1] @ A.T
                pred = [delta[start]]
                for _ in range(start, len(u)):
                    pred.append(A @ pred[-1])
                pred = np.asarray(pred)
                horizons = {}
                for h in [5, 10, 25, 50]:
                    if len(pred) <= h:
                        continue
                    # One prediction at fixed horizon per pulse; normalized below
                    # by pooled RMS across all pulses, rather than tiny endpoints.
                    horizons[str(h)] = dict(error=(pred[h] - delta[start+h]).tolist(),
                        actual=delta[start+h].tolist(),
                        hold_error=(delta[start] - delta[start+h]).tolist())
                records.append(dict(context=row['context'], amplitude=row['amplitude'],
                    start_s=row['start_s'], family=row['family'], source=source,
                    zero_input_start_s=start * .02, remaining_s=(len(u) - start) * .02,
                    one_step_rmse=rms(one - delta[start+1:]).tolist(),
                    free_rmse=rms(pred[1:] - delta[start+1:]).tolist(),
                    signal_rms=rms(delta[start+1:]).tolist(),
                    full_nrmse=(rms(pred[1:] - delta[start+1:]) /
                        np.maximum(rms(delta[start+1:]), FLOOR)).tolist(), horizons=horizons))
                if source == 'sensor' and row['seed'] == 45 and row['pitch'] == 0. and row['start_s'] == 6. and row['family'] == 'pulse_pos' and row['amplitude'] == .25:
                    example = (delta, u, pred, start)
    summary = {}
    for source in ['sensor', 'gt']:
        subset = [r for r in records if r['source'] == source]
        result = dict(traces=len(subset), zero_start_s_range=[min(r['zero_input_start_s'] for r in subset),
            max(r['zero_input_start_s'] for r in subset)],
            median_one_step_rmse=np.median([r['one_step_rmse'] for r in subset], axis=0).tolist(),
            median_free_nrmse=np.median([r['full_nrmse'] for r in subset], axis=0).tolist(), horizons={})
        for h in [5, 10, 25, 50]:
            values = [r['horizons'][str(h)] for r in subset if str(h) in r['horizons']]
            error, actual, hold = [np.asarray([v[k] for v in values]) for k in ['error', 'actual', 'hold_error']]
            result['horizons'][str(h)] = dict(pooled_rmse=rms(error).tolist(),
                pooled_signal_rms=rms(actual).tolist(),
                pooled_nrmse=(rms(error) / np.maximum(rms(actual), FLOOR)).tolist(),
                initial_state_hold_rmse=rms(hold).tolist())
        summary[source] = result
    return records, summary, example


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    if not out.is_relative_to(REPO / 'docs/exp') or out.exists():
        parser.error('New evidence directory under docs/exp required')
    out.mkdir(parents=True)
    archive = load_npz(OLD / 'f2_closed/identification.npz')
    manifest = load_json(OLD / 'f2_closed/manifest.json')
    frozen = load_json(OLD / 'f2_closed/model.json')
    A, B = np.asarray(frozen['A_closed']), np.asarray(frozen['B_res'])[:, 0]
    direct = load_json(RESPONSE / 'direct_B.json')
    ref = np.median([r['sensor_B'] for r in direct if r['actor'] == 'cached'], axis=0)
    episodes = original_episodes()
    train = [e for e in episodes if e['seed'] in (42, 43)]
    heldout = [e for e in episodes if e['seed'] == 44]
    x, y, u = stack(train)
    for key, value in [('x', x), ('y', y), ('u', u)]:
        np.testing.assert_array_equal(value, archive[key])
    for key, value in zip(['heldout_x', 'heldout_y', 'heldout_u'], stack(heldout)):
        np.testing.assert_array_equal(value, archive[key])
    coefficient, target, z = fit_diagnostic(x, y, u)
    np.testing.assert_allclose(coefficient[-1], B, atol=1e-12, rtol=1e-9)
    diagnostics, ru = fwl(x[:, 1:], target, u)
    np.testing.assert_allclose(diagnostics['B'], B, atol=1e-12, rtol=1e-9)
    singular = np.linalg.svd(z / np.sqrt(np.sum(z ** 2, axis=0)), compute_uv=False)
    corr = np.corrcoef(z, rowvar=False)
    diagnostics.update(centered_correlation=corr.tolist(), regressor_names=['delta_v', 'delta_pitch', 'delta_rate', 'u'],
        unit_norm_design_singular_values=singular.tolist(), unit_norm_condition=float(singular[0] / singular[-1]),
        original_scaled_condition=frozen['diagnostics']['scaled_condition_number'], rank=int(np.linalg.matrix_rank(z)),
        state_to_input_projection=np.linalg.lstsq(x[:, 1:], u, rcond=None)[0].tolist())
    subsets = {}
    for name, subset in [('amp_0.1', [e for e in train if e['amplitude'] == .1]),
                         ('amp_0.25', [e for e in train if e['amplitude'] == .25]),
                         ('amp_0.5', [e for e in train if e['amplitude'] == .5]),
                         ('heldout_seed44', heldout)]:
        sx, sy, su = stack(subset)
        _, st, _ = fit_diagnostic(sx, sy, su)
        subsets[name] = fwl(sx[:, 1:], st, su)[0]
    for name, mask in [('early_2_5s', (np.concatenate([e['time'] for e in train]) < 5.)),
                       ('late_5_10.5s', (np.concatenate([e['time'] for e in train]) >= 5.))]:
        subsets[name] = fwl(x[mask, 1:], target[mask], u[mask])[0]
    loo = []
    for omitted in range(len(train)):
        lx, ly, lu = stack([e for i, e in enumerate(train) if i != omitted])
        lc, _, _ = fit_diagnostic(lx, ly, lu)
        loo.append(lc[-1])
    # Exact least-squares loss profile for fixing B to a supplied reference.
    # Not a candidate dynamics model; A is a nuisance parameter in this calculation.
    conditional_states = np.linalg.lstsq(x[:, 1:], target - u[:, None] * ref, rcond=None)[0]
    err = target - z @ coefficient
    err_ref = target - x[:, 1:] @ conditional_states - u[:, None] * ref
    penalty = np.sum(ru ** 2) * (ref - B) ** 2
    np.testing.assert_allclose(np.sum(err_ref**2, axis=0) - np.sum(err**2, axis=0), penalty, atol=1e-14, rtol=1e-8)
    np.testing.assert_allclose(conditional_states - coefficient[:3],
        np.outer(np.linalg.lstsq(x[:, 1:], u, rcond=None)[0], B - ref), atol=1e-12)
    profile = dict(reference='Median54 direct central differences at18 related snapshots from6 initial conditions; not exact constant global B',
        direct_B_reference=ref.tolist(), original_rmse=rms(err).tolist(),
        fixed_reference_B_profile_rmse=rms(err_ref).tolist(),
        rmse_ratio=(rms(err_ref) / rms(err)).tolist(), SSE_penalty=penalty.tolist(),
        fractional_input_error_cancelled_by_adjusting_A=diagnostics['input_predictable_energy_fraction'],
        remaining_error_vs_input_innovation_correlation=(ru @ err_ref /
            np.sqrt((ru @ ru) * np.sum(err_ref ** 2, axis=0))).tolist())
    waveforms = {}
    for amplitude in [.1, .25, .5]:
        waves = [e['u'] for e in episodes if e['amplitude'] == amplitude]
        waveforms[str(amplitude)] = dict(episodes=len(waves),
            maximum_difference_between_initial_conditions=float(np.max(abs(np.asarray(waves) - waves[0]))),
            min_rms=float(min(rms(w) for w in waves)), max_rms=float(max(rms(w) for w in waves)))
    history = history_diagnostics(train, A, B)
    lag = lag_diagnostics(train, A, B)
    pulse_rows, pulse_summary, example = pulse_a_only(A)
    per_episode = [{k: e[k] for k in ['seed', 'pitch', 'amplitude', 'diagnostic']} for e in episodes]
    write(out / 'regression_diagnostics.json', dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
        original_B=B.tolist(), direct_B_reference=ref.tolist(), training_samples=len(x), diagnostics=diagnostics,
        subset_diagnostics=subsets, episodes=per_episode, input_waveforms=waveforms,
        leave_one_episode_out_B_range=[np.min(loo, axis=0).tolist(), np.max(loo, axis=0).tolist()],
        fixed_B_loss_profile=profile, lag_diagnostics=lag, history_associations=history,
        caveat='Descriptive correlated deterministic data; no iid confidence intervals; no causal omitted-state attribution.'))
    write(out / 'pulse_a_only.json', dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
        summary=pulse_summary, records=pulse_rows, note='Recorded finite pulse plus slew tail, not a one-step impulse.'))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    im = axes[0].imshow(corr, vmin=-1, vmax=1, cmap='coolwarm')
    axes[0].set_xticks(range(4), ['dv', 'pitch', 'rate', 'u']); axes[0].set_yticks(range(4), ['dv', 'pitch', 'rate', 'u'])
    for i in range(4):
        for j in range(4):
            axes[0].text(j, i, f'{corr[i,j]:.3f}', ha='center', va='center')
    fig.colorbar(im, ax=axes[0], fraction=.046)
    axes[0].set_title('Centered regressor correlation')
    axes[1].bar(['Explained by states', 'Remaining innovation'],
        [diagnostics['input_predictable_energy_fraction'], diagnostics['innovation_energy_fraction']])
    axes[1].set_ylim(0, 1); axes[1].set_ylabel('Uncentered input energy fraction')
    axes[1].set_title('Original no-intercept regression')
    fig.tight_layout(); fig.savefig(out / 'input_identifiability.png', dpi=160); plt.close(fig)
    delta, inp, pred, start = example
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    t = np.arange(len(delta)) * .02
    axes[0].step(t[:-1], inp, where='post'); axes[0].set_ylabel('Residual [Nm]')
    for ax, i, label in [(axes[1], 1, 'Delta v [m/s]'), (axes[2], 2, 'Delta pitch [rad]')]:
        ax.plot(t, delta[:, i], label='Measured pulse response')
        ax.plot(t[start:], pred[:, i], '--', label='Frozen A only, initialized at zero-input start')
        ax.set_ylabel(label); ax.legend(fontsize=8)
    for ax in axes:
        ax.axvline(start * .02, color='grey', linestyle=':'); ax.grid(True)
    axes[-1].set_xlabel('Time since branch [s]')
    fig.suptitle('Existing cached-actor pulse, seed45/pitch0, branch6s, +0.25Nm')
    fig.tight_layout(); fig.savefig(out / 'pulse_a_only.png', dpi=160); plt.close(fig)
    unchanged = all(digest(REPO / name) == value for name, value in INPUTS.items())
    assert unchanged
    write(out / 'integrity.json', dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
        all_read_inputs_preserved=unchanged, input_sha256=INPUTS, analysis_script_sha256=digest(Path(__file__)),
        archive_arrays_reconstructed_exactly=True, FWL_reproduces_B=True,
        conditional_loss_identity=True, conditional_A_identity=True,
        checkpoint_sha256=manifest['checkpoint_sha256'], onnx_sha256=manifest['onnx_sha256'],
        new_simulations=0, deployed_models=0, controller_changes=0))
    print('[DESKTOP_DRY_RUN] PASS: archive reconstruction, FWL, loss identities, input hashes')
    print('Input innovation energy fraction:', diagnostics['innovation_energy_fraction'])
    print('Subsets B velocity/pitch:', {k: [v['B'][1], v['B'][2]] for k, v in subsets.items()})
    print('A-only zero-input horizon pooled NRMSE:', pulse_summary['sensor']['horizons'])


if __name__ == '__main__':
    main()
