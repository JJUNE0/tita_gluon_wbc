# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Play / evaluate a checkpoint trained with plain RSL-RL PPO.

Mirrors ``scripts/np3o/play.py``'s CLI surface (``--task --checkpoint
--num_envs --export_policy --export_dir``), but loads via
``rsl_rl.runners.OnPolicyRunner`` instead of NP3O's ``OnConstraintPolicyRunner``.

ONNX export uses a custom two-input adapter (``TwoInputAdapter`` below) so the
exported interface stays byte-identical to the deployed
``nn_input0 [1,33]`` / ``nn_input1 [1,10,33]`` / ``nn_output [1,8]`` format --
``cosim_ros2_jazzy`` needs zero changes to consume it.

IMPORTANT layout note (see ``MyTitaFlatV7RslRlEnvCfg`` docstring in
``my_flat_env_cfg.py`` for the full derivation, empirically verified against
IsaacLab's own ``flatten_history_dim=True`` output with max abs error 0.0):
the RSL-RL actor was trained on IsaacLab's *term-major* flattened observation
--  ``[ang_vel(3*10) | gravity(3*10) | commands(3*10) | joint_pos(8*10) |
joint_vel(8*10) | actions(8*10)]``, each term's own block internally ordered
oldest-timestep-first -- NOT a naive frame-major reshape of ``nn_input1``
(``[frame0(33), frame1(33), ..., frame9(33)]``). ``TwoInputAdapter`` reproduces
the term-major layout explicitly from ``nn_input1``.
"""

import argparse
import importlib
import os

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description='Play a checkpoint trained with plain RSL-RL PPO.')
parser.add_argument('--task', type=str, required=True, help='Gym task ID.')
parser.add_argument('--num_envs', type=int, default=50, help='Number of envs for playback.')
parser.add_argument('--checkpoint', type=str, default=None, help='Absolute checkpoint path (overrides auto-resolve).')
parser.add_argument('--load_run', type=str, default='.*', help='Run dir regex when --checkpoint is omitted.')
parser.add_argument('--load_checkpoint', type=str, default=r'model_.*\.pt', help='Checkpoint filename regex.')
parser.add_argument(
    '--export_policy', action='store_true',
    help='Export the loaded policy as TorchScript + ONNX (two-input adapter) and exit.',
)
parser.add_argument(
    '--export_dir', type=str, default=None,
    help='Override export directory (defaults to <checkpoint_dir>/exported).',
)
AppLauncher.add_app_launcher_args(parser)
args_cli, _ = parser.parse_known_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import ddt_lab.tasks  # noqa: F401  -- registers tasks
import gymnasium as gym
import torch
from isaaclab_tasks.utils import get_checkpoint_path

from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper
from rsl_rl.runners import OnPolicyRunner

# Inject the learned base_lin_vel estimator classes into on_policy_runner's
# eval() namespace so EstimatorActorCriticCfg/EstimatorPPOCfg's class_name
# strings resolve, with zero changes to the installed rsl_rl package. See
# docs/plan_base_vel_estimator_ppo.md.
import rsl_rl.runners.on_policy_runner as _opr
from ddt_lab.algorithms.estimator import ActorCriticWithEstimator, PPOWithEstimator

_opr.ActorCriticWithEstimator = ActorCriticWithEstimator
_opr.PPOWithEstimator = PPOWithEstimator

# per-term (name, dim) boundaries within the 33-dim proprio vector, in the
# exact order declared in ObservationsCfg.PolicyCfg (rough_env_cfg.py) --
# empirically confirmed against IsaacLab's own flatten_history_dim=True output.
_TERM_DIMS = [
    ("base_ang_vel", 3), ("projected_gravity", 3), ("velocity_commands", 3),
    ("joint_pos", 8), ("joint_vel", 8), ("actions", 8),
]


class TwoInputAdapter(torch.nn.Module):
    """Wraps a trained RSL-RL actor to accept the deployed two-input interface.

    ``nn_input0 [B,33]`` is accepted but unused (kept only for interface
    parity with the NP3O-exported ONNX); ``nn_input1 [B,10,33]`` is
    reassembled into the term-major ``[B,330]`` layout the actor was actually
    trained on, then normalized + forwarded through the actor MLP.
    """

    def __init__(self, actor: torch.nn.Module, normalizer: torch.nn.Module):
        super().__init__()
        self.actor = actor
        self.normalizer = normalizer

    def forward(self, nn_input0: torch.Tensor, nn_input1: torch.Tensor) -> torch.Tensor:
        b, t, _ = nn_input1.shape
        offset = 0
        chunks = []
        for _name, dim in _TERM_DIMS:
            chunk = nn_input1[:, :, offset:offset + dim]  # (B, T, dim)
            chunks.append(chunk.reshape(b, t * dim))
            offset += dim
        flat = torch.cat(chunks, dim=-1)  # (B, 330), term-major
        # nn_input0 is redundant (its content is already the last slot of
        # nn_input1 for every term) -- but must stay a real ONNX graph input
        # for interface parity with the NP3O-exported policy.onnx, which
        # cosim_ros2_jazzy always feeds both tensors to. A zero-weighted but
        # non-eliminable dependency keeps it from being pruned as dead code.
        flat = flat + 0.0 * nn_input0.sum()
        flat = self.normalizer(flat)
        return self.actor(flat)


class SingleInputAdapter(torch.nn.Module):
    """For no-history policies (e.g. My16, ``history_length=0``): the raw obs
    IS already the flat vector the actor wants -- no term-major reconstruction
    needed. Exported with a single ``nn_input0`` input (no ``nn_input1`` at
    all); ``cosim_ros2_jazzy``'s ``policy_runner.py`` supports this via
    ``history_len=0`` in the deployment config.
    """

    def __init__(self, actor: torch.nn.Module, normalizer: torch.nn.Module):
        super().__init__()
        self.actor = actor
        self.normalizer = normalizer

    def forward(self, nn_input0: torch.Tensor) -> torch.Tensor:
        return self.actor(self.normalizer(nn_input0))


class EstimatorAdapter(torch.nn.Module):
    """For `My26`-style checkpoints (``ActorCriticWithEstimator``): the
    estimator MLP is baked into the exported graph so the deployed interface
    stays a single raw-proprio ``nn_input0`` -- ``cosim_ros2_jazzy``'s
    ``obs_builder`` needs zero changes (see
    ``docs/plan_base_vel_estimator_ppo.md``). No separate estimator output is
    exposed.
    """

    def __init__(
        self,
        estimator: torch.nn.Module,
        estimator_normalizer: torch.nn.Module,
        actor: torch.nn.Module,
        actor_normalizer: torch.nn.Module,
    ):
        super().__init__()
        self.estimator = estimator
        self.estimator_normalizer = estimator_normalizer
        self.actor = actor
        self.actor_normalizer = actor_normalizer

    def forward(self, nn_input0: torch.Tensor) -> torch.Tensor:
        proprio = nn_input0
        est_out = self.estimator(self.estimator_normalizer(proprio))
        actor_in = torch.cat([est_out, proprio], dim=-1)
        return self.actor(self.actor_normalizer(actor_in))


class EstimatorAdapterDebug(EstimatorAdapter):
    """Diagnostic-only variant of `EstimatorAdapter` exposing the estimator's
    raw (scaled) `base_lin_vel` prediction as a second output, alongside the
    action -- for `scripts/rsl_rl/eval_estimator_accuracy_mujoco.py` /
    `cosim_ros2_jazzy`-side accuracy probes. Not used for deployment (the
    deployed graph is the single-output `EstimatorAdapter` export) --
    `cosim_ros2_jazzy`'s `PolicyRunner` is a strict single-output runner.
    """

    def forward(self, nn_input0: torch.Tensor):
        proprio = nn_input0
        est_out = self.estimator(self.estimator_normalizer(proprio))
        actor_in = torch.cat([est_out, proprio], dim=-1)
        action = self.actor(self.actor_normalizer(actor_in))
        return action, est_out


def _resolve_agent_cfg(entry_point: str):
    module_name, attr = entry_point.split(':')
    obj = getattr(importlib.import_module(module_name), attr)
    return obj() if callable(obj) else obj


def main():
    spec = gym.spec(args_cli.task)
    agent_cfg = _resolve_agent_cfg(spec.kwargs['rsl_rl_cfg_entry_point'])
    env_cfg_entry = spec.kwargs['env_cfg_entry_point']
    env_cfg = env_cfg_entry() if callable(env_cfg_entry) else env_cfg_entry
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device

    env = gym.make(args_cli.task, cfg=env_cfg)
    env = RslRlVecEnvWrapper(env, clip_actions=agent_cfg.clip_actions)

    runner = OnPolicyRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)

    if args_cli.checkpoint is not None:
        ckpt = args_cli.checkpoint
    else:
        log_root = os.path.abspath(os.path.join('logs', 'rsl_rl', agent_cfg.experiment_name))
        ckpt = get_checkpoint_path(log_root, args_cli.load_run, args_cli.load_checkpoint)
    print(f'[INFO] loading checkpoint: {ckpt}')
    runner.load(ckpt)

    policy_nn = runner.alg.policy
    normalizer = getattr(policy_nn, 'actor_obs_normalizer', torch.nn.Identity())

    export_dir = args_cli.export_dir or os.path.join(os.path.dirname(ckpt), 'exported')
    os.makedirs(export_dir, exist_ok=True)

    device = args_cli.device or 'cuda:0'
    history_length = int(getattr(env_cfg.observations.policy, 'history_length', 0) or 0)
    onnx_path = os.path.join(export_dir, 'policy.onnx')
    jit_path = os.path.join(export_dir, 'policy.pt')

    if hasattr(policy_nn, 'estimator'):
        # My26-style ActorCriticWithEstimator checkpoint -- estimator obs_dim
        # read from its own input layer (pure proprio, no base_lin_vel term).
        obs_dim = policy_nn.estimator[0].in_features
        estimator_normalizer = getattr(policy_nn, 'estimator_normalizer', torch.nn.Identity())
        adapter = EstimatorAdapter(policy_nn.estimator, estimator_normalizer, policy_nn.actor, normalizer).to(device)
        adapter.eval()
        example_inputs = (torch.zeros(1, obs_dim, device=device),)
        input_names = ['nn_input0']
    elif history_length > 0:
        adapter = TwoInputAdapter(policy_nn.actor, normalizer).to(device)
        adapter.eval()
        example_inputs = (torch.zeros(1, 33, device=device), torch.zeros(1, history_length, 33, device=device))
        input_names = ['nn_input0', 'nn_input1']
    else:
        # single-frame obs (no history) -- obs_dim read from the actor's own
        # input layer rather than hardcoded, since it varies (36 for My16's
        # 33 + base_lin_vel(3), etc).
        obs_dim = policy_nn.actor[0].in_features
        adapter = SingleInputAdapter(policy_nn.actor, normalizer).to(device)
        adapter.eval()
        example_inputs = (torch.zeros(1, obs_dim, device=device),)
        input_names = ['nn_input0']

    torch.onnx.export(
        adapter,
        example_inputs,
        onnx_path,
        input_names=input_names,
        output_names=['nn_output'],
        opset_version=13,
    )
    print(f'[INFO] saved ONNX policy to {onnx_path}')

    traced = torch.jit.trace(adapter, example_inputs)
    traced.save(jit_path)
    print(f'[INFO] saved TorchScript policy to {jit_path}')

    if hasattr(policy_nn, 'estimator'):
        debug_adapter = EstimatorAdapterDebug(
            policy_nn.estimator, estimator_normalizer, policy_nn.actor, normalizer
        ).to(device)
        debug_adapter.eval()
        debug_onnx_path = os.path.join(export_dir, 'policy_debug.onnx')
        torch.onnx.export(
            debug_adapter,
            example_inputs,
            debug_onnx_path,
            input_names=input_names,
            output_names=['nn_output', 'est_vel'],
            opset_version=13,
        )
        print(f'[INFO] saved debug (action + est_vel) ONNX to {debug_onnx_path}')

    if args_cli.export_policy:
        env.close()
        return

    policy = runner.get_inference_policy(device=device)
    obs = env.get_observations()
    while simulation_app.is_running():
        with torch.inference_mode():
            actions = policy(obs)
            obs, _, _, _ = env.step(actions)
    env.close()


if __name__ == '__main__':
    main()
    simulation_app.close()
