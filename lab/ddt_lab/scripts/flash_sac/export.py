"""VALIDATION_SIM: Export a TITA FlashSAC checkpoint for the shared MuJoCo runner."""

import argparse
import json
from pathlib import Path

from runtime import REPO_ROOT, action_mapping_kwargs, setup_imports

setup_imports(False)
import torch
from flash_rl.agents.flashSAC.network import FlashSACActor


class NativeActionPolicy(torch.nn.Module):
    """Deterministic actor with checkpoint gains embedded in native-order output."""

    def __init__(self, actor, gains):
        super().__init__()
        self.actor = actor
        for name, values in gains.items():
            self.register_buffer(name, torch.tensor(values, dtype=torch.float32))

    def forward(self, observations):
        x = self.actor.embedder(observations, training=False)
        for block in self.actor.encoder:
            x = block(x, training=False)
        # Equivalent to UnitRMSNorm, expressed with portable ONNX operations.
        norm = self.actor.post_norm
        x = x * torch.rsqrt(x.square().mean(dim=-1, keepdim=True) + norm.eps) * norm.weight
        mean = torch.nn.functional.linear(x, self.actor.predictor.mean_w.w.weight, self.actor.predictor.mean_bias)
        normalized = mean.tanh()
        return normalized * torch.where(normalized >= 0, self.action_gain_positive, self.action_gain_negative)


def load_policy(path, metadata):
    if metadata['action_dim'] != 8 or metadata['actor_obs_dim'] not in (33, 34, 35):
        raise ValueError('This export supports 33/34/35-observation, 8-action TITA actors; the saved layout is validated separately')
    cfg = metadata['agent']
    actor = FlashSACActor(cfg['actor_num_blocks'], metadata['actor_obs_dim'], cfg['actor_hidden_dim'], 8)
    state = torch.load(path / 'actor.pt', map_location='cpu', weights_only=True)['network_state_dict']
    while state and all(name.startswith('_orig_mod.') for name in state):
        torch.nn.modules.utils.consume_prefix_in_state_dict_if_present(state, '_orig_mod.')
    actor.load_state_dict(state)
    return NativeActionPolicy(actor.eval(), action_mapping_kwargs(metadata)).eval()


def main():
    """Use the shared TITA checkpoint exporter without a per-policy YAML."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--validation_python', type=Path, default=Path.home() / 'venvs/cosim_ros2_jazzy/bin/python')
    args = parser.parse_args()
    import sys
    sys.path.insert(0, str(REPO_ROOT / 'sim2sim/sim2sim_ros2_jazzy'))
    from sim2sim_ros2_jazzy.checkpoint import prepare_checkpoint
    from sim2sim_ros2_jazzy.cli import record
    config = prepare_checkpoint(args.checkpoint, args.validation_python)
    record(json.loads((config.parent / 'manifest.json').read_text()), 'policy_export')
    print(f'[VALIDATION_SIM] Verified config: {config}', flush=True)


if __name__ == '__main__':
    main()
