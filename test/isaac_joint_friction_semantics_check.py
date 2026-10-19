"""TRAINING_SIM (simulator unit check): what does Isaac Lab joint ``friction`` mean on this install?

The local Isaac Lab v2.3.0 docstring calls actuator ``friction`` a *unitless* coefficient
(F_resist <= mu * F_spatial), while Isaac Sim >= 5 writes PhysX DOF friction properties
[static, dynamic, viscous]. This check distinguishes the two readings without guessing:

- TITA from the training task config, root link fixed, gravity off, no ground contact, so the
  transmitted spatial force through a wheel joint is close to zero.
- Legs keep the training PD (holding the default pose); wheels get zero damping and a constant
  feed-forward effort tau.
- Per env, wheel static=dynamic friction mu (viscous 0). The wheel angular acceleration gives the
  net torque; the friction torque is tau - I_eff * alpha, with I_eff calibrated from mu = 0.

If friction acts as an effort threshold in N m, wheels with tau < mu stay still. If it scales with
the transmitted spatial force, all wheels accelerate almost like mu = 0 in this unloaded test.
Also reports joint armature and the wheel body inertia seen by PhysX (MuJoCo uses armature 0.01).
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TASK = 'DDT-Velocity-Flat-Tita-My-v0'
MUS = [0.0, 1.0, 2.0]
TAUS = [0.5, 1.5, 3.0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--steps', type=int, default=20, help='physics steps at 5 ms (default 0.1 s)')
    parser.add_argument('--alpha-steps', type=int, default=4, help='steps used for the early acceleration estimate')
    parser.add_argument('--settle-steps', type=int, default=20, help='zero-effort steps after writing the default pose')
    parser.add_argument('--gravity', action='store_true',
                        help='enable gravity so each wheel joint transmits the wheel weight (load-dependence check)')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    sys.path.insert(0, str(REPO / 'lab/ddt_lab/scripts/flash_sac'))
    from runtime import setup_imports
    setup_imports(False)
    from isaaclab.app import AppLauncher

    app = AppLauncher(headless=True, device='cpu').app
    try:
        import torch
        import isaaclab.sim as sim_utils
        from isaaclab.scene import InteractiveScene, InteractiveSceneCfg
        from isaaclab.utils import configclass
        import ddt_lab.tasks  # noqa: F401
        from isaaclab_tasks.utils import parse_env_cfg

        cases = list(itertools.product(MUS, TAUS))
        env_cfg = parse_env_cfg(TASK, device='cpu', num_envs=len(cases))
        robot_cfg = env_cfg.scene.robot.replace(prim_path='{ENV_REGEX_NS}/Robot')
        robot_cfg.spawn.articulation_props.fix_root_link = True
        wheels = robot_cfg.actuators['wheels']
        wheels.damping = 0.0
        wheels.min_delay = wheels.max_delay = 0
        legs = robot_cfg.actuators['legs']
        legs.min_delay = legs.max_delay = 0

        @configclass
        class SceneCfg(InteractiveSceneCfg):
            robot = robot_cfg

        dt = 0.005
        gravity = (0.0, 0.0, -9.81) if args.gravity else (0.0, 0.0, 0.0)
        sim = sim_utils.SimulationContext(sim_utils.SimulationCfg(dt=dt, device='cpu', gravity=gravity))
        scene = InteractiveScene(SceneCfg(num_envs=len(cases), env_spacing=2.0))
        sim.reset()
        robot = scene['robot']
        wheel_ids = robot.find_joints('.*_leg_4')[0]
        n, j = len(cases), robot.num_joints

        static = torch.zeros(n, j)
        for e, (mu, _) in enumerate(cases):
            static[e, wheel_ids] = mu
        robot.write_joint_friction_coefficient_to_sim(static, joint_dynamic_friction_coeff=static.clone(),
                                                      joint_viscous_friction_coeff=torch.zeros(n, j))
        props = robot.root_physx_view.get_dof_friction_properties().clone()  # [static, dynamic, viscous]
        armature = robot.root_physx_view.get_dof_armatures().clone()
        inertias = robot.root_physx_view.get_inertias().clone()
        body_names = robot.body_names

        # sim.reset() leaves the USD joint positions (all zero, knee outside its range); write the
        # training default pose explicitly and settle with zero wheel effort before the test.
        robot.write_joint_state_to_sim(robot.data.default_joint_pos.clone(), torch.zeros(n, j))
        robot.reset()
        robot.set_joint_position_target(robot.data.default_joint_pos.clone())
        robot.set_joint_velocity_target(torch.zeros(n, j))

        def run(efforts, steps):
            series = []
            for _ in range(steps):
                robot.set_joint_effort_target(efforts)
                scene.write_data_to_sim()
                sim.step()
                scene.update(dt)
                series.append(robot.data.joint_vel[:, wheel_ids].mean(1).clone())
            return torch.stack(series)

        settle = run(torch.zeros(n, j), args.settle_steps)
        efforts = torch.zeros(n, j)
        for e, (_, tau) in enumerate(cases):
            efforts[e, wheel_ids] = tau
        start = robot.data.joint_vel[:, wheel_ids].mean(1).clone()
        velocity = run(efforts, args.steps)  # (steps, n)
        # Early-window acceleration (before any joint-speed saturation), relative to the settled start.
        k = args.alpha_steps
        alpha = (velocity[k - 1] - start) / (k * dt)

        reference = {tau: float(alpha[e]) for e, (mu, tau) in enumerate(cases) if mu == 0.0}
        inertia_eff = sum(tau / reference[tau] for tau in TAUS) / len(TAUS)
        rows = []
        for e, (mu, tau) in enumerate(cases):
            net = inertia_eff * float(alpha[e])
            rows.append(dict(mu=mu, tau_nm=tau, wheel_alpha_rad_s2=float(alpha[e]),
                             final_wheel_vel_rad_s=float(velocity[-1, e]), net_torque_nm=net,
                             friction_torque_nm=tau - net, wheel_vel_series=velocity[:, e].tolist()))
        wheel_bodies = [i for i, name in enumerate(body_names) if name.endswith('_leg_4')]
        result = dict(
            execution_domain='TRAINING_SIM (simulator unit check; no policy, no robot)',
            isaac_lab_task=TASK, physics=f'PhysX CPU, dt 5 ms, gravity {gravity}, root fixed, no ground',
            joint_names=robot.joint_names, wheel_joint_ids=[int(i) for i in wheel_ids],
            dof_friction_properties_env0=props[0].tolist(), dof_armature_env0=armature[0].tolist(),
            wheel_body_inertia_env0={body_names[i]: inertias[0, i].tolist() for i in wheel_bodies},
            effective_wheel_inertia_kgm2=inertia_eff, alpha_window_s=args.alpha_steps * dt,
            dof_friction_properties_per_env=[props[e, wheel_ids].tolist() for e in range(n)],
            settle_final_wheel_vel_rad_s=settle[-1].tolist(), cases=rows)
        (args.output / 'friction_semantics.json').write_text(json.dumps(result, indent=2) + '\n')
        print(f'[TRAINING_SIM] armature env0: {armature[0].tolist()}')
        print(f'[TRAINING_SIM] wheel body inertia (Ixx..): {result["wheel_body_inertia_env0"]}')
        print(f'[TRAINING_SIM] effective wheel inertia from mu=0: {inertia_eff:.5f} kg m^2')
        for row in rows:
            print('[TRAINING_SIM] mu={mu:.1f} tau={tau_nm:.1f} N m -> alpha={wheel_alpha_rad_s2:9.2f} rad/s^2 '
                  'final_vel={final_wheel_vel_rad_s:7.3f} rad/s friction_torque={friction_torque_nm:6.3f} N m'.format(**row))
    except Exception:
        import traceback
        traceback.print_exc()
        raise
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
        # SimulationApp.close() hung for >10 min on this machine after the results were written
        # (another Kit process holds the kv database); outputs are already flushed, so exit directly.
        import os
        os._exit(0)


if __name__ == '__main__':
    main()
