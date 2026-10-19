"""TRAINING_SIM (configuration only): diff the *current* task config against a checkpoint's env.yaml.

Reproduces the FlashSAC train.py config path without creating an environment:
``parse_env_cfg(task)`` -> ``cfg.seed`` -> ``runner_cfg.apply_env_cfg(cfg)`` -> ``dump_yaml``.
Then compares it leaf-by-leaf with the training-time ``env.yaml`` of a run directory and
reports the FlashSAC runner fields that define the deployed action mapping.

Usage (Isaac Lab Python):
    /home/cocel/isaac/env_isaaclab/bin/python test/diff_flash_env_cfg_vs_checkpoint.py \
        --run lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848 --output <dir>
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def yaml_loader():
    import yaml

    class Loader(yaml.SafeLoader):
        pass

    Loader.add_constructor('tag:yaml.org,2002:python/tuple', lambda l, n: tuple(l.construct_sequence(n)))
    Loader.add_constructor('tag:yaml.org,2002:python/object/apply:builtins.slice',
                           lambda l, n: ('slice', *l.construct_sequence(n)))
    return Loader


def flatten(value, prefix=''):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from flatten(item, f'{prefix}.{key}' if prefix else str(key))
    elif isinstance(value, (list, tuple)) and value and all(isinstance(v, dict) for v in value):
        for index, item in enumerate(value):
            yield from flatten(item, f'{prefix}[{index}]')
    else:
        yield prefix, value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--task', default='DDT-Velocity-Flat-Tita-My-v0')
    parser.add_argument('--run', type=Path, required=True, help='training run directory with env.yaml')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--num-envs', type=int, default=4096)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    import sys
    sys.path.insert(0, str(REPO / 'lab/ddt_lab/scripts/flash_sac'))
    from runtime import setup_imports  # same import path setup as scripts/flash_sac/train.py

    setup_imports(False)
    from isaaclab.app import AppLauncher

    app = AppLauncher(headless=True, device='cpu').app
    try:
        import yaml
        import ddt_lab.tasks  # noqa: F401 -- registers the task
        from isaaclab_tasks.utils import load_cfg_from_registry, parse_env_cfg
        from isaaclab.utils.io import dump_yaml

        runner_cfg = load_cfg_from_registry(args.task, 'flash_sac_cfg_entry_point')
        cfg = parse_env_cfg(args.task, device='cpu', num_envs=args.num_envs)
        cfg.seed = args.seed
        runner_cfg.apply_env_cfg(cfg)
        current_path = args.output / 'current_env.yaml'
        dump_yaml(str(current_path), cfg)

        loader = yaml_loader()
        old = dict(flatten(yaml.load((args.run / 'env.yaml').read_text(), Loader=loader)))
        new = dict(flatten(yaml.load(current_path.read_text(), Loader=loader)))
        ignore = ('.goal_vel_visualizer_cfg.', '.current_vel_visualizer_cfg.', 'log_dir', 'sim.device')
        changed = {k: [old[k], new[k]] for k in sorted(old.keys() & new.keys())
                   if old[k] != new[k] and not any(i in k for i in ignore)}
        removed = sorted(k for k in old.keys() - new.keys() if not any(i in k for i in ignore))
        added = sorted(k for k in new.keys() - old.keys() if not any(i in k for i in ignore))

        runner = {name: getattr(runner_cfg, name) for name in dir(runner_cfg)
                  if not name.startswith('_') and not callable(getattr(runner_cfg, name))}
        agent_meta = json.loads((args.run / 'agent.json').read_text())
        mapping = json.loads((args.run / 'action_mapping.json').read_text())
        runner_mapping = {k: list(runner[k]) for k in ('action_gain_negative', 'action_gain_positive') if k in runner}
        mapping_equal = all(
            all(abs(a - b) < 1e-6 for a, b in zip(runner_mapping[k], mapping[k])) for k in runner_mapping)

        report = dict(execution_domain='TRAINING_SIM (config only; no env created)', task=args.task,
                      run=str(args.run), changed=changed, removed=removed, added=added,
                      runner_action_gains=runner_mapping, checkpoint_action_mapping=mapping,
                      action_gains_equal=mapping_equal, checkpoint_agent=agent_meta)
        (args.output / 'env_cfg_diff.json').write_text(json.dumps(report, indent=2, default=str) + '\n')
        print(f'[TRAINING_SIM] leaves: old={len(old)} new={len(new)} changed={len(changed)} '
              f'removed={len(removed)} added={len(added)} action_gains_equal={mapping_equal}')
        for key, (a, b) in changed.items():
            print(f'  CHANGED {key}: {a!r} -> {b!r}')
        for key in removed:
            print(f'  REMOVED {key}: {old[key]!r}')
        for key in added:
            print(f'  ADDED   {key}: {new[key]!r}')
    except Exception:
        # SimulationApp.close() ends the process, so report the failure before closing.
        import traceback
        traceback.print_exc()
        raise
    finally:
        import sys
        sys.stdout.flush()
        sys.stderr.flush()
        app.close()


if __name__ == '__main__':
    main()
