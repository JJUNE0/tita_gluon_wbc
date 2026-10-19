"""DESKTOP_DRY_RUN: source actor -> installed bundle identity and inference parity."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
root = Path(__file__).resolve().parents[2]
checkpoint=root/'lab/ddt_lab/logs/flash_sac/tita_flash_sac_201940_278440/model_80000'
bundle=root/'sim2real/tita_ws/src/tita_controller/policies/flashsac_80000'
parser=argparse.ArgumentParser();parser.add_argument('mode', choices=['reference','onnx']);parser.add_argument('--fixture',type=Path,required=True);args=parser.parse_args()
if args.mode=='reference':
    sys.path.insert(0,str(root/'lab/ddt_lab/scripts/flash_sac'))
    import torch
    from export import NativeActionPolicy, FlashSACActor
    from runtime import action_mapping_kwargs
    metadata=json.loads((checkpoint/'ddt.json').read_text())
    # The source run is BaseComShift; export.load_policy's DEFAULT_TASK follows
    # the current training config, which may now select another task. Rebuild
    # exactly the saved architecture without relabelling the source task.
    assert metadata['task']=='DDT-Velocity-Flat-Tita-My-BaseComShift-v0'
    assert (metadata['actor_obs_dim'],metadata['action_dim'])==(33,8)
    saved=metadata['agent']
    actor=FlashSACActor(saved['actor_num_blocks'],33,saved['actor_hidden_dim'],8)
    state=torch.load(checkpoint/'actor.pt',map_location='cpu',weights_only=True)['network_state_dict']
    while state and all(k.startswith('_orig_mod.') for k in state):
        torch.nn.modules.utils.consume_prefix_in_state_dict_if_present(state,'_orig_mod.')
    actor.load_state_dict(state)
    policy=NativeActionPolicy(actor.eval(),action_mapping_kwargs(metadata)).eval()
    torch.set_num_threads(2)
    sample=torch.randn(256,33,generator=torch.Generator().manual_seed(80000))*2
    with torch.inference_mode(): action=policy(sample)
    np.savez(args.fixture,observations=sample.numpy(),actions=action.numpy())
    print('PASS DESKTOP_DRY_RUN source checkpoint loaded; 256 reference actions saved')
else:
    import onnxruntime as ort
    data=np.load(args.fixture)
    cfg=json.loads((bundle/'config.json').read_text())
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    assert sha(checkpoint/'actor.pt')==cfg['policy_interface']['checkpoint_sha256']
    assert sha(bundle/'policy.onnx')==cfg['policy_interface']['onnx_sha256']
    session=ort.InferenceSession(str(bundle/'policy.onnx'),providers=['CPUExecutionProvider'])
    actual=np.concatenate([session.run(None,{session.get_inputs()[0].name:x[None]})[0]
                           for x in data['observations']],axis=0)
    error=float(abs(actual-data['actions']).max())
    np.testing.assert_allclose(actual,data['actions'],atol=1e-5,rtol=1e-4)
    print(f'PASS DESKTOP_DRY_RUN actor/ONNX SHA identity, 256 samples, max action error {error:.9g}; obs33/action8, frozen inference')
