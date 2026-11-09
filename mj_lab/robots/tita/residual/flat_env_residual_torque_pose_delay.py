"""TRAINING_SIM: existing torque-delay task with random pose command targets."""
import math

from ..roll_pitch_height.flat_env_roll_pitch_height_cfg import pose_error
from .flat_env_residual_torque_delay import TitaFlatResidualTorqueDelayEnv, TitaFlatResidualTorqueDelayEnvCfg


class TitaFlatResidualTorquePoseDelayEnvCfg(TitaFlatResidualTorqueDelayEnvCfg):
    def __init__(self, teacher_checkpoint, *, pose_command_mode='height_roll_pitch',
                 pose_height_range=(.27,.42), pose_roll_pitch_deg=5., pose_nominal_fraction=.3,
                 pose_resampling_s=(5.,8.), pose_roll_deg=None, pose_pitch_deg=None, **kwargs):
        if pose_command_mode not in ('height','height_roll_pitch'):
            raise ValueError('Expected height or height_roll_pitch command randomization')
        if (len(pose_height_range)!=2 or not all(math.isfinite(v) for v in pose_height_range)
                or not .27<=pose_height_range[0]<=.335<=pose_height_range[1]<=.42
                or not math.isfinite(pose_roll_pitch_deg) or not 0<pose_roll_pitch_deg<=15
                or (pose_roll_deg is not None and (not math.isfinite(pose_roll_deg) or not 0<pose_roll_deg<=30))
                or (pose_pitch_deg is not None and (not math.isfinite(pose_pitch_deg) or not 0<pose_pitch_deg<=15))
                or not math.isfinite(pose_nominal_fraction) or not 0<=pose_nominal_fraction<=1
                or len(pose_resampling_s)!=2 or not all(math.isfinite(v) for v in pose_resampling_s)
                or not 0<pose_resampling_s[0]<=pose_resampling_s[1]):
            raise ValueError('Invalid torque residual pose command sampling')
        super().__init__(teacher_checkpoint, **kwargs)
        if self.teacher_metadata['actor_obs_dim']!=38:
            raise ValueError('Random pose torque residual requires the saved pose Teacher38')
        self.pose_command_mode=pose_command_mode
        pose=self.commands['base_pose']
        roll=math.radians(pose_roll_pitch_deg if pose_roll_deg is None else pose_roll_deg) if pose_command_mode=='height_roll_pitch' else 0.
        pitch=math.radians(pose_roll_pitch_deg if pose_pitch_deg is None else pose_pitch_deg) if pose_command_mode=='height_roll_pitch' else 0.
        pose.height_range=tuple(pose_height_range)
        pose.roll_range=(-roll,roll)
        pose.pitch_range=(-pitch,pitch)
        pose.rel_nominal_envs=pose_nominal_fraction
        pose.resampling_time_range=tuple(pose_resampling_s)
        pose.ramp_rates=(.15,.15,.05)

    def residual_manifest(self):
        value=super().residual_manifest();pose=self.commands['base_pose']
        value.update(pose_command_mode=self.pose_command_mode,
            pose_command_ranges=[list(pose.roll_range),list(pose.pitch_range),list(pose.height_range)],
            pose_command_nominal_fraction=pose.rel_nominal_envs,
            pose_command_resampling_s=list(pose.resampling_time_range),
            pose_command_ramp_rates=list(pose.ramp_rates),
            pose_command_sampling='Random target commands; fixed initial pose and zero initial velocities',
            pose_observation='Existing torque frame channels39:42 encode emitted pose minus nominal, divided by [.5,.3,.1]',
            history_sample_period_s=.004,history_first_to_last_s=.036)
        return value


class TitaFlatResidualTorquePoseDelayEnv(TitaFlatResidualTorqueDelayEnv):
    def step(self, residual_nm):
        reward,failed,timeout,info=super().step(residual_nm)
        command=self.raw.command_manager.get_command('base_pose')
        for index,name in enumerate(('roll','pitch','height')):
            unit='m' if name=='height' else 'rad'
            info[f'pose_{name}_error_{unit}']=pose_error(self.raw,index)
            info[f'pose_command_{name}_{unit}']=command[:,index]
        info['angular_xy_speed_rad_s']=self.robot.data.root_link_ang_vel_b[:,:2].norm(dim=1)
        return reward,failed,timeout,info
