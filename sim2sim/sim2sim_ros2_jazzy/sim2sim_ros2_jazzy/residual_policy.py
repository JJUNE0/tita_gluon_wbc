"""VALIDATION_SIM: saved250/500Hz torque residual with residual-only500Hz LPF."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import numpy as np

from .adapter import ObservationBuilder, ObsState, NATIVE_JOINTS, quat_wxyz_to_rotmat, quat_wxyz_to_rpy

REPO = Path(__file__).resolve().parents[3]


def residual_checkpoint(checkpoint):
    path=Path(checkpoint).expanduser().resolve()
    if path.is_dir() and (path/'bundle.json').is_file():
        saved=json.loads((path/'bundle.json').read_text())
        return path/saved['weight_file']
    if path.is_dir() and (path/'latest.json').is_file():
        latest=json.loads((path/'latest.json').read_text())
        selected=Path(latest['checkpoint'])
        if selected.is_absolute():
            return selected
        # Older runs save repo-relative output paths; portable runs can instead
        # save a checkpoint path relative to the run directory itself.
        for candidate in (path/selected, REPO/selected):
            if candidate.is_file():
                return candidate
        raise FileNotFoundError('latest.json checkpoint does not exist: '+str(selected))
    return path/'actor.pt' if path.is_dir() else path


def residual_metadata(checkpoint, teacher_hash):
    checkpoint = residual_checkpoint(checkpoint)
    metadata = json.loads((checkpoint.parent/'residual.json').read_text())
    digest = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    if metadata['teacher_sha256'] != teacher_hash:
        raise ValueError('Residual checkpoint requires its saved frozen Teacher')
    if metadata.get('policy_checkpoint_sha256', digest) != digest:
        raise ValueError('Residual checkpoint hash mismatch')
    history_length = metadata.get('actor_stack', metadata.get('history_length'))
    if (metadata['actor_obs_dim'] != 440 or history_length != 10
            or not isinstance(metadata.get('residual_wheel_latch'), bool)
            or metadata.get('residual_wheel_input_clipped') is not False):
        raise ValueError('Expected saved44x10 unclipped stop residual')
    if metadata.get('residual_mode','torque') != 'torque':
        raise ValueError('Production playback supports torque residuals only; action variants are archived')
    filtering = metadata.get('residual_torque_filter')
    if filtering is not None:
        if not isinstance(filtering, dict):
            raise ValueError('Invalid saved residual torque filter')
        cutoff = filtering.get('cutoff_hz', 0.)
        alpha = filtering.get('alpha', -1.)
        if (filtering.get('kind') != 'one_pole_matched'
                or filtering.get('placement') != 'residual_only' or filtering.get('update_hz') != 500
                or filtering.get('reset') != 'zero_on_episode_reset_or_gate_loss'
                or filtering.get('actor_previous_residual') != 'requested_pre_filter'
                or isinstance(cutoff, bool) or not isinstance(cutoff, (float, int))
                or not np.isfinite(cutoff) or not 0 < cutoff < 250
                or isinstance(alpha, bool) or not isinstance(alpha, (float, int))
                or not np.isfinite(alpha)
                or not np.isclose(alpha, -np.expm1(-2*np.pi*cutoff/500), atol=1e-8, rtol=0)):
            raise ValueError('Unsupported saved residual torque filter')
    if metadata['residual_wheel_latch']:
        raise ValueError('Torque residual uses its own fixed wheel reference without a velocity latch')
    actor_hz=metadata['actor_hz']
    if actor_hz not in (250,500) or (metadata['teacher_hz'],metadata['physics_hz']) != (50,500):
        raise ValueError('Expected torque250/500Hz / Teacher50Hz / physics500Hz')
    if actor_hz==500 and (not np.isclose(metadata.get('history_sample_period_s',0),.002)
            or not np.isclose(metadata.get('history_first_to_last_s',0),.018)):
        raise ValueError('Residual500Hz requires saved2ms/18ms history timing')
    metadata['residual_mode'] = 'torque'
    pose_mode = metadata.get('pose_command_mode','nominal')
    if pose_mode not in ('nominal','height','height_roll_pitch'):
        raise ValueError('Unsupported residual pose command mode')
    if pose_mode != 'nominal':
        ranges = np.asarray(metadata.get('pose_command_ranges'),dtype=float)
        if (ranges.shape != (3,2) or not np.isfinite(ranges).all()
                or np.any(ranges[:,0]>ranges[:,1]) or np.any(ranges[:2,0]>0) or np.any(ranges[:2,1]<0)
                or not .27 <= ranges[2,0] <= .335 <= ranges[2,1] <= .42
                or np.any(np.max(np.abs(ranges[:2]),axis=1) > np.array([np.pi/6,np.pi/12])+1e-8)):
            raise ValueError('Invalid saved residual pose command ranges')
    metadata['checkpoint'] = str(checkpoint)
    metadata['policy_checkpoint_sha256'] = digest
    return metadata


def residual_lpf_hz(metadata, requested=None):
    """Restore the trained cutoff unless a playback override (including 0) is supplied."""
    filtering = metadata.get('residual_torque_filter')
    cutoff = 0. if filtering is None else filtering['cutoff_hz']
    if requested is not None:
        cutoff = requested
    if (isinstance(cutoff, bool) or not isinstance(cutoff, (float, int))
            or not np.isfinite(cutoff) or not 0 <= cutoff < 250):
        raise ValueError('Residual LPF must be finite, 0 <= Hz < 250; 0 disables filtering')
    return float(cutoff)


class StopResidual:
    def __init__(self, cfg, env, adapter):
        import torch
        self.torch = torch
        from mj_lab.flash_sac import runtime
        runtime.setup_imports(False)
        from flash_rl.agents.flashSAC.network import FlashSACActor
        self.metadata = residual_metadata(cfg['learned_residual'], cfg['policy_interface']['checkpoint_sha256'])
        self.is_action = False
        agent = self.metadata['flash_sac_agent']
        self.actor = FlashSACActor(agent['actor_num_blocks'], 440, agent['actor_hidden_dim'], 8)
        state = torch.load(self.metadata['checkpoint'], map_location='cpu', weights_only=True)
        self.actor.load_state_dict(state['network_state_dict'])
        self.actor.eval().requires_grad_(False)
        torch.set_num_threads(1)
        teacher = Path(cfg['policy_interface']['checkpoint']).parent/'ddt.json'
        mapping = json.loads(teacher.read_text())
        self.positive = np.asarray(mapping['action_gain_positive'], dtype=np.float32)
        self.negative = np.asarray(mapping['action_gain_negative'], dtype=np.float32)
        if not np.isfinite(np.r_[self.positive, self.negative]).all() or min(*self.positive, *self.negative) <= 0:
            raise ValueError('Teacher action gains must be positive and finite')
        self.env, self.adapter = env, adapter
        fast = deepcopy(cfg)
        self.residual_decimation = self.metadata['physics_hz']//self.metadata['actor_hz']
        fast['control']['decimation'] = self.residual_decimation
        self.builder = ObservationBuilder(fast)
        if self.builder.position_term is None or self.builder.heading_term is None:
            raise ValueError('Residual requires saved Teacher wheel/heading channels')
        self.heading_offset = 0
        for term in self.builder.layout:
            if term['kind'] == 'heading_error':
                break
            self.heading_offset += term['size']
        self.defaults = np.asarray(cfg['robot']['default_joint_angles'], dtype=np.float32)
        self.limit = float(self.metadata['torque_residual_limit_nm'])
        self.filter_hz = residual_lpf_hz(self.metadata, cfg.get('residual_lpf_hz'))
        self.filter_alpha = None if self.filter_hz == 0 else float(-np.expm1(-2*np.pi*self.filter_hz/500))
        self.command = np.zeros(3, dtype=np.float32)
        self.pose = np.asarray([0., 0., cfg['pose_command']['nominal_height']], dtype=np.float32)
        self.raw_action = np.zeros(8, dtype=np.float32)
        self.command_action = np.zeros(8, dtype=np.float32)
        self.inferences = self.disabled_ticks = 0
        self.maximum_residual = np.zeros(8)
        self.reset()

    def reset(self):
        self.builder.reset()
        self.history = None
        self.enabled = False
        self.residual = np.zeros(8, dtype=np.float32)
        self.filtered_residual = np.zeros(8, dtype=np.float32)
        self.wheel_error = 0.
        self.previous_angles = None
        self.substep = 0

    def pose_allowed(self, pose, target):
        if self.metadata.get('pose_command_mode','nominal') == 'nominal':
            nominal = np.array([0.,0.,self.metadata.get('nominal_height',.335)],dtype=np.float32)
            return bool(np.array_equal(pose,nominal) and np.array_equal(target,nominal))
        ranges = np.asarray(self.metadata['pose_command_ranges'],dtype=float)
        values = np.asarray([pose,target],dtype=float)
        return bool(np.isfinite(values).all() and (values>=ranges[:,0]-1e-7).all()
                    and (values<=ranges[:,1]+1e-7).all())

    def state(self):
        quat = self.env.base_quat_sensor()
        rotation = quat_wxyz_to_rotmat(quat)
        return ObsState(self.env.joint_pos(), self.env.joint_vel(), quat, self.env.base_ang_vel(),
                        self.command.copy(), self.command_action.copy(),
                        rotation.T@self.env.base_lin_vel(), pose_command=self.pose.copy())

    def angles(self, state):
        q = state.joint_pos
        return q[[3, 7]]+q[[1, 5]]+q[[2, 6]]+float(quat_wxyz_to_rpy(state.base_quat_wxyz)[1])

    def frame(self, state):
        command = np.zeros(6)
        if self.metadata.get('pose_command_mode','nominal') != 'nominal':
            command = np.r_[self.command,(self.pose.astype(np.float32)-np.array([0.,0.,.335],np.float32))
                            /np.array([.5,.3,.1],np.float32)]
        gravity = quat_wxyz_to_rotmat(state.base_quat_wxyz).T@np.array([0., 0., -1.])
        value = np.r_[state.base_ang_vel*.25, gravity,
                      (state.joint_pos-self.defaults)[[0, 1, 2, 4, 5, 6]]*2.,
                      state.joint_vel*.05, self.raw_action, self.residual/10., command]
        value = np.clip(value, -10., 10.).astype(np.float32)
        scale = np.asarray(self.builder.position_term['scale']).item()
        return np.r_[value, self.wheel_error*scale,
                     self.teacher_observation[self.heading_offset]].astype(np.float32)

    def advance(self, state):
        self.teacher_observation = self.builder.build(state)
        angles = self.angles(state)
        if self.enabled and self.previous_angles is not None:
            delta = (angles-self.previous_angles+np.pi) % (2*np.pi)-np.pi
            self.wheel_error += float(delta.mean())*self.builder.position_term['params']['radius']
        self.previous_angles = angles.copy()
        if self.history is not None:
            self.history[:-1] = self.history[1:]
            self.history[-1] = self.frame(state)

    def observe(self, state, allowed):
        self.command = state.command.copy()
        self.pose = state.pose_command.copy()
        entering = bool(allowed) and not self.enabled
        if not allowed or entering:
            self.history = None
            self.wheel_error = 0.
            self.previous_angles = None
            self.residual[:] = 0.
            self.filtered_residual[:] = 0.
        self.enabled = bool(allowed)
        self.advance(state)
        return self.teacher_observation.copy()

    def begin(self, action):
        self.command_action = action.copy()
        self.raw_action = action/np.where(action >= 0, self.positive, self.negative)
        self.substep = 0

    def torque(self, positions, velocities):
        if self.substep % self.residual_decimation == 0:
            if self.substep:
                self.env.mujoco.mj_forward(self.env.model, self.env.data)
                self.advance(self.state())
            if self.enabled:
                frame = self.frame(self.state())
                if self.history is None:
                    self.history = np.tile(frame, (10, 1))
                self.history[-1] = frame
                with self.torch.inference_mode():
                    mean, _ = self.actor.get_mean_and_std(
                        self.torch.from_numpy(self.history.reshape(1, 440)), training=False)
                    self.residual = mean.tanh()[0].numpy()*self.limit
                if not np.isfinite(self.residual).all():
                    raise ValueError('Non-finite learned residual torque')
                self.inferences += 1
                self.maximum_residual = np.maximum(self.maximum_residual, np.abs(self.residual))
            else:
                self.residual[:] = 0.
                self.disabled_ticks += 1
        self.substep += 1
        # Update every 2ms, including the held actor sample. Keep actor history
        # in requested torque units, matching training's pre-filter feedback.
        if self.filter_alpha is None:
            self.filtered_residual[:] = self.residual
        elif self.enabled:
            self.filtered_residual += self.filter_alpha*(self.residual-self.filtered_residual)
        else:
            self.filtered_residual[:] = 0.
        return self.adapter.compute(self.command_action,positions,velocities,residual=self.filtered_residual)
