"""DESKTOP_DRY_RUN: render saved VALIDATION_SIM states; never advances physics."""
import argparse
import json
import os
from pathlib import Path
import subprocess

os.environ.setdefault('MUJOCO_GL', 'egl')
os.environ.setdefault('LP_NUM_THREADS', '2')
import mujoco
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--traces', type=Path, nargs='+', required=True)
    parser.add_argument('--labels', nargs='+', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--end', type=float, default=5.)
    parser.add_argument('--columns', type=int, default=3)
    args = parser.parse_args()
    assert len(args.traces) == len(args.labels)
    args.output.mkdir(parents=True, exist_ok=True)
    cfg = json.loads((args.traces[0].parent/'config_used.json').read_text())
    model = mujoco.MjModel.from_xml_path(str(REPO/cfg['model']['scene_xml']))
    floor = model.geom('floor').id
    obstacles = np.flatnonzero((model.geom_bodyid == 0) & (np.arange(model.ngeom) != floor))
    model.geom_rgba[obstacles, 3] = 0.
    data = mujoco.MjData(model)
    renderer = mujoco.Renderer(model, height=330, width=480)
    camera = mujoco.MjvCamera()
    camera.distance, camera.azimuth, camera.elevation = 1.05, 105., -9.
    traces = [np.load(path) for path in args.traces]
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
    small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
    columns = min(args.columns, len(traces))
    rows = (len(traces)+columns-1)//columns
    width, height = columns*480, 70+rows*410
    video = args.output/'comparison.mp4'
    command = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
               '-s', f'{width}x{height}', '-r', '25', '-i', '-', '-an', '-c:v', 'libx264',
               '-crf', '20', '-pix_fmt', 'yuv420p', str(video)]
    pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
    contact_sheet = []
    try:
        times = np.arange(-.5, args.end+.01, 1/25)
        still_frames = {round((pivot+.5)*25) for pivot in (0., .5, 1., 2., 4.)}
        for frame_index, time in enumerate(times):
            canvas = Image.new('RGB', (width, height), (20, 25, 34))
            draw = ImageDraw.Draw(canvas)
            draw.text((12, 8), 'VALIDATION_SIM | same frozen FlashSAC / native sim2real controller', font=font, fill='white')
            draw.text((12, 38), f't = {time:+.2f} s from stop request | saved-state replay, 1x speed', font=small,
                      fill='#ffbe66' if abs(time) < .15 else '#c5ccd8')
            for n, (trace, label) in enumerate(zip(traces, args.labels)):
                k = int(abs(trace['sample_times']-time).argmin())
                data.qpos[:] = trace['qpos'][k]
                data.qvel[:] = trace['qvel'][k]
                mujoco.mj_forward(model, data)
                camera.lookat[:] = [data.qpos[0], data.qpos[1], .20]
                renderer.update_scene(data, camera=camera)
                frame = Image.fromarray(renderer.render())
                x, y = (n % columns)*480, 70+(n//columns)*410
                draw.text((x+8, y+4), label, font=font, fill='#8fceff' if 'CURRENT' in label else '#a5ebbe')
                canvas.paste(frame, (x, y+30))
                signal = trace['rows'][abs(trace['rows'][:, 0]-time).argmin()]
                draw.text((x+8, y+364), f'z={signal[4]*100:.1f} cm   pitch={np.degrees(signal[9]):+.1f} deg',
                          font=small, fill='white')
                draw.text((x+8, y+386), f'vz={signal[7]:+.2f} m/s   floor normal={signal[-1]:.0f} N',
                          font=small, fill='#c5ccd8')
            pipe.stdin.write(np.asarray(canvas).tobytes())
            if frame_index in still_frames:
                contact_sheet.append(canvas.copy())
        pipe.stdin.close()
        assert pipe.wait() == 0
        if contact_sheet:
            sheet = Image.new('RGB', (width, height*len(contact_sheet)))
            for index, frame in enumerate(contact_sheet):
                sheet.paste(frame, (0, height*index))
            sheet.save(args.output/'contact_sheet.png')
            contact_sheet[min(2, len(contact_sheet)-1)].save(args.output/'preview.png')
        print('DESKTOP_DRY_RUN PASS: saved-state video', video)
    finally:
        if pipe.poll() is None:
            pipe.kill(); pipe.wait()
        renderer.close()


if __name__ == '__main__':
    main()
