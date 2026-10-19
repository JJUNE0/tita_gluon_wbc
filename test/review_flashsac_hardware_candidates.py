"""DESKTOP_DRY_RUN / VALIDATION_SIM: audit existing trials and compare commands.

No robot access or controller changes. Uses existing frozen exports and the
flat-floor, native-PD simulation runner. All residuals remain disabled.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path

import numpy as np

from velocity_bias_campaign import REPO, digest, make_runner, write

ARCHIVE = REPO / 'docs/exp/2026-10-16/velocity_bias_overnight'
POLICIES = {
    'current_A60000': 'tita_flash_sac_115632_883848_model_60000',
    'A75000': 'tita_flash_sac_115632_883848_model_75000',
    'A50000': 'tita_flash_sac_115632_883848_model_50000',
    'B60000': 'tita_flash_sac_193248_068255_model_60000',
}


def audit():
    survey = json.loads((ARCHIVE / 'survey_results.json').read_text())
    physics = json.loads((ARCHIVE / 'physics02_results.json').read_text())
    long = json.loads((ARCHIVE / 'long01_results.json').read_text())
    exports = {r['id']: r for r in json.loads((ARCHIVE / 'export_results.json').read_text())}
    rows = []
    for nominal in survey:
        cid = nominal['job']['checkpoint_id']
        export = exports[cid]
        assert digest(export['checkpoint']) == export['sha256']
        bundle = ARCHIVE / 'exports' / cid
        manifest = json.loads((bundle / 'manifest.json').read_text())
        assert digest(bundle / 'policy.onnx') == export['onnx_sha256'] == manifest['onnx_sha256']
        assert digest(bundle / 'config.json') == manifest['config_sha256']
        cfg = json.loads((bundle / 'config.json').read_text())
        assert cfg['policy_interface']['checkpoint_sha256'] == export['sha256']
        rs = [r for r in physics if r['job']['checkpoint_id'] == cid
              and r['job']['law'].get('mode') == 'constant']
        ls = [r for r in long if r['job']['checkpoint_id'] == cid
              and r['job']['law'].get('mode') == 'constant']
        assert len(rs) == 7 and len(ls) == 1
        rows.append(dict(checkpoint_id=cid, checkpoint_sha256=export['sha256'],
                         onnx_sha256=export['onnx_sha256'], config_sha256=manifest['config_sha256'],
                         bundle=str(bundle.relative_to(REPO)), survey_60s=nominal,
                         nominal_300s=ls[0], physics_60s=rs,
                         complete_physics=sum(bool(r.get('complete')) for r in rs),
                         worst_physics_tail_speed_m_s=max(abs(r.get('tail_speed_mean_m_s', 999.)) for r in rs)))
    return rows


def command_trial(job):
    cid, label, output = job
    cfg = json.loads((ARCHIVE / 'exports' / cid / 'config.json').read_text())
    runner = make_runner(cfg, dict(seed=104, pitch=0.))
    rows, failures = [], []
    try:
        # Runner disables world-body obstacles before its transform-up startup.
        dt = runner.env.control_dt
        assert abs(dt - .02) < 1e-12
        floor = runner.env.model.geom('floor').id
        obstacles = (runner.env.model.geom_bodyid == 0) & (np.arange(runner.env.model.ngeom) != floor)
        assert np.all(runner.env.model.geom_contype[obstacles] == 0)
        for tick in range(round(8. / dt)):
            runner.step_bias(0.)
            if tick >= 50 and runner.failures():
                raise RuntimeError(f'warmup: {runner.failures()}')
        phases = [(0., 0.), (.1, 0.), (0., 0.), (-.1, 0.), (0., .2), (0., 0.)]
        peak_torque = 0.
        for tick in range(round(120. / dt)):
            vx, wz = phases[tick // 1000]
            command = np.array([vx, 0., wz], dtype=np.float32)
            previous = runner.playback.last_action.copy()
            step = runner.step_bias(0., command)
            np.testing.assert_array_equal(previous, step['history'])
            np.testing.assert_allclose(step['motor'], step['baseline_motor'], atol=1e-6, rtol=0.)
            o = runner.observation
            rows.append([tick * dt, vx, wz, float(o['base_velocity'][0]),
                         float(o['yaw_rate'][0]), *o['rpy'], *o['base_position'][:2]])
            peak_torque = max(peak_torque, float(abs(step['motor'][:, [3, 7]]).max()))
            failures = runner.failures()
            if failures:
                break
        trace = np.asarray(rows)
        phases_result = []
        for phase in range(6):
            # Last 10 s of each phase; full transient is retained in overall RMSE.
            tail = trace[(trace[:, 0] >= phase * 20 + 10) & (trace[:, 0] < (phase + 1) * 20)]
            if len(tail):
                phases_result.append(dict(phase=phase, command=phases[phase],
                                          mean_vx_m_s=float(tail[:, 3].mean()),
                                          mean_yaw_rad_s=float(tail[:, 4].mean()),
                                          mean_pitch_deg=float(np.rad2deg(tail[:, 6]).mean())))
        result = dict(execution_domain='VALIDATION_SIM', checkpoint_id=cid,
                      checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'], label=label,
                      evidence_status='PASS' if len(trace) == 6000 and not failures else 'FAIL',
                      failures=failures, samples=len(trace),
                      vx_rmse_m_s=float(np.sqrt(np.mean((trace[:, 3] - trace[:, 1]) ** 2))),
                      yaw_rmse_rad_s=float(np.sqrt(np.mean((trace[:, 4] - trace[:, 2]) ** 2))),
                      max_tilt_deg=float(np.rad2deg(abs(trace[:, 5:7]).max())),
                      peak_wheel_torque_nm=peak_torque, phases=phases_result)
        np.savez_compressed(Path(output) / f'{label}_commands.npz', trace=trace)
        write(Path(output) / f'{label}_commands.json', result)
        return result
    finally:
        runner.env.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    assert output.is_relative_to(REPO / 'docs/exp')
    output.mkdir(parents=True, exist_ok=False)
    existing = audit()
    write(output / 'archive_audit.json', existing)
    current = json.loads((ARCHIVE / 'exports' / POLICIES['current_A60000'] / 'config.json').read_text())
    for cid in POLICIES.values():
        cfg = json.loads((ARCHIVE / 'exports' / cid / 'config.json').read_text())
        assert cfg['policy_interface']['observations'] == current['policy_interface']['observations']
        assert cfg['policy_interface']['actions'] == current['policy_interface']['actions']
        assert cfg['robot'] == current['robot']
    write(output / 'protocol.json', dict(execution_domain='VALIDATION_SIM',
          policies=POLICIES, script_sha256=digest(__file__), seed=104,
          warmup_s=8., phase_s=20., commands=[[0, 0], [.1, 0], [0, 0], [-.1, 0], [0, .2], [0, 0]],
          residuals=False, terrain='flat floor; world-body obstacles disabled before startup',
          screening='completion; candidate RMSE <= current * 1.1 + .002 m/s / .01 rad/s',
          limitation='No hardware approval, real transition matching, or multi-seed robustness claim.'))
    jobs = [(cid, label, str(output)) for label, cid in POLICIES.items()]
    with ProcessPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(command_trial, jobs))
    baseline = next(r for r in results if r['label'] == 'current_A60000')
    for r in results:
        r['command_screen_pass'] = (r['evidence_status'] == 'PASS'
            and r['vx_rmse_m_s'] <= 1.1 * baseline['vx_rmse_m_s'] + .002
            and r['yaw_rmse_rad_s'] <= 1.1 * baseline['yaw_rmse_rad_s'] + .01)
    write(output / 'command_comparison.json', results)
    print(json.dumps(results, indent=2), flush=True)


if __name__ == '__main__':
    main()
