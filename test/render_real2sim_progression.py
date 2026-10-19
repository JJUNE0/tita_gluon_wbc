"""VALIDATION_SIM: presentation video "Real2Sim-guided policy refinement" (2x4 grid, 5-minute zero command, x10).

Rows: FlashSAC baseline (model_60000, 33 observations, as in the 2026-10-17 velocity-bias video) and the Real2Sim-refined
FlashSAC (headw0 model_50000: knee PD/DR, sphere wheel contact, x_err + gyro heading observations, heading reward).
Columns add, left to right, the real-robot gaps identified by Real2Sim (sim2real/gap.md):
  NOMINAL (MuJoCo, cylinder wheels) -> + weak knee (L 0.60 / R 0.75, G1) -> + point wheel contact (sphere collider,
  low yaw scrub, G4) -> + leg high-frequency overreaction (25 Hz proxy raw + g * (raw - previous raw), g = 1.5, G2).
  (The open backward-bias gap G6 is not shown: with IMU +3 deg both policies creep >20 m in 5 min, and the refined
  policy's outcome flips between +2 and +2.5 deg; see docs/exp/2026-10-19/real2sim_progression_video.md.)
Stages:
  collect: 8 rollouts with test/screen_sphere_wheel_runs.py ``rollout`` (scenario stand300, MuJoCo physics, no robot);
  preview / render --column C: draw recorded qpos only (no physics steps), one H.264 column per process;
  compose: hstack the four columns and verify with ffprobe.
--scene-xml: MuJoCo scene to use instead of the exported config's path (the corrected TITA model was removed from the
  working tree in commit 88d7f240; extract it from c8c159d3 with ``git archive`` and pass it here). Patched configs are
  written to <output>/configs/ and the scene/robot XML git blob hashes are recorded in plan.json.
usage: python test/render_real2sim_progression.py --output docs/exp/<date>/<dir> --stage collect|preview|render|compose
       [--scene-xml PATH]
"""

import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

os.environ.setdefault('MUJOCO_GL', 'egl')
os.environ.setdefault('LP_NUM_THREADS', '2')

import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'test'))
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
LOGS = REPO / 'lab/ddt_lab/logs/flash_sac'
ROWS = [dict(tag='flashsac_baseline', step=60000, label='FlashSAC (baseline)',
             config=LOGS / 'tita_flash_sac_115632_883848/model_60000/sim2sim/actor/config.json'),
        dict(tag='flashsac_real2sim', step=50000, label='FlashSAC + Real2Sim',
             config=LOGS / 'tita_flash_sac_125547_806511/model_50000/sim2sim/actor/config.json')]
COLUMNS = [dict(plant='B_nom', title='NOMINAL', detail='MuJoCo default'),
           dict(plant='B', title='+ WEAK KNEE', detail='Knee torque L 0.60 · R 0.75'),
           dict(plant='A', title='+ POINT WHEEL CONTACT', detail='Low yaw scrub (sphere)'),
           dict(plant='A', g=1.5, title='+ LEG HF OVERREACTION', detail='25 Hz action gain g = 1.5')]
SCENARIO, DURATION, DT = 'stand300', 300., .02
W, H, CW, PH, FPS, SPEED = 1920, 1080, 480, 540, 30, 10
MAIN_DISTANCE = 2.05 * (PH - 4) / 400
REALTIME_START_SECONDS = 2.
FRAMES = round((REALTIME_START_SECONDS + (DURATION - REALTIME_START_SECONDS) / SPEED) * FPS) + 1
OUTPUT_TIMES = np.arange(FRAMES) / FPS
SOURCE_TIMES = np.where(OUTPUT_TIMES <= REALTIME_START_SECONDS, OUTPUT_TIMES,
                        REALTIME_START_SECONDS + (OUTPUT_TIMES - REALTIME_START_SECONDS) * SPEED)
SAMPLES = np.minimum(np.rint(SOURCE_TIMES / DT).astype(int), round(DURATION / DT) - 1)
INTRO_FRAME_COUNT = round(REALTIME_START_SECONDS * FPS)
PREVIEW_FRAMES = [0, (FRAMES - 1) // 2, FRAMES - 1]
COLORS = [(89, 177, 255), (87, 222, 169)]
OUTPUT = None
SCENE_XML = None
VARIANT = ''            # --variant nolabel: no condition title/detail at the top right; files get a _nolabel suffix
SHOW_CONDITION = True


def font(size, bold=False):
    suffix = 'Bold' if bold else 'Medium'
    return ImageFont.truetype(f'/usr/share/fonts/opentype/noto/NotoSansCJK-{suffix}.ttc', size, index=1)


F = {size: font(size) for size in [14, 16, 18]}
B = {size: font(size, True) for size in [18, 26, 32]}


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_config(row):
    """Exported config, with the scene path replaced when --scene-xml is given (written under <output>/configs/)."""
    if SCENE_XML is None:
        return row['config']
    path = OUTPUT / 'configs' / f"{row['tag']}.json"
    if not path.exists():
        cfg = json.loads(row['config'].read_text())
        cfg['model']['scene_xml'] = str(SCENE_XML)
        path.parent.mkdir(exist_ok=True)
        write(path, cfg)
    return path


def git_blob(path):
    return subprocess.run(['git', 'hash-object', str(path)], capture_output=True, text=True, check=True).stdout.strip()


def job(row, column):
    return dict(tag=row['tag'], step=row['step'], config=str(run_config(row)), output=str(OUTPUT),
                plant=column['plant'], scenario=SCENARIO, g=float(column.get('g', 0.)), save=True)


def signal_path(row, column):
    return OUTPUT / 'signals' / f"{row['tag']}_{row['step']}_{column['plant']}_{SCENARIO}_g{column.get('g', 0.):g}.npz"


def collect(workers):
    import screen_sphere_wheel_runs as screen
    assert screen.SCENARIOS[SCENARIO]['duration'] == DURATION
    (OUTPUT / 'signals').mkdir(parents=True, exist_ok=True)
    if (OUTPUT / 'plan.json').exists():
        raise FileExistsError(OUTPUT / 'plan.json')
    rows = []
    for row in ROWS:
        cfg = json.loads(row['config'].read_text())
        pi = cfg['policy_interface']
        rows.append(dict(label=row['label'], tag=row['tag'], step=row['step'], config=str(row['config'].relative_to(REPO)),
                         config_sha256=digest(row['config']), checkpoint_sha256=pi['checkpoint_sha256'],
                         onnx_sha256=pi['onnx_sha256'], obs_dim=cfg['policy']['obs_dim'],
                         leg_action_filter=pi.get('leg_action_filter', 'none')))
    columns = [dict(column, physics=screen.PLANTS[column['plant']]) for column in COLUMNS]
    scene = Path(SCENE_XML or REPO / json.loads(ROWS[1]['config'].read_text())['model']['scene_xml'])
    model = dict(scene_xml=str(scene), scene_git_blob=git_blob(scene), robot_git_blob=git_blob(scene.parent / 'robot.xml'))
    write(OUTPUT / 'plan.json', dict(execution_domain='VALIDATION_SIM', scenario=SCENARIO,
                                     schedule=screen.SCENARIOS[SCENARIO], rows=rows, columns=columns, model=model))
    jobs = [job(row, column) for column in COLUMNS for row in ROWS]
    started = time.monotonic()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(screen.rollout, jobs))
    for r in results:
        print(f"[VALIDATION_SIM] {r['job']['tag']} {r['job']['plant']} {r['evidence_status']} {r.get('failure')} "
              f"{time.monotonic() - started:.0f}s", flush=True)
    write(OUTPUT / 'results.json', results)
    assert all(r['evidence_status'] == 'PASS' for r in results), 'rollout failed'
    entry = {}
    for column in COLUMNS:
        q = [np.load(signal_path(row, column))['qpos'][0] for row in ROWS]
        entry[signal_path(ROWS[0], column).stem.split('_stand300_')[0].split('_', 3)[-1] + f"_g{column.get('g', 0.):g}"] = \
            float(np.abs(q[0] - q[1]).max())
    write(OUTPUT / 'source_hashes.json', {str(signal_path(r, c).relative_to(REPO)): digest(signal_path(r, c))
                                          for c in COLUMNS for r in ROWS})
    write(OUTPUT / 'rl_entry_qpos_max_abs_diff.json', entry)
    print(json.dumps(entry))


def yaw_deg(qpos):
    w, x, y, z = qpos[:, 3:7].T
    return np.degrees(np.unwrap(np.arctan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))))


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
            mj.mjv_connector(geom, mj.mjtGeom.mjGEOM_LINE, 2., np.r_[first[:2], .018], np.r_[second[:2], .018])
            scene.ngeom += 1


def scene_image(mj, renderer, data, camera, origin, path=None, color=None):
    renderer.update_scene(data, camera=camera)
    for flag in [mj.mjtRndFlag.mjRND_SHADOW, mj.mjtRndFlag.mjRND_REFLECTION, mj.mjtRndFlag.mjRND_FOG]:
        renderer.scene.flags[flag] = 0
    markers(mj, renderer, origin, path, color)
    return Image.fromarray(renderer.render())


def prepare(column):
    import mujoco as mj
    from sim2sim_ros2_jazzy.mujoco_env import TitaMujocoEnv
    sources = json.loads((OUTPUT / 'source_hashes.json').read_text())
    traces = []
    for row in ROWS:
        path = signal_path(row, COLUMNS[column])
        assert digest(path) == sources[str(path.relative_to(REPO))]
        with np.load(path) as z:
            traces.append(dict(qpos=z['qpos'], position=z['position'], t=z['t']))
        assert len(traces[-1]['qpos']) == round(DURATION / DT)
    env = TitaMujocoEnv(json.loads(Path(run_config(ROWS[1])).read_text()))
    model = env.model
    floor = model.geom('floor').id
    obstacles = np.flatnonzero((model.geom_bodyid == 0) & (np.arange(model.ngeom) != floor))
    model.geom_rgba[obstacles, 3] = 0
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
    origins = [t['qpos'][0, :3].copy() for t in traces]
    paths = [t['qpos'][:, :2] - o[:2] for t, o in zip(traces, origins)]
    extent = float(np.abs(np.concatenate(paths)).max())
    world_camera.distance, world_camera.azimuth, world_camera.elevation = max(2.6, extent * 3.), 90., -50.
    return dict(mj=mj, env=env, model=model, data=mj.MjData(model), renderer=renderer, camera=camera,
                world_renderer=world_renderer, world_camera=world_camera, traces=traces, origins=origins,
                distances=[np.linalg.norm(p, axis=1) for p in paths], headings=[yaw_deg(t['qpos']) - yaw_deg(t['qpos'])[0]
                                                                            for t in traces])


def text(d, xy, value, f, anchor='la', fill='white'):
    d.text(xy, value, anchor=anchor, font=f, fill=fill, stroke_width=1, stroke_fill=(30, 40, 52))


def render(column, preview):
    record = prepare(column)
    mj, model, data = record['mj'], record['model'], record['data']
    renderer, camera = record['renderer'], record['camera']
    spec = COLUMNS[column]
    output = OUTPUT / f'column_{column}{VARIANT}.mp4'
    encoder = log = None
    base_id = model.body('base_link').id
    try:
        if not preview:
            if output.exists():
                raise FileExistsError(output)
            log = (OUTPUT / f'encode_{column}{VARIANT}.log').open('w')
            encoder = subprocess.Popen(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'rawvideo',
                                        '-pix_fmt', 'rgb24', '-s', f'{CW}x{H}', '-r', str(FPS), '-i', '-', '-an',
                                        '-c:v', 'libx264', '-threads', '2', '-preset', 'fast', '-crf', '18',
                                        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(output)],
                                       stdin=subprocess.PIPE, stderr=log)
        started = time.monotonic()
        max_base_err = 0.
        for frame in (PREVIEW_FRAMES if preview else range(FRAMES)):
            sample = int(SAMPLES[frame])
            image = Image.new('RGB', (W, H), 'black')
            for group, trace in enumerate(record['traces']):
                data.qpos[:] = trace['qpos'][sample]
                data.qvel[:] = 0.
                mj.mj_forward(model, data)
                base = data.xpos[base_id].copy()
                max_base_err = max(max_base_err, float(np.abs(base - trace['position'][sample]).max()))
                angle = np.radians(camera.azimuth)
                right = np.array([-np.sin(angle), np.cos(angle), 0])
                camera.lookat[:] = base + right * .36 + [0, 0, -.08]
                panel = scene_image(mj, renderer, data, camera, record['origins'][group])
                d = ImageDraw.Draw(panel)
                text(d, (12, 10), ROWS[group]['label'], B[18])
                text(d, (12, 39), f'SIM {trace["t"][sample]:05.1f} s', F[14])
                if SHOW_CONDITION:
                    text(d, (464, 10), spec['title'], B[18], 'ra')
                    text(d, (464, 39), spec['detail'], F[16], 'ra')
                top = 78 if SHOW_CONDITION else 10          # nolabel: metrics move up into the freed top-right area
                text(d, (464, top), 'Distance from start', B[18], 'ra')
                text(d, (464, top + 24), f"{record['distances'][group][sample]:.3f} m", B[32], 'ra')
                text(d, (464, top + 68), 'Heading change', B[18], 'ra')
                text(d, (464, top + 90), f"{record['headings'][group][sample]:+.1f}°", B[26], 'ra')
                world = scene_image(mj, record['world_renderer'], data, record['world_camera'],
                                    record['origins'][group], trace['qpos'][:sample + 1, :3], COLORS[group])
                wd = ImageDraw.Draw(world)
                wd.line((114, 90, 126, 90), fill=(255, 205, 65), width=2)
                wd.line((120, 84, 120, 96), fill=(255, 205, 65), width=2)
                inset_y = PH - 196
                panel.paste(world, (10, inset_y))
                d = ImageDraw.Draw(panel)
                text(d, (12, inset_y - 23), 'FIXED WORLD', F[14])
                d.rectangle((9, inset_y - 1, 250, inset_y + 180), outline=(115, 138, 158), width=1)
                speed = 1 if frame < INTRO_FRAME_COUNT else SPEED
                d.text((464, PH - 44), f'x{speed}', anchor='ra', font=B[26], fill='black',
                       stroke_width=1, stroke_fill=(210, 220, 230))
                image.paste(panel, (column * CW + 2, group * PH + 2))
            crop = image.crop((column * CW, 0, (column + 1) * CW, H))
            if frame in PREVIEW_FRAMES:
                crop.save(OUTPUT / f'preview_{frame:03d}_column_{column}{VARIANT}.png')
            if encoder:
                encoder.stdin.write(crop.tobytes())
            if frame % 150 == 0:
                print(f'[VALIDATION_SIM] column {column}: {frame}/{FRAMES}; wall {time.monotonic() - started:.1f}s',
                      flush=True)
        assert max_base_err < 1e-5, max_base_err
        if encoder:
            encoder.stdin.close()
            assert encoder.wait() == 0
            write(OUTPUT / f'column_{column}{VARIANT}_verification.json', dict(
                execution_domain='VALIDATION_SIM', evidence_status='PASS', frames=FRAMES, no_physics_steps=True,
                rendered_base_vs_recorded_max_abs_m=max_base_err, plant=spec['plant'], title=spec['title'],
                detail=spec['detail'], condition_label_shown=SHOW_CONDITION,
                metrics_top_px=78 if SHOW_CONDITION else 10, final_distance_m=[float(x[-1]) for x in record['distances']],
                final_heading_deg=[float(x[-1]) for x in record['headings']],
                world_camera_distance_m=float(record['world_camera'].distance), sha256=digest(output)))
    finally:
        if encoder and encoder.poll() is None:
            encoder.terminate()
            encoder.wait()
        if log:
            log.close()
        renderer.close()
        record['world_renderer'].close()
        record['env'].close()


def compose(preview):
    for frame in PREVIEW_FRAMES:
        image = Image.new('RGB', (W, H), 'black')
        for column in range(4):
            with Image.open(OUTPUT / f'preview_{frame:03d}_column_{column}{VARIANT}.png') as panel:
                image.paste(panel, (column * CW, 0))
        image.save(OUTPUT / f'preview_{frame:03d}{VARIANT}.png')
    if preview:
        return
    metadata = [json.loads((OUTPUT / f'column_{c}{VARIANT}_verification.json').read_text()) for c in range(4)]
    assert all(m['evidence_status'] == 'PASS' and m['frames'] == FRAMES for m in metadata)
    output = OUTPUT / f'flashsac_real2sim_progression_2x4_10x{VARIANT}.mp4'
    if output.exists():
        raise FileExistsError(output)
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error']
    for c in range(4):
        cmd += ['-threads', '1', '-i', str(OUTPUT / f'column_{c}{VARIANT}.mp4')]
    cmd += ['-filter_complex', 'hstack=inputs=4', '-an', '-c:v', 'libx264', '-threads', '4', '-preset', 'fast',
            '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(output)]
    with (OUTPUT / f'compose{VARIANT}.log').open('w') as log:
        subprocess.run(cmd, stdout=log, stderr=log, check=True)
    probe = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries',
                            'stream=codec_name,pix_fmt,width,height,nb_read_frames,r_frame_rate:format=duration,size',
                            '-of', 'json', str(output)], capture_output=True, text=True, check=True)
    info = json.loads(probe.stdout)
    stream = info['streams'][0]
    assert (stream['width'], stream['height'], int(stream['nb_read_frames'])) == (W, H, FRAMES)
    assert stream['codec_name'] == 'h264' and stream['pix_fmt'] == 'yuv420p' and stream['r_frame_rate'] == '30/1'
    assert abs(float(info['format']['duration']) - FRAMES / FPS) < .01
    sources = json.loads((OUTPUT / 'source_hashes.json').read_text())
    assert all(digest(REPO / k) == v for k, v in sources.items())
    write(OUTPUT / f'video_verification{VARIANT}.json', dict(
        execution_domain='VALIDATION_SIM', evidence_status='PASS', source_hashes_unchanged=True, no_physics_steps=True,
        condition_label_shown=SHOW_CONDITION, speed=SPEED, simulation_s=DURATION, realtime_start_s=REALTIME_START_SECONDS, frames=FRAMES,
        video_sha256=digest(output), ffprobe=info, columns=metadata))


def main():
    global OUTPUT
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--stage', choices=['collect', 'preview', 'render', 'compose', 'preview-compose'], required=True)
    ap.add_argument('--column', type=int, choices=range(4))
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--scene-xml', type=Path)
    ap.add_argument('--variant', choices=['nolabel'], help='nolabel: hide the condition title/detail (top right)')
    a = ap.parse_args()
    global SCENE_XML, VARIANT, SHOW_CONDITION
    SCENE_XML = a.scene_xml.resolve() if a.scene_xml else None
    VARIANT = f'_{a.variant}' if a.variant else ''
    SHOW_CONDITION = a.variant != 'nolabel'
    OUTPUT = a.output.resolve()
    if not OUTPUT.is_relative_to(REPO / 'docs/exp'):
        ap.error('docs/exp output required')
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if a.stage == 'collect':
        collect(a.workers)
    elif a.stage in ('preview', 'render'):
        if a.column is None:
            ap.error('--column required')
        render(a.column, a.stage == 'preview')
    else:
        compose(a.stage == 'preview-compose')


if __name__ == '__main__':
    main()
