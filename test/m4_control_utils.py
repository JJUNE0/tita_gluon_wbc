"""VALIDATION_SIM: original fixed-control rollout with saturation-aware recording.

The former collector asserted actual residual == requested even at wheel effort
limits. Under severe lag that aborts before recording the physical outcome.
Control equations and all success thresholds are unchanged; only the recording
assertion changes. Incomplete episodes retain their failure and full-horizon
statistics remain None.
"""
import numpy as np
from flash_overnight_control_stages import physical_paths
from flash_overnight_model_stages import KEYS, BIAS, current, limited, rms


def rollout_control(r,group,gain,duration,pre,p_target,amplitude=0.,ramp_bias=False):
    states,steps,extra_rows,raw_rows,support = [],[],[],[],[]
    previous = 0.;total_previous = 0. if ramp_bias else BIAS
    f1 = None
    if group=='F1':
        from sim2sim_ros2_jazzy.residual_wheel_pd import ResidualWheelPD
        f1 = ResidualWheelPD(r.env);f1.update(np.zeros(3));f1.position=r.observation['sensor'][0]-p_target
        f1.age=f1.u=0.
    count = round(duration/.02)
    for i in range(count+1):
        states.append({k:r.observation[k].copy() for k in KEYS})
        failure = r.failures()
        if failure or i==count:break
        z = current(r);z[0]-=p_target
        if gain is not None:
            ix = gain['indices'];error=z[ix]-gain['reference']
            raw = float(-np.asarray(gain['K'])@error)
            extra = limited(raw,previous,i*.02)
            low,high = np.asarray(gain['low']),np.asarray(gain['high'])
            support.append(bool(np.all(z[ix][1:]>=low[1:]-1e-8) and np.all(z[ix][1:]<=high[1:]+1e-8)))
        else:raw=extra=0.;support.append(True)
        if group=='F1':
            f1.update(np.zeros(3));raw=extra=float(f1.u)
        previous = extra
        target = 0. if group=='A' else (extra if group=='F1' else BIAS+extra)
        total = float(np.clip(target,total_previous-.04,total_previous+.04)) if ramp_bias else target
        total_previous = total
        transition = r.step(total)
        # Saturation changes the actual additive input; record it instead of aborting.
        assert abs(transition['actual_u']) <= abs(total)+1e-6
        assert np.max(abs(transition['motor'][:,[3,7]])) <= 12.000001
        if gain is not None:assert abs(extra)<=.050000001
        raw_rows.append(raw);extra_rows.append(extra);steps.append(transition)
    trace = {k:np.asarray([s[k] for s in states]) for k in KEYS}
    if steps:trace.update({k:np.asarray([s[k] for s in steps]) for k in steps[0]})
    trace.update(raw_correction=np.asarray(raw_rows),correction=np.asarray(extra_rows),
        hidden_inside_train_range=np.asarray(support))
    if steps:
        np.testing.assert_array_equal(trace['previous_action'][:-1],trace['history'])
        np.testing.assert_array_equal(trace['previous_action'][1:],trace['action'])
    base,axle = physical_paths(trace,pre)
    trace.update(base_path=base,axle_path=axle)
    t=np.arange(len(base))*.02;tail=(t>=duration-5.)&(t<duration)
    target = -amplitude
    base_error=base-target;axle_error=axle-target
    motor = trace.get('physical_motor',trace.get('motor'))
    def error_metrics(error):
        return dict(IAE=float(np.trapz(abs(error),t)),last5_RMSE=float(rms(error[tail],0)) if tail.any() else None,
            max_error=float(max(abs(error))))
    stats = dict(complete=not failure and len(states)==count+1,failure=failure,duration_s=float(t[-1]),
        base=error_metrics(base_error),wheel_midpoint=error_metrics(axle_error),
        last5_base_speed_mean=float(trace['base_velocity'][tail].mean()) if tail.any() else None,
        last5_base_speed_RMS=float(rms(trace['base_velocity'][tail],None)) if tail.any() else None,
        last5_base_position_range=float(np.ptp(base[tail])) if tail.any() else None,
        max_planar_drift=float(max(np.linalg.norm(trace['base_position'][:,:2]-pre['base_position'][:2],axis=1))),
        pitch_RMS=float(rms(trace['sensor'][:,2]-(gain['reference'][2] if gain is not None else pre['pitch']),0)),
        wheel_torque_RMS=float(rms(motor[:,:,[3,7]],None)) if motor is not None else 0.,
        hidden_train_fraction=float(np.mean(support)) if support else 0.,
        correction_peak=float(max(abs(trace['correction']))) if len(steps) else 0.)
    return trace,stats
