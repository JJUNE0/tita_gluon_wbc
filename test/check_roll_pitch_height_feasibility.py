"""VALIDATION_SIM: nominal double-support IK grid; no policy or robot control."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys

import mujoco
import numpy as np
from scipy.optimize import least_squares

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from mj_lab.flash_sac import runtime
from mj_lab.robots.tita.flat_env_roll_pitch_height_cfg import TitaFlatRollPitchHeightEnvCfg
from mj_lab.robots.tita.robot_cfg import INITIAL_Q, JOINTS, ROBOT_XML, get_spec


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--roll-deg', type=float)
    parser.add_argument('--pitch-deg', type=float)
    parser.add_argument('--height-range', type=float, nargs=2)
    parser.add_argument('--samples-per-axis', type=int, default=3)
    parser.add_argument('--free-width', action='store_true',
                        help='Allow wheel spacing to vary, rather than fixing both wheel Y positions')
    parser.add_argument('--hard-limits', action='store_true',
                        help='Search hard joint limits without enforcing the current PD action envelope')
    parser.add_argument('--pd-equilibrium', action='store_true',
                        help='Constrain PD targets, allowing gravity deflection outside the target envelope')
    args = parser.parse_args()
    if args.hard_limits and args.pd_equilibrium:
        parser.error('--hard-limits and --pd-equilibrium are separate search modes')
    if args.samples_per_axis < 2:
        parser.error('--samples-per-axis must be at least two')
    cfg = TitaFlatRollPitchHeightEnvCfg(1)
    command = cfg.commands['base_pose']
    if args.roll_deg is not None:
        command.roll_range = (-np.radians(args.roll_deg), np.radians(args.roll_deg))
    if args.pitch_deg is not None:
        command.pitch_range = (-np.radians(args.pitch_deg), np.radians(args.pitch_deg))
    if args.height_range is not None:
        command.height_range = tuple(args.height_range)
    model = get_spec().compile()
    data = mujoco.MjData(model)
    indices = [0, 1, 2, 4, 5, 6]
    joints = [model.joint(JOINTS[i]).id for i in indices]
    qids, vids = model.jnt_qposadr[joints], model.jnt_dofadr[joints]
    feet = [model.body(side+'_leg_4').id for side in ('left', 'right')]
    defaults = np.array(INITIAL_Q)[indices]
    gains = np.array(runtime.load_default_runner_cfg().action_gain_positive)[indices]
    bounds = np.c_[defaults-.25*gains, defaults+.25*gains]
    # IK is constrained to the same position-target envelope and hard limits.
    lower = np.maximum(model.jnt_range[joints, 0], bounds[:, 0])
    upper = np.minimum(model.jnt_range[joints, 1], bounds[:, 1])
    if args.hard_limits or args.pd_equilibrium:
        lower, upper = model.jnt_range[joints, 0], model.jnt_range[joints, 1]
    kp = np.array([60., 60., 92.] * 2)
    weight = float(model.body_mass.sum()*9.81)
    results = []
    rng = np.random.default_rng(42)
    for roll, pitch, height in itertools.product(
            np.linspace(*command.roll_range, args.samples_per_axis),
            np.linspace(*command.pitch_range, args.samples_per_axis),
            sorted(set([*np.linspace(*command.height_range, args.samples_per_axis), command.nominal_height]))):
        cr, sr = np.cos(roll/2), np.sin(roll/2)
        cp, sp = np.cos(pitch/2), np.sin(pitch/2)
        data.qpos[:] = model.qpos0
        data.qpos[:3] = [0., 0., height]
        data.qpos[3:7] = [cr*cp, sr*cp, cr*sp, -sr*sp]

        def measure(q):
            data.qpos[qids] = q
            mujoco.mj_forward(model, data)
            return data.xpos[feet].copy(), data.subtree_com[model.body('base_link').id].copy()

        def equilibrium(wheels, com):
            left_fraction = (com[1]-wheels[1, 1])/(wheels[0, 1]-wheels[1, 1])
            forces = weight*np.array([left_fraction, 1.-left_fraction])
            torque = data.qfrc_bias.copy()
            for foot, force in zip(feet, forces):
                jac = np.zeros((3, model.nv))
                mujoco.mj_jac(model, data, jac, None, data.xpos[foot]-[0., 0., .0925], foot)
                torque -= jac.T @ np.array([0., 0., force])
            targets = data.qpos[qids]+torque[vids]/kp
            violation = np.maximum(np.maximum(bounds[:, 0]-targets, targets-bounds[:, 1]), 0.)
            return left_fraction, torque, targets, violation

        def geometry_residual(wheels, com):
            base = np.r_[wheels[:, 2]-.0925, wheels[0, 0]-wheels[1, 0], com[0]-wheels[:, 0].mean()]
            if args.free_width:
                width = wheels[0, 1]-wheels[1, 1]
                return np.r_[base, max(0., com[1]+.02-wheels[0, 1]), max(0., wheels[1, 1]+.02-com[1]),
                             max(0., .35-width), max(0., width-.75)]
            return np.r_[base, wheels[:, 1]-np.array([.2835, -.2835])]

        def residual(q):
            wheels, com = measure(q)
            result = geometry_residual(wheels, com)
            if args.pd_equilibrium:
                _, torque, _, violation = equilibrium(wheels, com)
                result = np.r_[result, violation*.2, np.maximum(np.abs(torque[vids])-60., 0.)*.01]
            return result

        solved = least_squares(residual, np.clip(defaults, lower+1e-8, upper-1e-8),
                               bounds=(lower, upper), max_nfev=300,
                               ftol=1e-12, xtol=1e-12, gtol=1e-12)
        if args.pd_equilibrium and np.max(np.abs(solved.fun)) > 1e-6:
            for initial in [rng.uniform(lower, upper) for _ in range(4)]:
                trial = least_squares(residual, initial, bounds=(lower, upper), max_nfev=500,
                                      ftol=1e-12, xtol=1e-12, gtol=1e-12)
                if np.linalg.norm(trial.fun) < np.linalg.norm(solved.fun):
                    solved = trial
                if np.max(np.abs(solved.fun)) < 1e-6:
                    break
        wheels, com = measure(solved.x)
        left_fraction, torque, required_targets, violation = equilibrium(wheels, com)
        target_violation = violation.max()
        gap = []
        for name in ('base_link', 'left_leg_3', 'right_leg_3'):
            geom = model.geom(name+'_collision').id
            extent = np.abs(data.geom_xmat[geom].reshape(3, 3)[2]) @ model.geom_size[geom]
            gap.append(float(data.geom_xpos[geom, 2]-extent))
        error = float(np.abs(geometry_residual(wheels, com)).max())
        feasible = (error < 1e-4 and 0. < left_fraction < 1. and min(gap) > .01
                    and np.abs(torque[vids]).max() < 60. and (args.hard_limits or target_violation < 1e-4))
        results.append(dict(roll_rad=roll, pitch_rad=pitch, height_m=height,
            kinematic_max_error_m=error, left_load_fraction=float(left_fraction),
            minimum_base_knee_clearance_m=min(gap), max_nominal_leg_torque_Nm=float(np.abs(torque[vids]).max()),
            max_nominal_pd_target_violation_rad=float(target_violation), feasible=bool(feasible),
            wheel_spacing_m=float(wheels[0, 1]-wheels[1, 1]),
            required_pd_targets_rad=required_targets.tolist(),
            joint_positions_rad=solved.x.tolist()))
    passed = sum(row['feasible'] for row in results)
    summary = dict(execution_domain='VALIDATION_SIM', evidence_status='PASS' if passed == len(results) else 'SUSPICIOUS',
        policy_checkpoint_sha256='N/A: nominal static model, no policy',
        robot_xml_sha256=hashlib.sha256(ROBOT_XML.read_bytes()).hexdigest(),
        search_options=vars(args) | {'output': str(args.output)},
        command_ranges_rad_m=dict(roll=list(command.roll_range), pitch=list(command.pitch_range), height=list(command.height_range)),
        detail='Nominal static samples, vertical wheel forces, nominal PD gains. '
               'Not a proof over continuous ranges; excludes DR, friction, dynamic stability and learned tracking.',
        feasible_count=passed, sample_count=len(results), results=results)
    args.output.write_text(json.dumps(summary, indent=2)+'\n')
    print('[VALIDATION_SIM]', summary['evidence_status'], f'{passed}/{len(results)} nominal static samples feasible')


if __name__ == '__main__':
    main()
