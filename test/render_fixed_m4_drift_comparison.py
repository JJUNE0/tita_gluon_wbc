"""VALIDATION_SIM: matched 15-minute rollouts and real-time drift comparison MP4s."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import time

os.environ.setdefault('MUJOCO_GL', 'egl')
os.environ.setdefault('LP_NUM_THREADS', '2')
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from flash_overnight_model_stages import CKPT, REPO, Runner, prepared_config, sha256
from sim2sim_ros2_jazzy.residual_wheel_lqr import ResidualWheelLQR

DT, FPS = .02, 10
HORIZONS = [60, 300, 900]
NAMES = ['FlashSAC only', 'FlashSAC + Fixed M4 LQR']
COLORS = [(89, 177, 255), (87, 222, 169)]
W, H = 640, 300
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONTS = {size: ImageFont.truetype(FONT_PATH, size) for size in [13, 15, 18, 21, 27]}


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def collect(out):
    cfg = json.loads(prepared_config(CKPT).read_text())
    runner = Runner(cfg, dict(seed=270, pitch=0.))
    try:
        for _ in range(400):
            runner.step(0.)
        assert not runner.failures()
        snapshot = runner.snapshot()
        write(out / 'config.json', cfg)
        for group in range(2):
            path = out / f'group_{group}.npz'
            if path.exists():
                raise FileExistsError(path)
            runner.restore(snapshot)
            residual = ResidualWheelLQR(runner.env) if group else None
            positions, rpy, sensors, actions, inputs = [], [], [], [], []
            qpos, qvel, sample_ticks = [], [], []
            failure = []
            started = time.monotonic()
            for tick in range(round(900 / DT) + 1):
                observation = runner.observation
                positions.append(observation['base_position'].copy())
                rpy.append(observation['rpy'].copy())
                sensors.append(observation['sensor'].copy())
                actions.append(runner.playback.last_action.copy())
                failure = runner.failures()
                if tick % 5 == 0 or failure:
                    sample_ticks.append(tick)
                    qpos.append(runner.env.data.qpos.copy())
                    qvel.append(runner.env.data.qvel.copy())
                if failure or tick == 45000:
                    break
                total = 0.
                if residual:
                    residual.update(np.zeros(3), runner.playback.last_action)
                    total = residual.u
                step = runner.step(total)
                if residual:
                    np.testing.assert_allclose(residual.apply(step['flash'][0]), step['motor'][0], atol=1e-7)
                assert np.isfinite(step['motor']).all()
                assert np.max(abs(step['motor'][:, [3, 7]])) <= 12.000001
                inputs.append([total, step['actual_u']])
                if tick % 3000 == 0:
                    print(f'[VALIDATION_SIM] {NAMES[group]}: {tick * DT:.0f}/900 s; '
                          f'elapsed {time.monotonic() - started:.1f}s', flush=True)
            np.savez_compressed(path, base_position=positions, rpy=rpy, sensor=sensors,
                                previous_action=actions, residual=inputs, qpos=qpos, qvel=qvel,
                                sample_ticks=sample_ticks)
            write(out / f'group_{group}_status.json', dict(execution_domain='VALIDATION_SIM',
                  evidence_status='FAIL' if failure else 'PASS', failure=failure,
                  duration_seconds=tick * DT, samples=tick + 1, disabled_obstacles=runner.disabled_obstacles))
            print(f'[VALIDATION_SIM] {NAMES[group]} completed {tick * DT:.2f}s, failure={failure}', flush=True)
    finally:
        runner.env.close()
    summarize(out)


def summarize(out, horizons=HORIZONS):
    cfg = json.loads((out / 'config.json').read_text())
    traces = [np.load(out / f'group_{i}.npz') for i in range(2)]
    for key in ['qpos', 'qvel', 'previous_action', 'base_position', 'rpy']:
        np.testing.assert_array_equal(traces[0][key][0], traces[1][key][0])
    metrics = {}
    for horizon in horizons:
        metrics[str(horizon)] = []
        for group, trace in enumerate(traces):
            end = min(round(horizon / DT), len(trace['base_position']) - 1)
            position = trace['base_position'][:end + 1]
            delta = position[:, :2] - position[0, :2]
            drift = np.linalg.norm(delta, axis=1)
            yaw = np.unwrap(trace['rpy'][:end + 1, 2])
            metrics[str(horizon)].append(dict(controller=NAMES[group],
                completed_seconds=end * DT, complete=end * DT == horizon,
                final_drift_m=float(drift[-1]), max_drift_m=float(drift.max()),
                final_delta_xy_m=delta[-1].tolist(), final_yaw_delta_degrees=float(np.degrees(yaw[-1] - yaw[0])),
                final_heading_error_degrees=float((np.degrees(yaw[-1] - yaw[0]) + 180) % 360 - 180),
                radial_position_IAE_m_s=float(np.trapz(drift, dx=DT))))
    write(out / 'metrics.json', dict(execution_domain='VALIDATION_SIM',
          evidence_status='PASS' if all(x['complete'] for rows in metrics.values() for x in rows) else 'FAIL',
          checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
          onnx_sha256=cfg['policy_interface']['onnx_sha256'], same_initial_state_exact=True, horizons=metrics))


def line(draw, points, color, width=2):
    if len(points) > 1:
        draw.line(points, fill=color, width=width)


def markers(mj, renderer, origin, path=None, color=None):
    for size in [[.14, .008, .004], [.008, .14, .004]]:
        scene = renderer.scene
        geom = scene.geoms[scene.ngeom]
        mj.mjv_initGeom(geom, mj.mjtGeom.mjGEOM_BOX, np.asarray(size),
                       np.r_[origin[:2], .008], np.eye(3).ravel(), np.array([1., .78, .18, 1.]))
        scene.ngeom += 1
    if path is not None and len(path) > 1:
        indices = np.unique(np.linspace(0, len(path) - 1, min(160, len(path))).astype(int))
        for first, second in zip(path[indices[:-1]], path[indices[1:]]):
            if np.linalg.norm(second[:2] - first[:2]) < 1e-6:
                continue
            scene = renderer.scene
            geom = scene.geoms[scene.ngeom]
            mj.mjv_initGeom(geom, mj.mjtGeom.mjGEOM_LINE, np.zeros(3), np.zeros(3),
                           np.eye(3).ravel(), np.r_[np.asarray(color) / 255., .9])
            mj.mjv_connector(geom, mj.mjtGeom.mjGEOM_LINE, 2.,
                             np.r_[first[:2], .018], np.r_[second[:2], .018])
            scene.ngeom += 1


def render(out, duration, *, env_factory=None, condition_label=None, physics_note='Nominal flat floor'):
    from sim2sim_ros2_jazzy.mujoco_env import TitaMujocoEnv
    traces = []
    for group in range(2):
        with np.load(out / f'group_{group}.npz') as archive:
            traces.append({key: archive[key] for key in archive.files})
    cfg = json.loads((out / 'config.json').read_text())
    env = TitaMujocoEnv(cfg) if env_factory is None else env_factory(cfg)
    mj, model = env.mujoco, env.model
    renderer = encoder = None
    video = out / f'flashsac_vs_fixed_m4_{duration // 60:02d}min.mp4'
    if video.exists():
        raise FileExistsError(video)
    try:
        disabled = json.loads((out / 'group_0_status.json').read_text())['disabled_obstacles']
        model.geom_rgba[disabled, 3] = 0.
        model.vis.global_.offwidth, model.vis.global_.offheight = W, H
        model.vis.quality.offsamples = 0
        model.vis.global_.fovy = 38.
        model.vis.headlight.ambient[:] = .55
        model.vis.headlight.diffuse[:] = .8
        renderer = mj.Renderer(model, height=H, width=W)
        from OpenGL import GL
        render_backend = GL.glGetString(GL.GL_RENDERER).decode()
        data = mj.MjData(model)
        end = round(duration / DT)
        origin = traces[0]['base_position'][0]
        paths = [t['base_position'][:end + 1, :2] - origin[:2] for t in traces]
        all_xy = np.concatenate(paths)
        low = np.minimum(all_xy.min(0), 0.)
        high = np.maximum(all_xy.max(0), 0.)
        centre = (low + high) / 2
        span = max(float((high - low).max()), .2) * 1.25
        drift_max = max(float(np.linalg.norm(p, axis=1).max()) for p in paths)
        drift_axis = max(.1, drift_max * 1.1)
        camera = mj.MjvCamera()
        mj.mjv_defaultCamera(camera)
        camera.lookat[:] = np.r_[origin[:2] + centre, .25]
        camera.distance = max(2.6, span * 1.9)
        camera.azimuth, camera.elevation = 90., -50.
        detail = mj.MjvCamera()
        mj.mjv_defaultCamera(detail)
        detail.distance, detail.azimuth, detail.elevation = 1.5, 115., -20.
        drifts = [np.linalg.norm(p, axis=1) for p in paths]
        yaw = [np.degrees(np.unwrap(t['rpy'][:, 2]) - t['rpy'][0, 2]) for t in traces]
        # Static axes and full-history coordinate arrays, with equal scale in both panels.
        plot_xy = []
        plot_drift = []
        for group, path in enumerate(paths):
            x = group * W
            plot_xy.append(np.column_stack([x + 168 + (path[:, 0] - centre[0]) / span * 130,
                                           878 - (path[:, 1] - centre[1]) / span * 130]))
            plot_drift.append(np.column_stack([x + 340 + np.arange(len(path)) * DT / duration * 275,
                                              941 - drifts[group] / drift_axis * 125]))
        started = time.monotonic()
        frames = duration * FPS + 1
        with (out / f'ffmpeg_{duration}.log').open('w') as error_log:
            encoder = subprocess.Popen(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1280x1000', '-r', str(FPS), '-i', '-',
                '-an', '-c:v', 'libx264', '-threads', '2', '-preset', 'fast', '-crf', '21', '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart', str(video)], stdin=subprocess.PIPE, stderr=error_log)
            for frame in range(frames):
                tick = frame * 5
                canvas = Image.new('RGB', (1280, 1000), (14, 20, 30))
                draw = ImageDraw.Draw(canvas)
                draw.text((18, 10), 'ZERO-COMMAND DRIFT  |  FlashSAC vs Fixed M4', font=FONTS[27], fill='white')
                draw.text((18, 46), f'Simulation {frame / FPS:06.1f} / {duration} s  |  1x speed  |  model_60000  |  matched start, seed 270',
                          font=FONTS[18], fill=(185, 199, 216))
                if condition_label:
                    draw.text((18, 69), condition_label, font=FONTS[13], fill=(255, 205, 95))
                for group, trace in enumerate(traces):
                    x, color = group * W, COLORS[group]
                    actual_tick = min(tick, len(trace['base_position']) - 1)
                    sample = min(frame, len(trace['sample_ticks']) - 1)
                    assert trace['sample_ticks'][sample] == actual_tick
                    data.qpos[:] = trace['qpos'][sample]
                    data.qvel[:] = trace['qvel'][sample]
                    mj.mj_forward(model, data)
                    base = data.xpos[model.body('base_link').id]
                    np.testing.assert_allclose(base, trace['base_position'][actual_tick], atol=1e-12)
                    delta = paths[group][actual_tick]
                    draw.text((x + 16, 86), NAMES[group], font=FONTS[21], fill=color)
                    draw.text((x + 16, 117), f'Distance from start: {drifts[group][actual_tick]:.4f} m  |  max {drifts[group][:actual_tick + 1].max():.4f} m',
                              font=FONTS[18], fill='white')
                    draw.text((x + 16, 145), f'dX {delta[0]:+.4f} m   dY {delta[1]:+.4f} m   yaw total {yaw[group][actual_tick]:+.2f} deg',
                              font=FONTS[18], fill=(190, 204, 220))
                    renderer.update_scene(data, camera=camera)
                    renderer.scene.flags[mj.mjtRndFlag.mjRND_SHADOW] = 0
                    renderer.scene.flags[mj.mjtRndFlag.mjRND_REFLECTION] = 0
                    renderer.scene.flags[mj.mjtRndFlag.mjRND_FOG] = 0
                    markers(mj, renderer, origin, trace['base_position'][:actual_tick + 1], color)
                    canvas.paste(Image.fromarray(renderer.render()), (x, 180))
                    draw.text((x + 16, 545), 'FIXED WORLD VIEW  |  same camera scale; yellow cross = start', font=FONTS[15], fill=(180, 194, 211))
                    detail.lookat[:] = base + [0., 0., -.05]
                    renderer.update_scene(data, camera=detail)
                    renderer.scene.flags[mj.mjtRndFlag.mjRND_SHADOW] = 0
                    renderer.scene.flags[mj.mjtRndFlag.mjRND_REFLECTION] = 0
                    renderer.scene.flags[mj.mjtRndFlag.mjRND_FOG] = 0
                    markers(mj, renderer, origin)
                    canvas.paste(Image.fromarray(renderer.render()).resize((448, 210)), (x + 96, 575))
                    draw.text((x + 16, 788), 'FOLLOW VIEW  |  same posture magnification', font=FONTS[15], fill=(180, 194, 211))
                    draw.rectangle((x + 30, 810, x + 305, 949), outline=(75, 95, 118))
                    points = plot_xy[group][:actual_tick + 1:5]
                    line(draw, [tuple(v) for v in points], color)
                    start = (x + 168 - centre[0] / span * 130, 878 + centre[1] / span * 130)
                    draw.ellipse((start[0] - 4, start[1] - 4, start[0] + 4, start[1] + 4), fill=(255, 200, 50))
                    last = plot_xy[group][actual_tick]
                    draw.ellipse((last[0] - 3, last[1] - 3, last[0] + 3, last[1] + 3), fill=color)
                    draw.text((x + 30, 952), f'X/Y trajectory | shared span {span:.2f} m', font=FONTS[13], fill=(180, 194, 211))
                    draw.rectangle((x + 340, 810, x + 615, 949), outline=(75, 95, 118))
                    line(draw, [tuple(v) for v in plot_drift[group][:actual_tick + 1:5]], color)
                    draw.text((x + 346, 812), f'{drift_axis:.2f} m', font=FONTS[13], fill=(180, 194, 211))
                    draw.text((x + 340, 952), f'Distance vs time | 0 to {duration} s', font=FONTS[13], fill=(180, 194, 211))
                    if actual_tick < tick:
                        draw.text((x + 16, 180), f'RUN STOPPED at {actual_tick * DT:.2f} s', font=FONTS[21], fill='red')
                draw.text((18, 979), f'Position = base_link ground truth for evaluation only. Sensors drive M4. {physics_note}; no online adaptation.',
                          font=FONTS[13], fill=(155, 173, 195))
                if frame in [0, frames - 1]:
                    canvas.save(out / f'{duration}s_{"first" if frame == 0 else "last"}.png')
                encoder.stdin.write(canvas.tobytes())
                if frame % 100 == 0:
                    print(f'[VALIDATION_SIM] video {duration}s: {frame / FPS:.0f}s rendered; '
                          f'elapsed {time.monotonic() - started:.1f}s', flush=True)
            encoder.stdin.close()
            assert encoder.wait() == 0
        probe = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
            '-show_entries', 'stream=codec_name,width,height,nb_read_frames,r_frame_rate:format=duration,size',
            '-of', 'json', str(video)], capture_output=True, text=True, check=True)
        info = json.loads(probe.stdout)
        assert int(info['streams'][0]['nb_read_frames']) == frames
        assert abs(float(info['format']['duration']) - frames / FPS) < .01
        write(out / f'video_{duration}_verification.json', dict(execution_domain='VALIDATION_SIM',
              evidence_status='PASS', video=video.name, sha256=sha256(video), frames=frames, fps=FPS,
              simulation_seconds=duration, render_backend=render_backend,
              condition_label=condition_label,
              yaw_display='signed cumulative unwrapped yaw change from start',
              render_pose_matches_recorded_base=True, ffprobe=info))
    finally:
        if encoder and encoder.poll() is None:
            encoder.terminate()
            encoder.wait()
        if renderer:
            renderer.close()
        env.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--stage', choices=['collect', 'summarize', 'render'], required=True)
    parser.add_argument('--duration', type=int, choices=HORIZONS)
    args = parser.parse_args()
    out = args.output.resolve()
    if not out.is_relative_to(REPO / 'docs/exp') or not out.is_dir():
        parser.error('Existing docs/exp/YYYY-MM-DD evidence directory required')
    if args.stage == 'collect':
        collect(out)
    elif args.stage == 'summarize':
        summarize(out)
    else:
        if args.duration is None:
            parser.error('--duration required for render')
        render(out, args.duration)


if __name__ == '__main__':
    main()
