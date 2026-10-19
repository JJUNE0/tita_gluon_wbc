"""DESKTOP_DRY_RUN: distinguish sensor response from base-origin GT response.

Read-only post-analysis of the same fixed test inputs; no refit or correction.
"""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation

from analyze_flash_state_learning import rms
from eval_flash_m5_yaw_rate import SOURCE, write


def terms(original, extra):
    yaw = original['rpy'][:,2]
    forward = np.column_stack([np.cos(yaw),np.sin(yaw),np.zeros(len(yaw))])
    lateral = np.column_stack([-np.sin(yaw),np.cos(yaw),np.zeros(len(yaw))])
    omega = Rotation.from_euler('xyz',original['rpy']).apply(extra['gyro'])
    offset = original['position']-extra['base_position']
    pitch = np.sum(omega*lateral,axis=1)*offset[:,2]
    yaw_term = -omega[:,2]*np.sum(offset*lateral,axis=1)
    axle_minus_base = original['gt'][:,1]-extra['base_velocity'][:,0]
    articulation = axle_minus_base-pitch-yaw_term
    sensor_minus_axle = original['sensor'][:,1]-original['gt'][:,1]
    return dict(sensor_minus_axle=sensor_minus_axle,rotation_pitch=pitch,
        rotation_yaw=yaw_term,articulation=articulation,
        sensor_minus_base=original['sensor'][:,1]-extra['base_velocity'][:,0])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',required=True,type=Path)
    args = p.parse_args()
    root = args.root.resolve()
    rows,example = [],None
    for path in sorted(root.glob('*/results.json')):
        info = json.loads(path.read_text())
        if info['job']['split']!='test':continue
        for row in info['responses']:
            with np.load(SOURCE/info['job']['id']/row['trace']) as a, np.load(path.parent/row['trace']) as ae:
                current = terms(a,ae)
            with np.load(SOURCE/info['job']['id']/row['baseline']) as b, np.load(path.parent/row['baseline']) as be:
                baseline = terms(b,be)
            delta = {k:current[k]-baseline[k] for k in current}
            closure = delta['sensor_minus_base']-sum(delta[k] for k in [
                'sensor_minus_axle','rotation_pitch','rotation_yaw','articulation'])
            assert max(abs(closure))<1e-14
            rows.append(dict(context=info['job']['id'],family=row['family'],amplitude=row['amplitude'],
                first2s_delta_component_rms={k:float(rms(v[1:101],0)) for k,v in delta.items()},
                closure_max=float(max(abs(closure)))))
            if example is None and row['family']=='pulse_pos' and row['amplitude']==.05:
                example = (row,info['job']['id'],delta)
    medians = {k:float(np.median([r['first2s_delta_component_rms'][k] for r in rows]))
        for k in rows[0]['first2s_delta_component_rms']}
    write(root/'reference_response_facts.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        rows=rows,first2s_component_rms_medians_SI=medians,
        maximum_closure=max(r['closure_max'] for r in rows),
        identity='delta(sensor-base)=delta(sensor-axle)+delta(Omega_l*d_z)-delta(Omega_z*d_l)+delta(articulation)',
        note='Component RMS values do not add and are not unique causal percentages. Articulation is the '
            'measured relative velocity left after rigid base rotation. No estimator correction or new model.'))
    row,context,delta = example
    t = np.arange(len(delta['sensor_minus_base']))*.02
    fig,ax = plt.subplots(figsize=(10,4))
    for k in delta:ax.plot(t,delta[k]*1000,label=k)
    ax.set(xlabel='time after probe [s]',ylabel='matched velocity difference [mm/s]',
        title=f'{context}: pulse +0.05Nm, same sensor and physical points')
    ax.grid(alpha=.3);ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(root/'reference_response.png',dpi=150);plt.close(fig)
    print('[DESKTOP_DRY_RUN] reference-response component RMS medians [mm/s]',
        {k:v*1000 for k,v in medians.items()},flush=True)


if __name__=='__main__':
    main()
