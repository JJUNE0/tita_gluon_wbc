"""DESKTOP_DRY_RUN: native Torch reference actions for a flashsac_headw0_<step> ARM ONNX check (Isaac Lab Python)."""
import json
from pathlib import Path
import sys

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'lab/ddt_lab/scripts/flash_sac'))
from export import load_policy  # noqa: E402

STEP = int(sys.argv[1]) if len(sys.argv) > 1 else 50000
checkpoint = ROOT / f'lab/ddt_lab/logs/flash_sac/tita_flash_sac_125547_806511/model_{STEP}'
metadata = json.loads((checkpoint / 'ddt.json').read_text())
torch.set_num_threads(2)
samples = torch.randn(256, 35, generator=torch.Generator().manual_seed(31415)) * 2
actor = load_policy(checkpoint, metadata)
with torch.inference_mode():
    means = actor.actor.get_mean_and_std(samples, training=False)[0].tanh()
    native = means * torch.where(means >= 0, actor.action_gain_positive, actor.action_gain_negative)
out = Path(__file__).resolve().parent / f'flashsac_headw0_{STEP}'
out.mkdir(exist_ok=True)
np.savetxt(out / 'obs.txt', samples.numpy(), fmt='%.9g')
np.savetxt(out / 'expected.txt', native.numpy(), fmt='%.9g')
print('fixture', out, samples.shape, native.shape)
