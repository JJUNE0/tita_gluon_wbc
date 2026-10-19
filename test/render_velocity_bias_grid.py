"""VALIDATION_SIM: eight matched 300s trajectories in a two-row, four-column MP4."""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import subprocess
import time

os.environ.setdefault('MUJOCO_GL', 'egl')
os.environ.setdefault('LP_NUM_THREADS', '2')

import numpy as np
from PIL import Image, ImageDraw

import compare_velocity_bias_m4 as paired
import render_fixed_m4_drift_comparison as visual
from static_target_domain import StaticEnv

DT, FPS = .02, 10
WIDTH, HEIGHT = 2560, 1200
TILE_W, TILE_H, HEADER = 640, 530, 100
WORLD_H = 264
COLORS = [(89, 177, 255), (87, 222, 169)]
NAMES = ['FlashSAC only', 'FlashSAC + velocity bias']


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def collect_one(root, condition, group):
    root = Path(root)
    plan = json.loads((root / 'plan.json').read_text())
    out = root / condition['name']
    out.mkdir(exist_ok=True)
    path = out / f'group_{group}.npz'
    if path.exists():
        raise FileExistsError(path)
    mode = 'velocity' if group else 'baseline'
    e = paired.Comparison(dict(seed=plan['seed'], physics=condition['target'], mode=mode, warmup=0.))
    r, env = e.runner, e.env
    cfg = env.cfg
    started = time.monotonic()
    try:
        assert env.control_dt == DT
        if group:
            assert e.velocity.ACQUISITION_SECONDS == 2.
        assert paired.digest(cfg['policy_interface']['checkpoint']) == cfg['policy_interface']['checkpoint_sha256']
        assert paired.digest(cfg['policy']['path']) == cfg['policy_interface']['onnx_sha256']
        assert all(o['kind'] != 'lin_vel' for o in cfg['policy_interface']['observations'])
        initial_hash = hashlib.sha256(np.r_[env.data.qpos, env.data.qvel, r.playback.last_action].tobytes()).hexdigest()
        physics = dict(target=condition['target'], total_mass_kg=float(env.model.body_mass[1:].sum()),
                       base_com=env.model.body_ipos[env.model.body('base_link').id].tolist())
        if hasattr(env, 'fingerprint'):
            physics.update(env.metadata)
        state, qpos, qvel, ticks, action, bias, eligible = [], [], [], [], [], [], []
        failure = []
        count = round(plan['duration_s'] / DT)
        for tick in range(count + 1):
            o = r.observation
            state.append(np.r_[o['base_position'], o['base_velocity'], o['rpy'], o['fk_sensor']])
            action.append(r.playback.last_action.copy())
            bias.append(e.velocity.u if group else 0.)
            eligible.append(e.velocity.eligible if group else False)
            finite = np.isfinite(np.r_[env.data.qpos, env.data.qvel]).all()
            if not finite or max(abs(o['rpy'][:2])) > .9 or env.data.qpos[2] < .025:
                failure = ['always_on_finite_tilt_height_guard']
            elif tick * DT + 1e-9 >= 2.:
                failure = r.failures()
            if tick % 5 == 0 or failure:
                ticks.append(tick)
                qpos.append(env.data.qpos.copy())
                qvel.append(env.data.qvel.copy())
            if failure or tick == count:
                break
            e.step()  # Actual default controller, native torque clipping and history/leg assertions.
            if tick % 3000 == 0:
                print('[VALIDATION_SIM] collect', condition['name'], mode, tick * DT, flush=True)
        if hasattr(env, 'assert_static'):
            env.assert_static()
        state = np.asarray(state)
        distance = np.linalg.norm(state[:, :2] - state[0, :2], axis=1)
        tail = np.arange(len(state)) * DT >= max(2., plan['duration_s'] - 20.)
        np.savez_compressed(path, state=state, qpos=qpos, qvel=qvel, sample_ticks=ticks,
                            previous_action=action, velocity_bias=bias, eligible=eligible)
        result = dict(execution_domain='VALIDATION_SIM', evidence_status='PASS' if not failure else 'FAIL',
            controller=NAMES[group], condition=condition, duration_s=tick * DT, failure=failure,
            checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
            onnx_sha256=cfg['policy_interface']['onnx_sha256'], initial_physics_sha256=initial_hash,
            acquisition_s=2. if group else None, disabled_obstacles=r.disabled_obstacles, physics=physics,
            final_drift_m=float(distance[-1]), max_drift_m=float(distance.max()),
            radial_IAE_m_s=float(np.trapz(distance, dx=DT)),
            tail_speed_mean_m_s=float(state[tail, 3].mean()) if tail.any() else None,
            tail_speed_rms_m_s=float(np.sqrt(np.mean(state[tail, 3] ** 2))) if tail.any() else None,
            elapsed_wall_s=time.monotonic() - started)
        write(out / f'group_{group}_status.json', result)
        if group == 0:
            write(out / 'config.json', cfg)
        return result
    finally:
        env.close()


def collect(root):
    plan = json.loads((root / 'plan.json').read_text())
    rows = []
    with ProcessPoolExecutor(max_workers=4, mp_context=multiprocessing.get_context('spawn')) as pool:
        tasks = [pool.submit(collect_one, str(root), condition, group)
                 for condition in plan['conditions'] for group in range(2)]
        for task in as_completed(tasks):
            rows.append(task.result())
            write(root / 'collection_results.json', rows)
            print('[VALIDATION_SIM] trajectories complete', len(rows), '/ 8', flush=True)
    for condition in plan['conditions']:
        out = root / condition['name']
        a, b = [json.loads((out / f'group_{i}_status.json').read_text()) for i in range(2)]
        assert a['initial_physics_sha256'] == b['initial_physics_sha256']
        assert a['physics'] == b['physics']
        x, y = [np.load(out / f'group_{i}.npz') for i in range(2)]
        for key in ['qpos', 'qvel', 'previous_action', 'state']:
            np.testing.assert_array_equal(x[key][0], y[key][0])
    write(root / 'collection_verification.json', dict(execution_domain='VALIDATION_SIM',
          evidence_status='PASS', matched_initial_state_per_column=True, matched_physics_per_column=True,
          completed_trajectories=sum(r['duration_s'] == plan['duration_s'] for r in rows), total_trajectories=8))


def init_scene(renderer, env, data, camera, origin, color, path=None):
    renderer.update_scene(data, camera=camera)
    mj = env.mujoco
    for flag in [mj.mjtRndFlag.mjRND_SHADOW, mj.mjtRndFlag.mjRND_REFLECTION, mj.mjtRndFlag.mjRND_FOG]:
        renderer.scene.flags[flag] = 0
    visual.markers(mj, renderer, origin, path, color)
    return Image.fromarray(renderer.render())


def verify_video(path, frames, width):
    probe = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
        '-show_entries', 'stream=codec_name,width,height,nb_read_frames,r_frame_rate:format=duration,size',
        '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    info = json.loads(probe.stdout)
    assert int(info['streams'][0]['nb_read_frames']) == frames
    assert (info['streams'][0]['width'], info['streams'][0]['height']) == (width, HEIGHT)
    assert abs(float(info['format']['duration']) - frames / FPS) < .01
    return info


def render(root, preview=False, column_index=None):
    plan = json.loads((root / 'plan.json').read_text())
    frames = round(plan['duration_s'] * FPS) + 1
    records, resources = {}, []
    encoder = None
    output = root / 'flashsac_vs_velocity_bias_2x4_05min.mp4'
    if column_index is not None:
        output = root / f'column_{column_index}.mp4'
    output_width = WIDTH if column_index is None else TILE_W
    if output.exists() and not preview:
        raise FileExistsError(output)
    try:
        for column, condition in enumerate(plan['conditions']):
            if column_index is not None and column != column_index:
                continue
            out = root / condition['name']
            traces = []
            for group in range(2):
                with np.load(out / f'group_{group}.npz') as archive:
                    traces.append({key: archive[key] for key in archive.files})
            cfg = json.loads((out / 'config.json').read_text())
            env = StaticEnv(cfg, condition['target'])
            env.record_startup = False
            mj, model = env.mujoco, env.model
            status = json.loads((out / 'group_0_status.json').read_text())
            recorded = status['physics']
            assert float(model.body_mass[1:].sum()) == recorded['total_mass_kg']
            np.testing.assert_array_equal(model.body_ipos[model.body('base_link').id], recorded['base_com'])
            if 'fingerprint' in recorded:
                assert env.fingerprint() == recorded['fingerprint']
            model.geom_rgba[status['disabled_obstacles'], 3] = 0.
            model.vis.global_.offwidth, model.vis.global_.offheight = TILE_W, WORLD_H
            model.vis.quality.offsamples = 0
            model.vis.global_.fovy = 38.
            model.vis.headlight.ambient[:] = .55
            model.vis.headlight.diffuse[:] = .8
            world = mj.Renderer(model, height=WORLD_H, width=TILE_W)
            detail = mj.Renderer(model, height=126, width=224)
            resources.append((env, world, detail))
            origin = traces[0]['state'][0, :3]
            paths = [t['state'][:, :2] - origin[:2] for t in traces]
            xy = np.concatenate(paths)
            lo, hi = np.minimum(xy.min(0), 0.), np.maximum(xy.max(0), 0.)
            center = (lo + hi) / 2
            span = max(float((hi - lo).max()), .2) * 1.25
            camera = mj.MjvCamera()
            mj.mjv_defaultCamera(camera)
            camera.lookat[:] = np.r_[origin[:2] + center, .25]
            camera.distance = max(2.6, span * 1.9)
            camera.azimuth, camera.elevation = 90., -50.
            follow = mj.MjvCamera()
            mj.mjv_defaultCamera(follow)
            follow.distance, follow.azimuth, follow.elevation = 1.5, 115., -20.
            records[column] = dict(env=env, world=world, detail=detail, data=mj.MjData(model), origin=origin,
                traces=traces, paths=paths, center=center, span=span, camera=camera, follow=follow,
                distance=[np.linalg.norm(p, axis=1) for p in paths],
                yaw=[np.degrees(np.unwrap(t['state'][:, 6]) - t['state'][0, 6]) for t in traces])
        from OpenGL import GL
        backend = GL.glGetString(GL.GL_RENDERER).decode()
        frame_ids = [0, 100, 1500, frames - 1] if preview else range(frames)
        started = time.monotonic()
        ffmpeg_log = 'ffmpeg.log' if column_index is None else f'ffmpeg_column_{column_index}.log'
        with (root / ffmpeg_log).open('w') as stderr:
            if not preview:
                encoder = subprocess.Popen(['ffmpeg', '-hide_banner', '-loglevel', 'error',
                    '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{output_width}x{HEIGHT}', '-r', str(FPS), '-i', '-',
                    '-an', '-c:v', 'libx264', '-threads', '2', '-preset', 'fast', '-crf', '18',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(output)],
                    stdin=subprocess.PIPE, stderr=stderr)
            for frame in frame_ids:
                tick = frame * 5
                canvas = Image.new('RGB', (WIDTH, HEIGHT), (14, 20, 30))
                draw = ImageDraw.Draw(canvas)
                draw.text((18, 8), 'ZERO-COMMAND DRIFT | FlashSAC vs velocity bias | 2 x 4 environments',
                          font=visual.FONTS[27], fill='white')
                draw.text((18, 43), f'Simulation {frame / FPS:06.1f} / 300 s | 1x speed | model_60000 | start = RL entry | bias delay 2 s',
                          font=visual.FONTS[18], fill=(185, 199, 216))
                for column, condition in enumerate(plan['conditions']):
                    draw.text((column * TILE_W + 12, 75), condition['label'], font=visual.FONTS[18], fill=(255, 205, 95))
                    if column not in records:
                        continue
                    record = records[column]
                    env, data, origin = record['env'], record['data'], record['origin']
                    mj = env.mujoco
                    drift_axis = max(.1, max(float(d.max()) for d in record['distance']) * 1.1)
                    for group, trace in enumerate(record['traces']):
                        x, y, color = column * TILE_W, HEADER + group * TILE_H, COLORS[group]
                        actual = min(tick, len(trace['state']) - 1)
                        sample = min(frame, len(trace['sample_ticks']) - 1)
                        assert trace['sample_ticks'][sample] == actual
                        data.qpos[:] = trace['qpos'][sample]
                        data.qvel[:] = trace['qvel'][sample]
                        mj.mj_forward(env.model, data)
                        base = data.xpos[env.model.body('base_link').id]
                        np.testing.assert_allclose(base, trace['state'][actual, :3], atol=1e-12)
                        distance = record['distance'][group]
                        delta = record['paths'][group][actual]
                        draw.text((x + 12, y + 4), NAMES[group], font=visual.FONTS[21], fill=color)
                        if not group:
                            state = 'residual OFF'
                        elif frame < 20:
                            state = 'WAIT 2 s'
                        elif trace['eligible'][actual]:
                            state = 'ACTIVE'
                        else:
                            state = 'GATED'
                        draw.text((x + 470, y + 8), state, font=visual.FONTS[15], fill=color)
                        draw.text((x + 12, y + 34), f'Distance {distance[actual]:.4f} m | max {distance[:actual + 1].max():.4f} m',
                                  font=visual.FONTS[18], fill='white')
                        draw.text((x + 12, y + 60), f'dX {delta[0]:+.4f} m  dY {delta[1]:+.4f} m  yaw {record["yaw"][group][actual]:+.1f} deg',
                                  font=visual.FONTS[15], fill=(190, 204, 220))
                        main = init_scene(record['world'], env, data, record['camera'], origin, color,
                                          trace['state'][:actual + 1, :3])
                        canvas.paste(main, (x, y + 82))
                        record['follow'].lookat[:] = base + [0., 0., -.05]
                        inset = init_scene(record['detail'], env, data, record['follow'], origin, color)
                        canvas.paste(inset, (x + 404, y + 212))
                        draw.rectangle((x + 403, y + 211, x + 629, y + 339), outline=color)
                        draw.text((x + 407, y + 193), 'FOLLOW VIEW', font=visual.FONTS[13], fill=color)
                        draw.text((x + 12, y + 350), 'Fixed world + follow inset | yellow cross = RL-entry position',
                                  font=visual.FONTS[13], fill=(185, 199, 216))
                        draw.rectangle((x + 14, y + 380, x + 302, y + 493), outline=(75, 95, 118))
                        path = record['paths'][group][:actual + 1:5]
                        points = np.column_stack((x + 158 + (path[:, 0] - record['center'][0]) / record['span'] * 102,
                                                  y + 436 - (path[:, 1] - record['center'][1]) / record['span'] * 102))
                        visual.line(draw, [tuple(p) for p in points], color)
                        ox = x + 158 - record['center'][0] / record['span'] * 102
                        oy = y + 436 + record['center'][1] / record['span'] * 102
                        draw.ellipse((ox - 3, oy - 3, ox + 3, oy + 3), fill=(255, 200, 50))
                        draw.text((x + 14, y + 500), f'XY path | paired span {record["span"]:.2f} m', font=visual.FONTS[13], fill=(185, 199, 216))
                        draw.rectangle((x + 330, y + 380, x + 626, y + 493), outline=(75, 95, 118))
                        indices = np.arange(0, actual + 1, 5)
                        points = np.column_stack((x + 330 + indices * DT / plan['duration_s'] * 296,
                                                  y + 493 - distance[indices] / drift_axis * 107))
                        visual.line(draw, [tuple(p) for p in points], color)
                        draw.text((x + 336, y + 384), f'{drift_axis:.2f} m', font=visual.FONTS[13], fill=(185, 199, 216))
                        draw.text((x + 330, y + 500), 'Distance vs time | same scale within column', font=visual.FONTS[13], fill=(185, 199, 216))
                        if actual < tick:
                            draw.text((x + 12, y + 94), f'RUN STOPPED at {actual * DT:.2f} s', font=visual.FONTS[21], fill='red')
                draw.text((18, 1174), 'GT position for evaluation only | static physics from startup | matched initial state and camera scale within each column | no LQR',
                          font=visual.FONTS[15], fill=(155, 173, 195))
                if frame in [0, 100, 1500, frames - 1]:
                    if column_index is None:
                        canvas.save(root / f'frame_{frame:04d}.png')
                if column_index is not None:
                    canvas = canvas.crop((column_index * TILE_W, 0, (column_index + 1) * TILE_W, HEIGHT))
                if encoder:
                    encoder.stdin.write(canvas.tobytes())
                if frame % 100 == 0:
                    print('[VALIDATION_SIM] grid render', frame / FPS, '/ 300s; wall', round(time.monotonic() - started, 1), flush=True)
            if encoder:
                encoder.stdin.close()
                assert encoder.wait() == 0
        if not preview:
            info = verify_video(output, frames, output_width)
            verification = 'video_verification.json' if column_index is None else f'column_{column_index}_verification.json'
            write(root / verification, dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
                video=output.name, sha256=paired.digest(output), frames=frames, fps=FPS, simulation_s=300,
                render_backend=backend, render_pose_matches_recorded_base=True, ffprobe=info))
    finally:
        if encoder and encoder.poll() is None:
            encoder.terminate()
            encoder.wait()
        for env, world, detail in resources:
            world.close()
            detail.close()
            env.close()


def compose(root):
    plan = json.loads((root / 'plan.json').read_text())
    frames = plan['duration_s'] * FPS + 1
    output = root / 'flashsac_vs_velocity_bias_2x4_05min.mp4'
    if output.exists():
        raise FileExistsError(output)
    metadata = [json.loads((root / f'column_{i}_verification.json').read_text()) for i in range(4)]
    assert all(m['evidence_status'] == 'PASS' and m['frames'] == frames for m in metadata)
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'error']
    for column in range(4):
        command += ['-threads', '1', '-i', str(root / f'column_{column}.mp4')]
    command += ['-filter_complex_threads', '1', '-filter_complex', 'hstack=inputs=4',
                '-an', '-c:v', 'libx264', '-threads', '4', '-preset', 'fast', '-crf', '21',
                '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(output)]
    with (root / 'compose.log').open('w') as log:
        subprocess.run(command, stdout=log, stderr=log, check=True)
    info = verify_video(output, frames, WIDTH)
    write(root / 'video_verification.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
        video=output.name, sha256=paired.digest(output), frames=frames, fps=FPS, simulation_s=300,
        render_backend=[m['render_backend'] for m in metadata],
        render_pose_matches_recorded_base=True, layout='top baseline / bottom velocity bias; four paired columns', ffprobe=info))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--stage', choices=['collect', 'preview', 'render', 'compose'], required=True)
    parser.add_argument('--column', type=int, choices=range(4))
    args = parser.parse_args()
    root = args.output.resolve()
    if not root.is_relative_to(paired.REPO / 'docs/exp'):
        parser.error('docs/exp output required')
    if args.stage == 'collect':
        collect(root)
    elif args.stage == 'compose':
        compose(root)
    else:
        render(root, preview=args.stage == 'preview', column_index=args.column)


if __name__ == '__main__':
    main()
