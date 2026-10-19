"""VALIDATION_SIM: replay the 0809 student with its original 808 observation contract."""
import os
from pathlib import Path
import sys

REPO = Path('/home/cocel/Desktop/Research/isaaclab_add_reward_autotuning')
RUN = REPO / 'logs/co_rl/Tita_Flat_Stand_Drive-v3-mooppo/mooppo/2026-08-09_15-40-20'
os.chdir(REPO)
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / 'scripts/co_rl'))
sys.argv[1:1] = [
    '--task', 'Isaac-Velocity-Flat-Tita-RMAStudent-TargetHeight-v3-moo-ppo',
    '--algo', 'mooppo', '--checkpoint', str(RUN / 'model_999.pt'),
    '--num_policy_stacks', '1', '--num_critic_stacks', '0',
]
from scripts.co_rl import play
import gymnasium as gym
import yaml

saved = yaml.safe_load((RUN / 'params/agent.yaml').read_text())
student = gym.spec('Isaac-Velocity-Flat-Tita-RMAStudent-TargetHeight-v3-moo-ppo')
teacher = gym.spec('Isaac-Velocity-Flat-Tita-RMATeacher808-TargetHeight-v3-moo-ppo')
student.kwargs['env_cfg_entry_point'] = teacher.kwargs['env_cfg_entry_point']
original_agent = student.kwargs['co_rl_cfg_entry_point']


def restored_agent():
    cfg = original_agent()
    cfg.num_policy_stacks = saved['num_policy_stacks']
    cfg.num_critic_stacks = saved['num_critic_stacks']
    cfg.policy.teacher_checkpoint_path = str(REPO / saved['policy']['teacher_checkpoint_path'])
    return cfg


student.kwargs['co_rl_cfg_entry_point'] = restored_agent
# Playback should preserve previously exported model files.
for name in ('export_policy_as_jit', 'export_policy_as_onnx', 'export_student_onnx'):
    setattr(play, name, lambda *args, **kwargs: None)
print('[0809 PLAY] Restored 68D observation, 25D privileged input, 50-frame adaptation history.', flush=True)
try:
    play.main()
finally:
    play.simulation_app.close()
