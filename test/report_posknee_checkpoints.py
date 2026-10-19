"""VALIDATION_SIM: export checkpoint comparison tables and scientific plots from measured rollouts."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    out=args.output.resolve()
    report=json.loads((out/'summary.json').read_text())
    results=json.loads((out/'results.json').read_text())
    policies=json.loads((out/'policies.json').read_text())
    steps=sorted(int(k) for k in report['by_checkpoint'])
    short=['L hip','L thigh','L knee','L wheel','R hip','R thigh','R knee','R wheel']
    rows=[]
    for step in steps:
        for scale in (1.,.75,.55):
            d=report['by_checkpoint'][str(step)]['domains'][str(scale)]
            if d['failures']:
                continue
            for j,name in enumerate(report['joint_order']):
                rows.append(dict(step=step,knee_scale=scale,joint=name,
                    mean_angle_rad=d['stand_joint_mean_rad'][j],std_angle_rad=d['stand_joint_std_rad'][j],
                    mean_angle_deg=float(np.degrees(d['stand_joint_mean_rad'][j])),
                    std_angle_deg=float(np.degrees(d['stand_joint_std_rad'][j])),
                    stand_torque_rms_nm=d['stand_torque_rms_nm'][j],
                    stand_torque_abs_peak_nm=d['stand_torque_abs_peak_nm'][j],
                    all_rl_torque_abs_peak_nm=d['full_torque_abs_peak_nm'][j]))
    with (out/'joint_angles_torques.csv').open('w') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    fig,axes=plt.subplots(2,2,figsize=(11,7),constrained_layout=True)
    keys=[('stand_speed_rms_m_s',1000.,'Standing speed RMS [mm/s]'),
          ('stop_speed_rms_m_s',1000.,'After-stop speed RMS [mm/s]'),
          ('stand_pitch_rms_deg',1.,'Standing pitch RMS vs 0 deg [deg]'),
          ('leg_torque_rms_nm',1.,'Standing leg torque RMS [Nm]')]
    for ax,(key,factor,title) in zip(axes.flat,keys):
        for scale in (1.,.75,.55):
            values=[report['by_checkpoint'][str(step)]['domains'][str(scale)].get(key,np.nan)*factor for step in steps]
            ax.plot(np.array(steps)/1000,values,'o-',label=f'Knee PD x {scale:g}',markersize=4)
        ax.set_title(title);ax.set_xlabel('Checkpoint [k steps]');ax.grid(alpha=.25)
        ax.legend(fontsize=8)
    fig.suptitle('PosKneeMA2 checkpoint comparison | 3 seeds per condition | flat MuJoCo')
    fig.savefig(out/'checkpoint_comparison.png',dpi=180)
    fig.savefig(out/'checkpoint_comparison.svg')
    plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,5),constrained_layout=True)
    nominal=[report['by_checkpoint'][str(step)]['domains']['1.0'] for step in steps]
    legs=[0,1,2,4,5,6]
    data=[np.degrees(np.array([d['stand_joint_mean_rad'] for d in nominal]))[:,legs],
          np.array([d['stand_torque_rms_nm'] for d in nominal])]
    for ax,a,labels,title in zip(axes,data,[[short[j] for j in legs],short],
            ['Standing leg angle means [deg]','Standing joint torque RMS [Nm]']):
        im=ax.imshow(a,aspect='auto',cmap='coolwarm' if a.min()<0 else 'viridis')
        ax.set_xticks(range(len(labels)),labels,rotation=35,ha='right')
        ax.set_yticks(range(len(steps)),[f'{s//1000}k' for s in steps]);ax.set_title(title)
        for i in range(len(steps)):
            for j in range(a.shape[1]):
                ax.text(j,i,f'{a[i,j]:.1f}',ha='center',va='center',fontsize=8,
                    color='white' if a[i,j]>(a.max()+a.min())/2 else 'black')
        fig.colorbar(im,ax=ax,shrink=.8)
    fig.savefig(out/'joint_angles_torques.png',dpi=180);plt.close(fig)
    chosen=report['ranking'][0]
    # Plot all seeds for the automatically ranked candidate to expose variability.
    selected=[r for r in results if r['step']==chosen and r['scenario']=='drive' and r['knee_scale']==1.]
    fig,axes=plt.subplots(4,1,figsize=(12,9),sharex=True,constrained_layout=True)
    for r in selected:
        s=np.load(Path(__file__).resolve().parents[1]/r['signal_file'])
        t=s['t'];label=f"seed {r['seed']}"
        axes[0].plot(t,s['velocity_body'][:,0],alpha=.7,label=label)
        axes[1].plot(t,s['gyro'][:,2],alpha=.7)
        axes[2].plot(t,s['rpy_deg'][:,1],alpha=.7)
        axes[3].plot(t,np.sqrt(np.mean(s['torque'].mean(axis=1)[:,legs]**2,axis=1)),alpha=.7)
    axes[0].plot(t,s['command'][:,0],'k--',label='command')
    axes[1].plot(t,s['command'][:,2],'k--')
    for ax,label in zip(axes,['Forward velocity [m/s]','Yaw rate [rad/s]','Pitch vs 0 [deg]','Leg torque RMS [Nm]']):
        ax.set_ylabel(label);ax.grid(alpha=.2)
    axes[0].legend(loc='upper right',ncol=4);axes[-1].set_xlabel('Seconds after RL entry')
    fig.suptitle(f'Automatically ranked candidate {chosen//1000}k | nominal MuJoCo')
    fig.savefig(out/'selected_trajectory.png',dpi=160);plt.close(fig)
    lines=['# PosKneeMA2 40k–85k 체크포인트 비교','',
        'Execution Domain: VALIDATION_SIM','',
        f'Evidence Status: {"PASS" if all(r["evidence_status"]=="PASS" for r in results) else "SUSPICIOUS"} (sim screening); hardware NOT_TESTED.','',
        'Run: `tita_flash_sac_180212_290240` · task `DDT-Velocity-Flat-Tita-My-PosKneeMA2-v0` · branch `agent/codex/dev_tita_gluon`','',
        '10 checkpoints × 3 seeds (42/104/270) × knee PD scales (1.0/0.75/0.55) × stand/drive = 180 rollouts. '
        'Stand: 32 s, measured after 8 s (24 s). Drive: 106 s, commands ±0.6/±1.0 m/s and ±1.0/±1.5 rad/s, '
        '0.5/s ramp; after-stop metrics use the last 3 s of each stop. '
        'The world-body obstacles are disabled only in the evaluation plant to compare flat-ground policies. '
        'Production source code and robot configuration are unchanged.','',
        'Pitch error uses horizontal 0°, consistent with flat orientation. Drift displacement is GT base world-x '
        'over the settled 24 s; speed RMS is GT planar speed (used only as evaluation data). '
        'Joint angles are absolute encoder angles, not action offsets. Torque is MA2 → action mapping → '
        '`clip(Kp*(q_target-q)+Kd*(qd_target-dq), ±effort_limit)` sampled every physics substep. '
        'The knee sensitivity changes Kp/Kd before clipping, exactly matching the training event semantics. '
        'It is not a measured hardware motor coefficient.','',
        f'Automated ranking (predeclared zero-command speed criterion): **{chosen//1000}k** first. '
        'See `evaluation_protocol.json` for the selection rule; trajectory tracking, pitch and torque are reported separately.','',
        '## Nominal plant, mean of 3 seeds','',
        '| ckpt | drift Δx /24s [cm] | stand speed RMS [mm/s] | after-stop speed RMS [mm/s] | pitch mean ± temporal std [°] | leg torque RMS [Nm] | wheel torque RMS [Nm] | failures /18 |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for step,d in zip(steps,nominal):
        row=report['by_checkpoint'][str(step)]
        lines.append(f'| {step//1000}k | {d["stand_displacement_x_m"]*100:+.3f} | {d["stand_speed_rms_m_s"]*1000:.3f} | '
            f'{d["stop_speed_rms_m_s"]*1000:.3f} | {d["stand_pitch_mean_deg"]:+.3f} ± {d["stand_pitch_std_deg"]:.3f} | '
            f'{d["leg_torque_rms_nm"]:.3f} | {d["wheel_torque_rms_nm"]:.3f} | {row["failed_rollouts"]} |')
    lines+=['','## Nominal standing joint means [deg]','',
        '| ckpt | L hip | L thigh | L knee | R hip | R thigh | R knee |','|---|---:|---:|---:|---:|---:|---:|']
    for step,d in zip(steps,nominal):
        angles=np.degrees(d['stand_joint_mean_rad'])
        lines.append(f'| {step//1000}k | '+' | '.join(f'{angles[j]:.2f}' for j in legs)+' |')
    lines+=['','## Nominal standing torque RMS [Nm]','',
        '| ckpt | L hip | L thigh | L knee | L wheel | R hip | R thigh | R knee | R wheel |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for step,d in zip(steps,nominal):
        lines.append(f'| {step//1000}k | '+' | '.join(f'{x:.3f}' for x in d['stand_torque_rms_nm'])+' |')
    lines+=['','## Sensitivity: speed RMS while stopped [mm/s]','',
        'Each cell: stand / post-move stop. Equal scene/seeds/commands; only the two knee PD gains change.','',
        '| ckpt | knee x1.0 | knee x0.75 | knee x0.55 | worst zero-speed score [mm/s] |',
        '|---|---:|---:|---:|---:|']
    for step in steps:
        item=report['by_checkpoint'][str(step)];cells=[]
        for scale in (1.,.75,.55):
            d=item['domains'][str(scale)]
            cells.append('FAIL' if d['failures'] else f'{d["stand_speed_rms_m_s"]*1000:.3f} / {d["stop_speed_rms_m_s"]*1000:.3f}')
        lines.append(f'| {step//1000}k | '+' | '.join(cells)+f' | {item["worst_zero_speed_score_m_s"]*1000:.3f} |')
    lines+=['','## Evidence and limits','',
        '`policies.json`: checkpoint/ONNX/config hashes and all native-vs-ONNX parity results (256 inputs each). '
        '`results.json`: every rollout, per-joint angle and torque statistics, stop windows and tracking. '
        '`joint_angles_torques.csv`: all checkpoints × knee scales × 8 joints, mean/std and torque RMS/peaks. '
        '`signals/*.npz`: complete policy-tick states/actions and physics-substep torques. '
        '`summary.csv`, `summary.json`: comparison and ranking.','',
        'The screening harness was checked against the actual public Sim2SimNode for the 75k nominal '
        'seed-42 stand: 1600 RL ticks match exactly in joint state, raw action, applied action and PD torque '
        '(`public_node_replay.log`). All policy observations are the saved 34-element encoder/IMU definition; '
        'no GT velocity is fed into the actor.','',
        'An initial smoke criterion (base height <0.18 m) rejected the legitimate crouched RL entry at 0.179 m. '
        'Before the sweep it was replaced with actual base-floor collision and the 0.65-rad tilt guard. '
        'The original smoke/protocol are retained as `smoke.log`, `evaluation_protocol_initial_height_guard.json`. '
        'No selection was made from that invalid smoke.','',
        'No motor calibration, extra delay, IMU noise, backlash/compliance or physical 25 Hz chatter is modelled. '
        'Three small initial-state perturbations do not establish hardware confidence. The result selects a '
        'candidate for staged experiments, not a deployment approval. No robot access, deployment, commit or publication.','',
        '## Policy provenance','',
        '| ckpt | Policy Checkpoint SHA256 | ONNX SHA256 |','|---|---|---|']
    for p in policies:
        lines.append(f'| {p["step"]//1000}k | `{p["checkpoint_sha256"]}` | `{p["onnx_sha256"]}` |')
    lines+=['','## Figures','',
        '![Checkpoint comparison](posknee_checkpoint_screen/checkpoint_comparison.png)','',
        '![Joint angles and torques](posknee_checkpoint_screen/joint_angles_torques.png)','',
        '![Selected candidate trajectory](posknee_checkpoint_screen/selected_trajectory.png)','']
    (out.parent/'posknee_checkpoint_screen.md').write_text('\n'.join(lines))
    write_manifest={str(p.relative_to(Path(__file__).resolve().parents[1])):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in [Path(__file__),Path(__file__).with_name('evaluate_posknee_checkpoints.py'),
            Path(__file__).with_name('check_posknee_screen_replay.py')]}
    (out/'analysis_sources.json').write_text(json.dumps(write_manifest,indent=2)+'\n')
    print(f'[VALIDATION_SIM] Tables, figures and report saved. Automated first candidate: {chosen}')


if __name__=='__main__':
    main()
