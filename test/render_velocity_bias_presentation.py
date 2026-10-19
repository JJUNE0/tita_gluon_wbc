"""VALIDATION_SIM: presentation edit of recorded poses; never advances physics."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

os.environ.setdefault('MUJOCO_GL', 'egl')
os.environ.setdefault('LP_NUM_THREADS', '2')

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import compare_velocity_bias_m4 as paired
import render_fixed_m4_drift_comparison as visual
from static_target_domain import StaticEnv

REPO = paired.REPO
SOURCE = REPO / 'docs/exp/2026-10-17/velocity_bias_grid_video'
OUTPUT = REPO / 'docs/exp/2026-10-17/velocity_bias_presentation'
W, H, CW, PH, FPS, SPEED = 1920, 1080, 480, 540, 30, 10
MAIN_DISTANCE = 2.05 * (PH - 4) / 400  # Preserve the approved robot size as headers are removed.
REALTIME_START_SECONDS = 2.
FRAMES = round((REALTIME_START_SECONDS + (300 - REALTIME_START_SECONDS) / SPEED) * FPS) + 1
OUTPUT_TIMES = np.arange(FRAMES) / FPS
SOURCE_TIMES = np.where(OUTPUT_TIMES <= REALTIME_START_SECONDS, OUTPUT_TIMES,
                        REALTIME_START_SECONDS + (OUTPUT_TIMES - REALTIME_START_SECONDS) * SPEED)
SAMPLES = np.rint(SOURCE_TIMES * 10).astype(int)
INTRO_FRAME_COUNT = round(REALTIME_START_SECONDS * FPS)
PREVIEW_FRAMES = [0, (FRAMES - 1) // 2, FRAMES - 1]
TITLES = ['NOMINAL', 'LOW FRICTION', 'CoM +5 mm', 'CoM −5 mm']
DETAILS = ['', 'Sliding μ = 0.2', 'Mass ×1.15', 'Mass ×1.15']
TARGETS = [{}, {'friction': .2}, {'mass': 1.15, 'com': .005}, {'mass': 1.15, 'com': -.005}]


def font(size, bold=False):
    suffix = 'Bold' if bold else 'Medium'
    return ImageFont.truetype(f'/usr/share/fonts/opentype/noto/NotoSansCJK-{suffix}.ttc', size, index=1)


F = {size: font(size) for size in [12, 14, 16, 18, 20, 23, 26, 32]}
B = {size: font(size, True) for size in [18, 23, 26, 32]}


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    paths = [SOURCE / 'plan.json', SOURCE / 'flashsac_vs_velocity_bias_2x4_05min.mp4']
    for condition in json.loads((SOURCE / 'plan.json').read_text())['conditions']:
        root = SOURCE / condition['name']
        paths += [root / 'config.json']
        paths += [root / f'group_{g}{ext}' for g in range(2) for ext in ['.npz', '_status.json']]
    return {str(p.relative_to(REPO)): digest(p) for p in paths}


def scene_image(record, renderer, camera, group, tick, path=False):
    renderer.update_scene(record['data'], camera=camera)
    mj = record['env'].mujoco
    for flag in [mj.mjtRndFlag.mjRND_SHADOW, mj.mjtRndFlag.mjRND_REFLECTION, mj.mjtRndFlag.mjRND_FOG]:
        renderer.scene.flags[flag] = 0
    trajectory = record['traces'][group]['state'][:tick + 1, :3] if path else None
    visual.markers(mj, renderer, record['origin'], trajectory, [(89, 177, 255), (87, 222, 169)][group])
    return Image.fromarray(renderer.render())


def prepare(column):
    plan = json.loads((SOURCE / 'plan.json').read_text())
    condition = plan['conditions'][column]
    assert condition['target'] == TARGETS[column], 'Condition label must match recorded physics'
    root = SOURCE / condition['name']
    traces, statuses = [], []
    for g in range(2):
        with np.load(root / f'group_{g}.npz') as archive:
            traces.append({key: archive[key] for key in ['qpos', 'qvel', 'sample_ticks', 'state']})
        statuses.append(json.loads((root / f'group_{g}_status.json').read_text()))
    assert all(s['evidence_status'] == 'PASS' and s['duration_s'] == 300 for s in statuses)
    assert statuses[0]['initial_physics_sha256'] == statuses[1]['initial_physics_sha256']
    assert statuses[0]['physics'] == statuses[1]['physics']
    intro_samples = round(REALTIME_START_SECONDS * 10) + 1
    for key in ['qpos', 'qvel']:
        np.testing.assert_array_equal(traces[0][key][:intro_samples], traces[1][key][:intro_samples])
    env = StaticEnv(json.loads((root / 'config.json').read_text()), condition['target'])
    mj, model = env.mujoco, env.model
    physics = statuses[0]['physics']
    assert float(model.body_mass[1:].sum()) == physics['total_mass_kg']
    np.testing.assert_array_equal(model.body_ipos[model.body('base_link').id], physics['base_com'])
    if 'fingerprint' in physics:
        assert env.fingerprint() == physics['fingerprint']
    model.geom_rgba[statuses[0]['disabled_obstacles'], 3] = 0
    model.vis.global_.offwidth, model.vis.global_.offheight = CW - 4, PH
    model.vis.global_.fovy = 38
    model.vis.quality.offsamples = 0
    model.vis.headlight.ambient[:] = .55
    model.vis.headlight.diffuse[:] = .8
    renderer = mj.Renderer(model, height=PH - 4, width=CW - 4)
    camera = mj.MjvCamera()
    mj.mjv_defaultCamera(camera)
    camera.distance, camera.azimuth, camera.elevation = MAIN_DISTANCE, 115., -20.
    world_renderer = mj.Renderer(model, height=180, width=240)
    world_camera = mj.MjvCamera()
    mj.mjv_defaultCamera(world_camera)
    origin = traces[0]['state'][0, :3].copy()
    paths = [t['state'][:, :2] - t['state'][0, :2] for t in traces]
    xy = np.concatenate(paths)
    extent = float(abs(xy).max())
    world_camera.distance, world_camera.azimuth, world_camera.elevation = max(2.6, extent * 3.), 90., -50.
    # Symmetric, fixed range around RL entry: every inset has its origin at the same center.
    world_camera.lookat[:] = np.r_[origin[:2], .008]
    return dict(env=env, renderer=renderer, camera=camera, world_renderer=world_renderer,
                world_camera=world_camera, origin=origin, data=mj.MjData(model), traces=traces,
                statuses=statuses, distances=[np.linalg.norm(p, axis=1) for p in paths])


def render(column, preview):
    record = prepare(column)
    env, renderer, camera = record['env'], record['renderer'], record['camera']
    mj, data = env.mujoco, record['data']
    output = OUTPUT / f'column_{column}.mp4'
    encoder = None
    from OpenGL import GL
    backend = GL.glGetString(GL.GL_RENDERER).decode()
    try:
        if not preview:
            if output.exists():
                raise FileExistsError(output)
            log = (OUTPUT / f'encode_{column}.log').open('w')
            encoder = subprocess.Popen(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'rawvideo',
                '-pix_fmt', 'rgb24', '-s', f'{CW}x{H}', '-r', str(FPS), '-i', '-', '-an', '-c:v', 'libx264',
                '-threads', '2', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart', str(output)], stdin=subprocess.PIPE, stderr=log)
        started = time.monotonic()
        for frame in (PREVIEW_FRAMES if preview else range(FRAMES)):
            sample = int(SAMPLES[frame])
            tick = sample * 5
            image = Image.new('RGB', (W, H), 'black')
            for group, trace in enumerate(record['traces']):
                assert trace['sample_ticks'][sample] == tick
                data.qpos[:] = trace['qpos'][sample]
                data.qvel[:] = trace['qvel'][sample]
                mj.mj_forward(env.model, data)
                base = data.xpos[env.model.body('base_link').id]
                np.testing.assert_allclose(base, trace['state'][tick, :3], atol=1e-12, rtol=0)
                angle = np.radians(camera.azimuth)
                right = np.array([-np.sin(angle), np.cos(angle), 0])
                camera.lookat[:] = base + right * .36 + [0, 0, -.08]
                np.testing.assert_allclose(camera.lookat - base, right * .36 + [0, 0, -.08], atol=1e-12)
                panel = scene_image(record, renderer, camera, group, tick)
                d = ImageDraw.Draw(panel)
                d.text((12, 10), TITLES[column], font=B[18], fill='white',
                       stroke_width=1, stroke_fill=(30, 40, 52))
                if DETAILS[column]:
                    d.text((12, 39), DETAILS[column], font=F[16], fill='white',
                           stroke_width=1, stroke_fill=(30, 40, 52))
                distance = record['distances'][group]
                for y, text, size in [(78, 'Distance from start', 18), (102, f'{distance[tick]:.3f} m', 32)]:
                    d.text((464, y), text, anchor='ra', font=B[size], fill='white',
                           stroke_width=1, stroke_fill=(30, 40, 52))
                world_camera = record['world_camera']
                np.testing.assert_array_equal(world_camera.lookat, np.r_[record['origin'][:2], .008])
                world = scene_image(record, record['world_renderer'], world_camera, group, tick, path=True)
                wd = ImageDraw.Draw(world)
                # Keep the start marker legible even when the true-scale robot is very small.
                wd.line((114, 90, 126, 90), fill=(255, 205, 65), width=2)
                wd.line((120, 84, 120, 96), fill=(255, 205, 65), width=2)
                inset_y = PH - 196
                panel.paste(world, (10, inset_y))
                d = ImageDraw.Draw(panel)
                d.text((12, inset_y - 23), 'FIXED WORLD', font=F[14], fill='white',
                       stroke_width=1, stroke_fill=(30, 40, 52))
                d.rectangle((9, inset_y - 1, 250, inset_y + 180), outline=(115, 138, 158), width=1)
                speed = 1 if frame < INTRO_FRAME_COUNT else SPEED
                d.text((464, PH - 44), f'x{speed}', anchor='ra', font=B[26], fill='black',
                       stroke_width=1, stroke_fill=(210, 220, 230))
                image.paste(panel, (column * CW + 2, group * PH + 2))
            crop = image.crop((column * CW, 0, (column + 1) * CW, H))
            if frame in PREVIEW_FRAMES:
                crop.save(OUTPUT / f'preview_{frame:03d}_column_{column}.png')
            if encoder:
                encoder.stdin.write(crop.tobytes())
            if frame % 150 == 0:
                print(f'[VALIDATION_SIM] column {column}: {frame}/{FRAMES}; wall {time.monotonic() - started:.1f}s', flush=True)
        if encoder:
            encoder.stdin.close()
            assert encoder.wait() == 0
            log.close()
            write(OUTPUT / f'column_{column}_verification.json', dict(execution_domain='VALIDATION_SIM',
                evidence_status='PASS', frames=FRAMES, render_backend=backend,
                all_rendered_base_positions_match=True, physics_match=True, sha256=digest(output),
                main_camera_distance_m=MAIN_DISTANCE, main_camera_anchor_matches=True, peak_removed=True,
                environment_label=TITLES[column], environment_detail=DETAILS[column],
                environment_label_position='top_left', controller_label_removed=True, simulation_time_label_removed=True,
                header_background_removed=True, bottom_speed_label='x1 then x10', speed_label_color='black',
                realtime_start_s=REALTIME_START_SECONDS, paired_standup_poses_identical=True,
                world_view=dict(fixed_camera=True, origin_centered=True, same_camera_for_both_rows=True,
                    distance_m=record['world_camera'].distance, azimuth_deg=90, elevation_deg=-50,
                    true_scale_robot=True, origin=record['world_camera'].lookat.tolist()),
                checkpoint_sha256=record['statuses'][0]['checkpoint_sha256']))
    finally:
        if encoder and encoder.poll() is None:
            encoder.terminate()
            encoder.wait()
        renderer.close()
        record['world_renderer'].close()
        env.close()


def compose(preview):
    for frame in PREVIEW_FRAMES:
        image = Image.new('RGB', (W, H), 'black')
        for column in range(4):
            with Image.open(OUTPUT / f'preview_{frame:03d}_column_{column}.png') as panel:
                image.paste(panel, (column * CW, 0))
        image.save(OUTPUT / f'preview_{frame:03d}.png')
    if preview:
        return
    metadata = [json.loads((OUTPUT / f'column_{c}_verification.json').read_text()) for c in range(4)]
    assert all(m['evidence_status'] == 'PASS' and m['frames'] == FRAMES for m in metadata)
    output = OUTPUT / 'flashsac_velocity_bias_2x4_10x_presentation.mp4'
    if output.exists():
        raise FileExistsError(output)
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error']
    for c in range(4):
        cmd += ['-threads', '1', '-i', str(OUTPUT / f'column_{c}.mp4')]
    cmd += ['-filter_complex_threads', '1', '-filter_complex', 'hstack=inputs=4', '-an', '-c:v', 'libx264',
            '-threads', '4', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(output)]
    with (OUTPUT / 'compose.log').open('w') as log:
        subprocess.run(cmd, stdout=log, stderr=log, check=True)
    probe = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
        '-show_entries', 'stream=codec_name,pix_fmt,width,height,nb_read_frames,r_frame_rate:format=duration,size',
        '-of', 'json', str(output)], capture_output=True, text=True, check=True)
    info = json.loads(probe.stdout)
    stream = info['streams'][0]
    assert (stream['width'], stream['height'], int(stream['nb_read_frames'])) == (W, H, FRAMES)
    assert stream['codec_name'] == 'h264' and stream['pix_fmt'] == 'yuv420p' and stream['r_frame_rate'] == '30/1'
    assert abs(float(info['format']['duration']) - FRAMES / FPS) < .01
    original = json.loads((OUTPUT / 'source_hashes.json').read_text())
    assert inputs() == original
    write(OUTPUT / 'video_verification.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
        source_hashes_unchanged=True, no_physics_steps=True, all_rendered_base_positions_match=True,
        source_frame_indices=SAMPLES.tolist(), speed=SPEED, simulation_s=300, same_xy_scale_within_column=True,
        realtime_start_s=REALTIME_START_SECONDS, source_frame_spacing_s=.1,
        speed_schedule=[dict(simulation_start_s=0, simulation_end_s=REALTIME_START_SECONDS, speed=1),
                        dict(simulation_start_s=REALTIME_START_SECONDS, simulation_end_s=300, speed=SPEED)],
        video_sha256=digest(output), ffprobe=info, columns=metadata))


def main():
    global OUTPUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=['init', 'preview', 'render', 'compose', 'preview-compose'], required=True)
    parser.add_argument('--column', type=int, choices=range(4))
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    OUTPUT = args.output.resolve()
    if not OUTPUT.is_relative_to(REPO / 'docs/exp'):
        parser.error('docs/exp output required')
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if args.stage == 'init':
        if (OUTPUT / 'source_hashes.json').exists():
            raise FileExistsError(OUTPUT / 'source_hashes.json')
        write(OUTPUT / 'source_hashes.json', inputs())
    elif args.stage in ['preview', 'render']:
        if args.column is None:
            parser.error('--column required')
        render(args.column, args.stage == 'preview')
    else:
        compose(args.stage == 'preview-compose')


if __name__ == '__main__':
    main()
