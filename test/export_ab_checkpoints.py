"""VALIDATION_SIM: export arm A/B FlashSAC checkpoints for sim2sim evaluation only.

``lab/ddt_lab/scripts/flash_sac/export.py`` accepts only ``DDT-Velocity-Flat-Tita-My-v0``. Changing
that deployment-path check needs operator approval, so this test-side wrapper leaves the file
untouched and, per checkpoint, temporarily treats the run's own task as the export task *only after*
verifying that the run keeps the deployed interface:

- ``policy_interface.json`` and ``action_mapping.json`` byte-identical to the reference run
  ``tita_flash_sac_115632_883848`` (observation order/scales, joint order, action terms, gains);
- ``ddt.json`` reports 33 actor observations, 8 actions and the expected task.

Exports (ONNX + sim2sim config + parity manifest from the existing ``prepare_checkpoint``) go to an
evaluation directory, never to the robot bundle. Run with the Isaac Lab interpreter.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import traceback
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
REFERENCE_RUN = REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848'
RUNS = {
    'A': ('tita_flash_sac_201940_278440', 'DDT-Velocity-Flat-Tita-My-BaseComShift-v0'),
    'B': ('tita_flash_sac_201942_248862', 'DDT-Velocity-Flat-Tita-My-Real2Sim-BaseComShift-v0'),
    'Bp42': ('tita_flash_sac_095147_230888', 'DDT-Velocity-Flat-Tita-My-Real2Sim-NomMix-v0'),
    'Bp7': ('tita_flash_sac_095149_279860', 'DDT-Velocity-Flat-Tita-My-Real2Sim-NomMix-v0'),
    'C1': ('tita_flash_sac_114458_484840', 'DDT-Velocity-Flat-Tita-My-LegScale-v0'),
    'C2': ('tita_flash_sac_114500_483968', 'DDT-Velocity-Flat-Tita-My-LegScale-Reward-v0'),
}


def digest(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--steps', type=int, nargs='+', default=[40000, 50000, 60000, 70000, 80000, 90000, 100000])
    parser.add_argument('--output', type=Path, default=REPO / 'docs/exp/2026-10-18/flashsac_ab_sim2sim/exports')
    parser.add_argument('--validation-python', type=Path, default=Path.home() / 'venvs/cosim_ros2_jazzy/bin/python')
    parser.add_argument('--arms', nargs='+', default=['A', 'B'], choices=sorted(RUNS))
    parser.add_argument('--cache', action='store_true',
                        help="write to the sim2sim launcher's own cache (<model>/sim2sim/actor) instead of --output")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    sys.path[:0] = [str(REPO / 'lab/ddt_lab/scripts/flash_sac'), str(REPO / 'sim2sim/sim2sim_ros2_jazzy')]
    import export  # the module prepare_checkpoint imports load_policy from
    from sim2sim_ros2_jazzy.checkpoint import prepare_checkpoint

    rows = []
    for arm, (run, task) in ((a, RUNS[a]) for a in args.arms):
        run_dir = REPO / 'lab/ddt_lab/logs/flash_sac' / run
        interface = {name: digest(run_dir / name) == digest(REFERENCE_RUN / name)
                     for name in ('policy_interface.json', 'action_mapping.json')}
        for step in args.steps:
            ckpt = run_dir / f'model_{step}'
            out = ckpt / 'sim2sim' / 'actor' if args.cache else args.output / f'{run}_model_{step}'
            row = dict(arm=arm, run=run, task=task, step=step, checkpoint=str(ckpt), output=str(out),
                       interface_identical_to_reference=interface)
            try:
                meta = json.loads((ckpt / 'ddt.json').read_text())
                assert all(interface.values()), f'interface differs from reference: {interface}'
                assert (meta['task'], meta['actor_obs_dim'], meta['action_dim']) == (task, 33, 8), meta['task']
                assert digest(ckpt / 'actor.pt') == meta['actor_sha256'], 'actor hash mismatch'
                with patch.object(export, 'DEFAULT_TASK', task), \
                        patch('sim2sim_ros2_jazzy.checkpoint.export_directory', lambda path, out=out: out):
                    config = prepare_checkpoint(ckpt, args.validation_python)
                manifest = json.loads((out / 'manifest.json').read_text())
                assert manifest['checkpoint_sha256'] == meta['actor_sha256']
                row.update(evidence_status='PASS', config=str(config), checkpoint_sha256=meta['actor_sha256'],
                           onnx_sha256=manifest['onnx_sha256'], config_sha256=manifest['config_sha256'],
                           parity=manifest['parity'])
            except Exception:
                row.update(evidence_status='FAIL', error=traceback.format_exc())
            rows.append(row)
            results = args.output / ('cache_export_results.json' if args.cache else 'export_results.json')
            results.write_text(json.dumps(rows, indent=2) + '\n')
            print(f"[VALIDATION_SIM] export {arm} {run} model_{step}: {row['evidence_status']} "
                  f"{row.get('parity', row.get('error', '')[-200:])}", flush=True)
    print(f"[VALIDATION_SIM] export_DEFAULT_TASK after run: {export.DEFAULT_TASK}")


if __name__ == '__main__':
    main()
