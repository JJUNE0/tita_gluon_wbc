"""VALIDATION_SIM: E timing checks and bounded additive FlashSAC wheel residuals.

Existing policy, observation/history, adapter, leg PD and physics code are reused.
Only residual state sensing is synchronized; the actor sensor path stays as A.
"""

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'test'))
from debug_lqr_d4_diagnostics import ARCHIVE, Plant
from eval_flash_leg_fixed_lqr4 import action_history_slice, hybrid_torque
from sim2sim.lqr.controller import WheelLQR
from sim2sim.lqr.evaluate import ground_truth, write_json
from sim2sim.lqr.model import Description
from sim2sim.lqr.runtime import LEGS, WHEELS, policy_config
from sim2sim_ros2_jazzy.checkpoint import read_yaml, sha256

E_ARCHIVE = REPO / 'docs/exp/2026-10-15/flash_leg_fixed_lqr4/full'
DEFAULT_RESIDUAL = dict(kp=2., kv=.5, limit_total_nm=1., ramp_s=1., slew_total_nm_s=2.)


class PositionVelocityResidual:
    """Total sagittal torque, in Nm, split between the two signed wheel axes."""

    def __init__(self, config, alpha, p_hold):
        self.config, self.alpha, self.p_hold = dict(config), float(alpha), float(p_hold)
        self.previous = 0.

    def command(self, state, t, dt):
        cfg = self.config
        raw = -cfg['kp'] * (state[0] - self.p_hold) - cfg['kv'] * state[1]
        fraction = np.clip(t / cfg['ramp_s'], 0., 1.)
        ramp = fraction**2 * (3. - 2. * fraction)
        target = self.alpha * ramp * np.clip(raw, -cfg['limit_total_nm'], cfg['limit_total_nm'])
        step = cfg['slew_total_nm_s'] * dt
        self.previous = float(np.clip(target, self.previous-step, self.previous+step))
        return self.previous, float(raw), float(ramp)


def additive_torque(torque, total_residual, signs):
    # Keep exact A arithmetic for alpha=0, including dtype and saturation order.
    if total_residual == 0.:
        return torque.copy()
    result = torque.copy()
    result[WHEELS] += signs * total_residual / 2.
    return result


def run(policy, cfg, description, parameters, seed, pitch, label, source, output,
        alpha=0., residual_config=None, residual_factory=PositionVelocityResidual):
    plant = Plant(policy, cfg, description, parameters, {'name':'nominal'}, seed, pitch)
    env, playback = plant.env, plant.playback
    observation = plant.observe()
    initial = np.r_[env.data.qpos, env.data.qvel].copy()
    fixed = WheelLQR(parameters, env.control_dt, 4, cfg['controller'], adaptive=False) if label.startswith('E-') else None
    if fixed:
        fixed.frozen = True
    residual = residual_factory(residual_config or DEFAULT_RESIDUAL, alpha, observation[source][0])
    history_slice, history_scale, history_clip = action_history_slice(policy)
    commands = np.zeros((env.decimation, 8))
    motors, flash = commands.copy(), commands.copy()
    obs = np.zeros(policy['policy']['obs_dim'])
    action, history = np.zeros(8), np.zeros(8)
    u = raw = ramp = 0.
    leg_error = history_error = sum_error = 0.
    rows, violations = [], []
    try:
        for tick in range(round(cfg['duration_s']/env.control_dt)+1):
            t = tick * env.control_dt
            violations, margin = plant.failures(observation, source)
            cached_position, _ = ground_truth(env, plant.wheels)
            rows.append(dict(time=t, sensor_state=observation['sensor'].copy(),
                synchronized_state=observation['synchronized'].copy(), gt_state=observation['gt'].copy(),
                state=observation[source].copy(), gt_position=cached_position.copy(),
                true_position=observation['position'].copy(), true_rpy=observation['rpy'].copy(),
                command_substeps=commands.copy(), motor_substeps=motors.copy(), flash_substeps=flash.copy(),
                policy_observation=obs.copy(), policy_action=action.copy(), history_input=history.copy(),
                residual_total_nm=u if not fixed else 0., wheel_feedback_total_nm=u,
                residual_raw_nm=raw, activation=ramp,
                leg_error=env.joint_pos()[LEGS]-plant.stand[LEGS], joint_position=env.joint_pos(),
                joint_velocity=env.joint_vel(), leg_limit_margin=margin))
            if violations or tick == round(cfg['duration_s']/env.control_dt):
                break
            env.data.xfrc_applied[:] = 0.
            force = cfg['disturbance']
            if force['start_s'] <= t < force['start_s']+force['duration_s']:
                env.data.xfrc_applied[plant.base, 0] = force['force_n']
            history = playback.last_action.copy()
            obs, action = playback.infer()
            expected = history.copy()
            if history_clip is not None:
                expected = np.clip(expected, *history_clip)
            history_error = max(history_error, float(np.max(abs(obs[history_slice]-expected*history_scale))))
            if fixed:
                u = fixed.command(observation[source])
                raw, ramp = float(-fixed.K @ observation[source]), 1.
            else:
                u, raw, ramp = residual.command(observation[source], t, env.control_dt)
            flash_rows = []

            def override(q, dq, torque):
                nonlocal leg_error, sum_error
                flash_rows.append(torque.copy())
                result = hybrid_torque(torque, u, plant.signs) if fixed else additive_torque(torque, u, plant.signs)
                leg_error = max(leg_error, float(np.max(abs(result[LEGS]-torque[LEGS]))))
                expected_wheels = plant.signs*u/2 if fixed else torque[WHEELS]+plant.signs*u/2
                sum_error = max(sum_error, float(np.max(abs(result[WHEELS]-expected_wheels))))
                return result

            def motor(torque):
                # Nominal: identity motor, with the same per-wheel limit as A.
                result = torque.copy()
                result[WHEELS] = np.clip(result[WHEELS], -playback.adapter.limit[WHEELS], playback.adapter.limit[WHEELS])
                return result

            commands, motors = playback.step(action, override, motor)
            np.testing.assert_array_equal(playback.last_action, action)
            flash = np.asarray(flash_rows)
            observation = plant.observe()
        trace = {key:np.asarray([row[key] for row in rows]) for key in rows[0]}
        name = f'{label}_s{seed}_p{pitch:+.3f}'
        np.savez_compressed(output/(name+'.npz'), **trace)
        rms = lambda v: float(np.sqrt(np.mean(np.asarray(v)**2)))
        d = trace['gt_position']-trace['gt_position'][0]
        true_d = trace['true_position']-trace['true_position'][0]
        peak_index = np.linalg.norm(d[:,:2],axis=1).argmax()
        if fixed:
            np.testing.assert_array_equal(fixed.K, fixed.K0)
            assert not fixed.rls.regressors and fixed.accepted == fixed.rejected == 0
        result = dict(execution_domain='VALIDATION_SIM', evidence_status='FAIL' if violations else 'PASS',
            checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'], label=label, state_source=source,
            seed=seed, pitch_delta_rad=pitch, alpha=alpha, residual_config=residual.config,
            initial_physics=initial.tolist(), completed_s=float(trace['time'][-1]), failures=violations,
            trace=name+'.npz', max_displacement_m=float(np.linalg.norm(d[:,:2],axis=1).max()),
            true_max_displacement_m=float(np.linalg.norm(true_d[:,:2],axis=1).max()),
            max_forward_displacement_m=float(abs(d[:,0]).max()), max_lateral_displacement_m=float(abs(d[:,1]).max()),
            xy_at_planar_peak_m=d[peak_index,:2].tolist(), position_rms_m=rms(d[:,:2])*np.sqrt(2),
            pitch_rms_rad=rms(trace['sensor_state'][:,2]),
            true_pitch_error_rms_rad=rms(trace['gt_state'][:,2]),
            torque_rms_nm=rms(trace['motor_substeps'][1:,:,WHEELS]),
            peak_torque_nm=float(abs(trace['motor_substeps'][:,:,WHEELS]).max()),
            residual_rms_total_nm=rms(trace['residual_total_nm'][1:]),
            residual_peak_total_nm=float(abs(trace['residual_total_nm']).max()),
            wheel_saturation_ratio=float(np.mean(abs(trace['motor_substeps'][1:,:,WHEELS])>=playback.adapter.limit[WHEELS]-1e-6)),
            odometry_gt_path_error_rms_m=rms(trace['synchronized_state'][:,0]-trace['gt_state'][:,0]),
            audit=dict(leg_torque_max_error_nm=leg_error, history_max_error=history_error,
                       wheel_sum_max_error_nm=sum_error, online_rls_calls=0), K=fixed.K.tolist() if fixed else None)
        return result
    finally:
        env.close()


def replay_check(result, output):
    label = 'E' if result['label']=='E-original' else 'A'
    reference = next(r for r in map(json.loads,(E_ARCHIVE/'results.jsonl').read_text().splitlines())
                     if r['mode']==label and r['mismatch']=='nominal' and r['seed']==result['seed']
                     and r['pitch_delta_rad']==result['pitch_delta_rad'])
    assert result['completed_s']==reference['completed_s']
    with np.load(output/result['trace']) as a, np.load(E_ARCHIVE/reference['trace']) as b:
        pairs = [('sensor_state','state'),('gt_position','gt_position'),('leg_error','leg_error')]
        errors = {x:float(abs(a[x]-b[y]).max()) for x,y in pairs}
        reference_substeps = b['motor_substeps'][:,:,WHEELS] if label=='E' else b['motor_substeps']
        errors['motor_substeps'] = float(abs(a['motor_substeps'][:,:,WHEELS]-reference_substeps).max())
        assert max(errors.values())==0., errors
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--stage',choices=('e','f1'),required=True)
    parser.add_argument('--alphas',type=float,nargs='+',default=[0.,.1,.25,.5,1.])
    parser.add_argument('--quick',action='store_true')
    args = parser.parse_args()
    output=args.output.resolve()
    if not output.is_relative_to(REPO/'docs/exp') or output.exists():
        parser.error('New output directory under docs/exp/ required')
    if any(not 0.<=a<=1. for a in args.alphas):
        parser.error('Alpha must be between zero and one')
    output.mkdir(parents=True)
    cfg=json.loads((ARCHIVE/'config.json').read_text())
    parameters=json.loads((ARCHIVE/'manifest.json').read_text())['nominal_parameters']
    policy=policy_config()
    source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description=Description(source['scene']['robot']['spawn']['asset_path'])
    write_json(output/'manifest.json',dict(execution_domain='VALIDATION_SIM',evidence_status='NOT_TESTED',
        checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],onnx_sha256=policy['policy_interface']['onnx_sha256'],
        cfg=cfg,parameters=parameters,residual_config=DEFAULT_RESIDUAL,alphas=args.alphas,
        script_sha256=sha256(Path(__file__)),stage=args.stage,actor_sensor_timing='original A cache',
        residual_sensing='synchronized encoders/IMU; ground truth used only for evaluation',
        saturation_order='original adapter clipping, add residual, original Playback final effort clipping',
        online_adaptation=False,quick=args.quick))
    started=time.monotonic()
    for seed in cfg['seeds']:
        for pitch in cfg['pitch_disturbances_rad']:
            if args.quick and (seed!=42 or pitch!=0.):
                continue
            jobs=[('E-original','sensor',0.),('E-sync','synchronized',0.),('E-GT','gt',0.)] if args.stage=='e' else (
                [('A','synchronized',0.)]+[(f'F-1_a{alpha:g}','synchronized',alpha) for alpha in args.alphas])
            reference=None
            for label, state, alpha in jobs:
                r=run(policy,cfg,description,parameters,seed,pitch,label,state,output,alpha)
                if label in ('A','E-original') or label=='F-1_a0':
                    r['archive_replay_errors']=replay_check(r,output)
                if reference is None:
                    reference=r
                else:
                    np.testing.assert_array_equal(r['initial_physics'],reference['initial_physics'])
                with (output/'results.jsonl').open('a') as stream:
                    stream.write(json.dumps(r,allow_nan=False)+'\n')
                print(f'[VALIDATION_SIM] {label} s{seed} p{pitch:+.3f}: {r["evidence_status"]} '
                      f't={r["completed_s"]:.2f} drift={r["max_displacement_m"]:.4f} '
                      f'pitchRMS={r["pitch_rms_rad"]:.4f} wheelRMS={r["torque_rms_nm"]:.4f} '
                      f'{r["failures"]} elapsed={time.monotonic()-started:.1f}s',flush=True)
    write_json(output/'completion.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',elapsed_s=time.monotonic()-started))


if __name__=='__main__':
    main()
