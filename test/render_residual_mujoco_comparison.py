"""VALIDATION_SIM: deterministic torque replay of archived A/F-1/G, real MuJoCo video."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

os.environ.setdefault('MUJOCO_GL','egl')
import numpy as np
from PIL import Image,ImageDraw,ImageFont

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'test'))
from debug_lqr_d4_diagnostics import ARCHIVE,Plant
from sim2sim.lqr.runtime import policy_config
from sim2sim.lqr.model import Description
from sim2sim.lqr.evaluate import ground_truth,write_json
from sim2sim_ros2_jazzy.checkpoint import read_yaml,sha256

BASE=REPO/'docs/exp/2026-10-15/online_residual_gain/online_mass'
COLORS=[(70,160,255),(255,179,65),(92,218,164)]
W,H=640,360


def font(size):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',size)


def add_markers(plant,renderer,trace,tick):
    """Render-only geometry: origin cross and one-metre ruler; never contacts."""
    mj=plant.env.mujoco;scene=renderer.scene
    origin=trace['gt_position'][0]
    positions=[([origin[0],origin[1],.006],[.14,.007,.004],[1.,.75,.1,1.]),
               ([origin[0],origin[1],.006],[.007,.14,.004],[1.,.75,.1,1.])]
    for x in (-2.,-1.,0.,1.):
        positions.append(([origin[0]+x,origin[1],.008],[.006,.2,.004],[.15,.6,1.,.7]))
    for pos,size,color in positions:
        geom=scene.geoms[scene.ngeom]
        mj.mjv_initGeom(geom,mj.mjtGeom.mjGEOM_BOX,np.asarray(size),np.asarray(pos),np.eye(3).reshape(-1),np.asarray(color))
        scene.ngeom+=1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--duration',type=float,default=60.)
    args=parser.parse_args();output=args.output.resolve()
    if not output.is_relative_to(REPO/'docs/exp') or output.exists() or not 0.<args.duration<=60.:
        parser.error('New docs/exp output directory, duration in (0,60] required')
    output.mkdir(parents=True)
    cfg=json.loads((ARCHIVE/'config.json').read_text());parameters=json.loads((ARCHIVE/'manifest.json').read_text())['nominal_parameters']
    policy=policy_config();source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description=Description(source['scene']['robot']['spawn']['asset_path'])
    results=[r for r in map(json.loads,(BASE/'results.jsonl').read_text().splitlines()) if r['mismatch']=='nominal' and r['seed']==42 and r['pitch_delta_rad']==0.]
    ordered=[next(r for r in results if r['label']==label) for label in ('A','F-1','G')]
    plants=[];traces=[];renderers=[];fixed_cameras=[];close_cameras=[];errors=[]
    encoder=None;frames=0;started=time.monotonic()
    video=output/'nominal_A_F1_G_60s.mp4'
    try:
        for result in ordered:
            plant=Plant(policy,cfg,description,parameters,{'name':'nominal'},42,0.)
            plants.append(plant)
            np.testing.assert_array_equal(np.r_[plant.env.data.qpos,plant.env.data.qvel],result['initial_physics'])
            with np.load(BASE/result['trace']) as stored:
                trace={key:stored[key] for key in ('time','state','sensor_state','gt_state','gt_position','motor_substeps','alpha','alpha_centre')}
            traces.append(trace);errors.append(dict(state=0.,sensor_state=0.,gt_state=0.,gt_position=0.))
            plant.env.model.vis.global_.offwidth=W;plant.env.model.vis.global_.offheight=H
            plant.env.model.vis.global_.fovy=35.
            plant.env.model.vis.headlight.ambient[:]=.55
            plant.env.model.vis.headlight.diffuse[:]=.8
            plant.env.model.vis.headlight.specular[:]=.3
            # setup_scene already disabled these obstacles' contacts. Hide them
            # visually as well; no physics parameter is changed for rendering.
            plant.env.model.geom_rgba[plant.applied['disabled_obstacles'],3]=0.
            renderer=plant.env.mujoco.Renderer(plant.env.model,height=H,width=W);renderers.append(renderer)
            camera=plant.env.mujoco.MjvCamera();plant.env.mujoco.mjv_defaultCamera(camera)
            camera.lookat[:]=[-1.,-.08,.25];camera.distance=3.9;camera.azimuth=90.;camera.elevation=-25.
            fixed_cameras.append(camera)
            close=plant.env.mujoco.MjvCamera();plant.env.mujoco.mjv_defaultCamera(close)
            close.distance=1.4;close.azimuth=115.;close.elevation=-18.
            close_cameras.append(close)
        encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo',
            '-pix_fmt','rgb24','-s','1920x1080','-r','25','-i','-','-an','-c:v','libx264','-preset','fast','-crf','20',
            '-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE,stderr=(output/'ffmpeg.log').open('w'))
        n=round(args.duration/.02)
        for tick in range(n+1):
            t=tick*.02
            views=[]
            for i,(plant,trace) in enumerate(zip(plants,traces)):
                observation=plant.observe()
                position,_=ground_truth(plant.env,plant.wheels)
                for key,actual in [('state',observation['synchronized']),('sensor_state',observation['sensor']),
                                   ('gt_state',observation['gt']),('gt_position',position)]:
                    errors[i][key]=max(errors[i][key],float(abs(actual-trace[key][tick]).max()))
                if tick%2==0:
                    # Fresh geometry on clone only; original physics/cache remains untouched.
                    data=plant.truth_data
                    renderer=renderers[i]
                    renderer.update_scene(data,camera=fixed_cameras[i]);add_markers(plant,renderer,trace,tick)
                    wide=Image.fromarray(renderer.render())
                    close_cameras[i].lookat[:]=data.xpos[plant.base]+[0.,0.,-.1]
                    renderer.update_scene(data,camera=close_cameras[i]);add_markers(plant,renderer,trace,tick)
                    detail=Image.fromarray(renderer.render())
                    views.append((wide,detail))
            if tick%2==0:
                canvas=Image.new('RGB',(1920,1080),(15,21,31));draw=ImageDraw.Draw(canvas)
                draw.text((22,12),'MuJoCo | Zero command | Nominal | Same initial state',font=font(29),fill='white')
                draw.text((22,53),f't = {t:05.2f} / {args.duration:.0f} s   |   seed 42, pitch perturbation 0 rad   |   recorded motor-torque replay',font=font(20),fill=(187,199,213))
                for i,(result,trace,(wide,detail)) in enumerate(zip(ordered,traces,views)):
                    x=i*W;color=COLORS[i]
                    title={'A':'A  |  FlashSAC','F-1':'F-1  |  Fixed PD residual','G':'G  |  Online alpha residual'}[result['label']]
                    d=np.linalg.norm(trace['gt_position'][:tick+1,:2]-trace['gt_position'][0,:2],axis=1)
                    draw.text((x+12,92),title,font=font(25),fill=color)
                    draw.text((x+12,126),f'drift {d[-1]:.4f} m   |   max {d.max():.4f} m',font=font(21),fill='white')
                    canvas.paste(wide,(x,160));canvas.paste(detail,(x,552))
                    draw.text((x+12,525),'FIXED CAMERA  |  yellow cross = start; blue ticks = 1 m',font=font(15),fill=(170,185,203))
                    draw.text((x+12,918),'FOLLOW CAMERA  |  posture detail, same magnification',font=font(17),fill=(170,185,203))
                    if result['label']=='G':
                        draw.text((x+12,947),f'alpha {trace["alpha"][tick]:.2f}   centre {trace["alpha_centre"][tick]:.2f}',font=font(21),fill=color)
                    # Same drift scale and time scale in every panel.
                    box=(x+42,988,x+W-20,1050)
                    draw.rectangle(box,outline=(85,104,127))
                    points=[(box[0]+k*.02/60*(box[2]-box[0]),box[3]-value/2.6*(box[3]-box[1])) for k,value in enumerate(d)]
                    if len(points)>1:draw.line(points,fill=color,width=3)
                    draw.text((x+5,981),'2.6',font=font(12),fill=(160,177,197));draw.text((x+10,1039),'0',font=font(12),fill=(160,177,197))
                    draw.text((x+42,1054),'0 s                         Planar drift [m]                         60 s',font=font(12),fill=(160,177,197))
                if tick==0:canvas.save(output/'first_frame.png')
                if tick==n:canvas.save(output/'last_frame.png')
                encoder.stdin.write(canvas.tobytes());frames+=1
                if tick%250==0:
                    print(f'[VALIDATION_SIM] rendered {t:.0f}/{args.duration:.0f}s frames={frames} elapsed={time.monotonic()-started:.1f}s',flush=True)
            if tick==n:break
            for plant,trace in zip(plants,traces):
                env=plant.env;env.data.xfrc_applied[:]=0.
                force=cfg['disturbance']
                if force['start_s']<=t<force['start_s']+force['duration_s']:
                    env.data.xfrc_applied[plant.base,0]=force['force_n']
                for substep in range(env.decimation):
                    env.data.ctrl[env.actuator_ids]=trace['motor_substeps'][tick+1,substep]
                    env.mujoco.mj_step(env.model,env.data)
        encoder.stdin.close();assert encoder.wait()==0
        assert max(value for error in errors for value in error.values())==0.,errors
        write_json(output/'verification.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',
            checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],onnx_sha256=policy['policy_interface']['onnx_sha256'],
            script_sha256=sha256(Path(__file__)),frames=frames,fps=25,duration_simulation_s=args.duration,
            seed=42,pitch_delta_rad=0.,records=[{k:r[k] for k in ('label','max_displacement_m','trace')} for r in ordered],
            replay_max_errors=errors,video_sha256=sha256(video),
            rendering='MuJoCo EGL offscreen, clone data only; two views per controller',
            interpretation='One matched nominal trial. Table values 2.272/0.479/0.474 m are nine-trial means, not this individual trace.'))
        print('[VALIDATION_SIM] PASS exact torque replay and rendering',errors,flush=True)
    finally:
        if encoder and encoder.poll() is None:
            encoder.stdin.close();encoder.terminate();encoder.wait()
        for renderer in renderers:renderer.close()
        for plant in plants:plant.env.close()


if __name__=='__main__':
    main()
