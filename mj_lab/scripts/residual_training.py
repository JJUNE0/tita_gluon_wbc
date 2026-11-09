"""TRAINING_SIM / VALIDATION_SIM: torque learner helpers and recorded-pose rendering."""
import argparse
import json
import os
from pathlib import Path

os.environ.setdefault('MUJOCO_GL','egl')
import numpy as np
import torch
from mj_lab.flash_sac import runtime

def write(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')
    temporary.replace(path)


class ResidualPolicy(torch.nn.Module):
    """Deterministic native Actor mean -> normalized residual request."""
    def __init__(self, actor):
        super().__init__()
        self.actor = actor

    def forward(self, observation):
        x = self.actor.embedder(observation, training=False)
        for block in self.actor.encoder:
            x = block(x, training=False)
        norm = self.actor.post_norm
        x = x*torch.rsqrt(x.square().mean(-1, keepdim=True)+norm.eps)*norm.weight
        mean = torch.nn.functional.linear(x, self.actor.predictor.mean_w.w.weight, self.actor.predictor.mean_bias)
        return mean.tanh()


def render_trace(source, target, label):
    """VALIDATION_SIM: render recorded training/evaluation poses, not new control."""
    import imageio.v2 as imageio
    import mujoco
    from PIL import Image, ImageDraw
    from mj_lab.robots.tita.common.robot_cfg import get_spec, JOINTS
    with np.load(source, allow_pickle=False) as recorded:
        spec = get_spec()
        spec.worldbody.add_geom(type=mujoco.mjtGeom.mjGEOM_PLANE, size=[200., 200., .1],
                                rgba=[.25, .28, .3, 1.], contype=0, conaffinity=0)
        payload = spec.body('base_link').add_body(name='video_payload')
        payload.add_geom(name='video_mass', type=mujoco.mjtGeom.mjGEOM_SPHERE,
                         size=[.03, 0., 0.], mass=1e-6, contype=0, conaffinity=0, rgba=[1., .3, .05, 1.])
        model = spec.compile()
        data = mujoco.MjData(model)
        joints = [model.joint(name).qposadr[0] for name in JOINTS]
        root = next(model.joint(i).qposadr[0] for i in range(model.njnt)
                    if model.jnt_type[i] == mujoco.mjtJoint.mjJNT_FREE)
        body, geom = model.body('video_payload').id, model.geom('video_mass').id
        camera = mujoco.MjvCamera()
        camera.distance, camera.azimuth, camera.elevation = 2., 135., -15.
        renderer = mujoco.Renderer(model, height=480, width=640)
        try:
            with imageio.get_writer(target, fps=25, codec='libx264', quality=7) as video:
                origin = recorded['root'][0, :2].copy()
                for i, pose in enumerate(recorded['root']):
                    data.qpos[root:root+7] = pose
                    data.qpos[root:root+2] -= origin
                    data.qpos[joints] = recorded['joints'][i]
                    model.body_pos[body] = recorded['payload_position'][i]
                    model.geom_rgba[geom, 3] = float(recorded['mass'][i] > .001)
                    mujoco.mj_forward(model, data)
                    camera.lookat[:] = [*data.qpos[root:root+2], .25]
                    renderer.update_scene(data, camera=camera)
                    image = Image.fromarray(renderer.render())
                    draw = ImageDraw.Draw(image)
                    draw.rectangle((0, 0, 640, 90), fill=(20, 20, 20))
                    draw.text((8, 7), f"{label} / t={recorded['time'][i]:.2f}s\n"
                        f"payload={recorded['mass'][i]:.2f}kg force={recorded['force'][i]:.1f}N "
                        f"speed={recorded['speed'][i]*100:.2f}cm/s", fill='white')
                    if 'pose_command' in recorded:
                        command = recorded['pose_command'][i]
                        draw.text((8, 59), f"target h={command[2]:.3f}m roll/pitch={np.degrees(command[:2]).round(1)}deg "
                            f"actual h={pose[2]:.3f}m", fill='white')
                    video.append_data(np.asarray(image))
        finally:
            renderer.close()


def frame(env, world, info):
    return dict(root=env.robot.data.root_link_pose_w[world].cpu().numpy().copy(),
        joints=env.robot.data.joint_pos[world, env.ids].cpu().numpy().copy(),
        payload_position=env.raw.payload_location[world].cpu().numpy().copy(),
        mass=float(info['payload_kg'][world]), force=float(info['force_n'][world]),
        speed=float(info['planar_speed'][world]), time=float(env.age[world]*env.dt),
        pose_command=env.raw.command_manager.get_command('base_pose')[world].cpu().numpy().copy())


def save_frames(path, frames):
    np.savez_compressed(path, **{key: np.asarray([row[key] for row in frames]) for key in frames[0]})


def save_curves(output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    rows = [json.loads(line) for line in (output/'metrics.jsonl').read_text().splitlines()]
    if not rows:
        return None
    x = [row['vector_step'] for row in rows]
    figure, axes = plt.subplots(5,1,figsize=(11,13),sharex=True)
    axes[0].plot(x,[row['task_reward'] for row in rows])
    axes[0].set_ylabel('Task reward / step')
    for group in ('clean','dr'):
        axes[1].plot(x,[row[group+'/planar_speed'] for row in rows],label=group)
        axes[2].plot(x,[row[group+'/residual_rms'] for row in rows],label=group)
        axes[3].plot(x,[row.get(group+'/pose_height_error_m',0.)*100 for row in rows],label=group)
        axes[4].plot(x,[np.degrees(np.hypot(row.get(group+'/pose_roll_error_rad',0.),
            row.get(group+'/pose_pitch_error_rad',0.))) for row in rows],label=group)
    axes[1].set_ylabel('Planar speed (m/s)')
    axes[2].set_ylabel('Residual torque RMS (Nm)')
    axes[3].set_ylabel('Height error (cm)')
    axes[4].set_ylabel('Roll/pitch error (deg)')
    axes[4].set_xlabel('Vector control step')
    for axis in axes:
        axis.grid(alpha=.3)
    axes[1].legend()
    figure.tight_layout()
    path = output/'training_curves.png'
    figure.savefig(path,dpi=150)
    plt.close(figure)
    return path


def fresh_agent(env, reference, args):
    runtime.setup_imports(False)
    from flash_rl.agents.flashSAC.agent import FlashSACConfig
    settings = dict(reference)
    settings.update(seed=args.seed, device_type='cuda:0', buffer_device_type='cuda:0',
        buffer_max_length=args.buffer_size, buffer_min_length=args.min_buffer,
        sample_batch_size=args.batch_size, gamma=args.gamma, use_compile=False, use_amp=False,
        load_optimizer=False, load_reward_normalizer=False)
    return runtime.make_agent(env, FlashSACConfig(**settings))


class ContinuousTermination:
    """Keep original eval trials running, while retaining native failure signals."""
    def __init__(self, native):
        self.native = native
        self.latest = None

    def compute(self):
        self.latest = self.native.compute().clone()
        return torch.zeros_like(self.latest)

    def __getattr__(self, name):
        return getattr(self.native, name)


def tensor_digest(values):
    import hashlib
    return hashlib.sha256(values.detach().cpu().contiguous().numpy().tobytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render',type=Path,required=True)
    parser.add_argument('--video-output',type=Path,required=True)
    parser.add_argument('--label',default='Torque residual')
    args=parser.parse_args()
    render_trace(args.render,args.video_output,args.label)


if __name__=='__main__':
    main()
