"""VALIDATION_SIM: replay existing zero-command logs, measure odometry geometry.

No controller, estimator, policy or model is changed. Contact velocities and
point transport are measured on the same fresh MuJoCo data used for old GT.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
import json
from pathlib import Path
import pickle

import numpy as np
from scipy.spatial.transform import Rotation

from eval_flash_state_learning import StateRunner, STATE_KEYS
from eval_flash_pv_models import REPO, CKPT, prepared_config, write, sha256
from sim2sim_ros2_jazzy.adapter import NATIVE_JOINTS

SOURCE = REPO/'docs/exp/2026-10-15/flash_affine_lqr'
SCHEMES = ['normal_force', 'uniform_loaded', 'max_normal_force']
CONTACT_COLUMNS = ['sample','wheel','contact','normal_force','offset_f','offset_l','offset_z',
                   'slip_f','slip_l','slip_z','height_term','yaw_term','ground_f','distance']


def contact_terms(radius,forward,lateral,velocity,omega,offset,ground):
    """Exact identity at an arbitrary contact constraint point, static z-up floor.

    r*omega_l-v_center_f = (r+offset_z)*omega_l-offset_l*omega_z
                          -relative_contact_velocity_f-ground_velocity_f.
    """
    vertical = np.cross(forward,lateral)
    slip = velocity + np.cross(omega,offset) - ground
    height = (radius+offset@vertical)*(omega@lateral)
    yaw = -(offset@lateral)*(omega@vertical)
    return dict(height=float(height),yaw=float(yaw),slip=float(slip@forward),
        slip_l=float(slip@lateral),slip_z=float(slip@vertical),ground=float(ground@forward))


def point_velocity(r,data,point,body):
    jp = np.zeros((3,r.env.model.nv))
    jr = np.zeros_like(jp)
    r.env.mujoco.mj_jac(r.env.model,data,jp,jr,point,body)
    return jp@data.qvel,jr@data.qvel


def axes_velocity(r,data,q,dq):
    quat = data.sensor('trunk_quat').data
    rot = Rotation.from_quat(quat[[1,2,3,0]])
    gyro = rot.apply(data.sensor('trunk_gyro').data)
    _,axes = r.description.frames(q)
    angular = [gyro+sum((rot.apply(axes[NATIVE_JOINTS[i]])*dq[i] for i in chain),start=np.zeros(3))
               for chain in r.description.wheel_chains()]
    return np.asarray(angular)


def sample(r,data):
    m,mj = r.env.model,r.env.mujoco
    quat = data.sensor('trunk_quat').data
    rotation = Rotation.from_quat(quat[[1,2,3,0]])
    roll,pitch,yaw = rotation.as_euler('xyz')
    forward = np.array([np.cos(yaw),np.sin(yaw),0.])
    lateral = np.array([-np.sin(yaw),np.cos(yaw),0.])
    q64 = data.qpos[r.env.qpos_addr]
    dq64 = data.qvel[r.env.qvel_addr]
    angular32 = axes_velocity(r,data,q64.astype(np.float32).astype(float),dq64.astype(np.float32).astype(float))
    angular64 = axes_velocity(r,data,q64,dq64)
    radius = r.description.radius
    base = m.body('base_link').id
    base_pos = data.xpos[base]
    base_v,base_w = point_velocity(r,data,base_pos,base)
    centers = data.xpos[r.wheel_bodies]
    velocities,angulars = zip(*(point_velocity(r,data,data.xpos[b],b) for b in r.wheel_bodies))
    velocities,angulars = np.asarray(velocities),np.asarray(angulars)
    axle_v = velocities.mean(0)
    offset = centers.mean(0)-base_pos
    transport_pitch = float((base_w@lateral)*offset[2])
    transport_yaw = float(-base_w[2]*(offset@lateral))
    articulation = float((axle_v-base_v-np.cross(base_w,offset))@forward)
    sensor_v = float(radius*np.mean(angular32@lateral))
    exact_v = float(radius*np.mean(angulars@lateral))
    gt_v = float(axle_v@forward)
    weighted = {k:np.zeros((3,2)) for k in ['height','yaw','slip','ground']}
    contact_rows = []
    force_totals,counts,contact_offsets = [],[],[]
    rotation_test = Rotation.from_euler('z',.83)
    invariance_error = 0.
    for wheel,body in enumerate(r.wheel_bodies):
        loaded = []
        for ci in range(data.ncon):
            c = data.contact[ci]
            bodies = [int(m.geom_bodyid[g]) for g in c.geom]
            if body not in bodies:continue
            force = np.zeros(6)
            mj.mj_contactForce(m,data,ci,force)
            normal = float(force[0])
            if normal<=1e-8:continue
            other = bodies[1] if bodies[0]==body else bodies[0]
            assert other==0,'This diagnostic expects static floor contacts only'
            ground,_ = point_velocity(r,data,c.pos,other)
            delta = c.pos-centers[wheel]
            terms = contact_terms(radius,forward,lateral,velocities[wheel],angulars[wheel],delta,ground)
            rotated = contact_terms(radius,rotation_test.apply(forward),rotation_test.apply(lateral),
                rotation_test.apply(velocities[wheel]),rotation_test.apply(angulars[wheel]),
                rotation_test.apply(delta),rotation_test.apply(ground))
            invariance_error = max(invariance_error,max(abs(terms[k]-rotated[k]) for k in terms))
            loaded.append((normal,terms,delta))
            contact_rows.append([wheel,ci,normal,delta@forward,delta@lateral,delta[2],
                terms['slip'],terms['slip_l'],terms['slip_z'],terms['height'],terms['yaw'],terms['ground'],float(c.dist)])
        assert loaded,'No loaded contact for a wheel'
        forces = np.asarray([row[0] for row in loaded])
        weights = [forces/forces.sum(),np.ones(len(forces))/len(forces),np.eye(len(forces))[int(np.argmax(forces))]]
        for scheme,weight in enumerate(weights):
            for k in weighted:weighted[k][scheme,wheel]=sum(w*row[1][k] for w,row in zip(weight,loaded))
        force_totals.append(forces.sum());counts.append(len(forces))
        contact_offsets.append(sum(w*row[2] for w,row in zip(weights[0],loaded)))
    geometry = weighted['height']+weighted['yaw']
    reconstructed = geometry.mean(1)-weighted['slip'].mean(1)-weighted['ground'].mean(1)+(sensor_v-exact_v)
    closure = reconstructed-(sensor_v-gt_v)
    result = dict(sensor_v=sensor_v,gt_axle_v=gt_v,exact_angular_odometry=exact_v,
        urdf_float64_v=float(radius*np.mean(angular64@lateral)),axis_and_sensor_error=sensor_v-exact_v,
        omega_urdf_MuJoCo_error=float(np.max(np.linalg.norm(angular64-angulars,axis=1))),
        gt_base_v=float(base_v@forward),gt_body_heading_v=float(axle_v@rotation.apply([1.,0.,0.])),
        wheel_center_v=velocities@forward,wheel_omega=angulars,
        geometry_height=weighted['height'],geometry_yaw=weighted['yaw'],slip=weighted['slip'],ground=weighted['ground'],
        closure_error=closure,heading_rotation_invariance_error=invariance_error,
        transport_pitch=transport_pitch,transport_yaw=transport_yaw,transport_articulation=articulation,
        transport_closure=float((axle_v-base_v)@forward-transport_pitch-transport_yaw-articulation),
        base_position=base_pos.copy(),axle_position=centers.mean(0),rpy=np.array([roll,pitch,yaw]),
        axle_minus_base_lateral=float(offset@lateral),force_totals=np.asarray(force_totals),
        contact_counts=np.asarray(counts),contact_offset_normal_force=np.asarray(contact_offsets))
    return result,np.asarray(contact_rows)


def replay_job(cfg,job,output):
    out = Path(output)/job['id']
    out.mkdir()
    r = StateRunner(cfg,job)
    original = SOURCE/'control'/job['id']
    info = json.loads((original/'results.json').read_text())
    summaries = []
    try:
        for run in info['runs']:
            if run['family']!='zero' or run['group'] not in ['bias_only','fixed_LQR']:continue
            tick = round(run['start_hold_s']/.02)
            snapshot_path = SOURCE/'fresh'/job['id']/f'snapshot_t{tick}.pkl.gz'
            with gzip.open(snapshot_path,'rb') as f:r.restore(pickle.load(f))
            with np.load(original/run['trace']) as archive:
                diagnostics,contacts,states,steps = [],[],[],[]
                for i in range(len(archive['sensor'])):
                    states.append({k:r.observation[k].copy() for k in STATE_KEYS})
                    before = (r.env.data.qpos.copy(),r.env.data.qvel.copy(),r.env.data.ctrl.copy(),r.estimator.position)
                    values,contact = sample(r,r.sensors)
                    np.testing.assert_allclose(values['sensor_v'],r.observation['sensor'][1],atol=1e-14,rtol=0)
                    np.testing.assert_allclose(values['gt_axle_v'],r.observation['gt'][1],atol=1e-14,rtol=0)
                    assert max(abs(values['closure_error']))<1e-12 and abs(values['transport_closure'])<1e-12
                    np.testing.assert_array_equal(r.env.data.qpos,before[0]);np.testing.assert_array_equal(r.env.data.qvel,before[1])
                    np.testing.assert_array_equal(r.env.data.ctrl,before[2]);assert r.estimator.position==before[3]
                    diagnostics.append(values)
                    contacts.extend(np.column_stack([np.full(len(contact),i),contact]))
                    if i<len(archive['requested_u']):steps.append(r.step(float(archive['requested_u'][i])))
                for key in STATE_KEYS:np.testing.assert_array_equal([x[key] for x in states],archive[key])
                for key in steps[0]:np.testing.assert_array_equal([x[key] for x in steps],archive[key])
            data = {k:np.asarray([x[k] for x in diagnostics]) for k in diagnostics[0]}
            data['contacts'] = np.asarray(contacts)
            filename = f"{run['group']}_t{tick}.npz"
            np.savez_compressed(out/filename,**data)
            summaries.append(dict(group=run['group'],start_hold_s=run['start_hold_s'],trace=filename,
                archive=run['trace'],exact_replay=True,max_closure=float(np.max(abs(data['closure_error']))),
                mean_gap=float(np.mean(data['sensor_v']-data['gt_axle_v']))))
        write(out/'results.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',job=job,runs=summaries,
            no_new_controller=True,original_trajectory_unchanged=True))
        print('[VALIDATION_SIM]',job['id'],'exact replays',len(summaries),flush=True)
        return dict(id=job['id'],replays=len(summaries))
    finally:r.env.close()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--workers',type=int,default=3)
    args = p.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(REPO/'docs/exp') and not out.exists()
    out.mkdir(parents=True)
    config = prepared_config(CKPT)
    cfg = json.loads(config.read_text())
    source_manifest = json.loads((SOURCE/'fresh/manifest.json').read_text())
    files = list((SOURCE/'control').rglob('*.npz'))+list((SOURCE/'fresh').rglob('*.pkl.gz'))
    files += list((REPO/'sim2sim/sim2sim_ros2_jazzy').rglob('*.py'))+list((REPO/'sim2sim/lqr').glob('*.py'))
    files += [CKPT/'actor.pt',config,config.parent/'policy.onnx',SOURCE/'fixed_gain_frozen.json',Path(__file__).resolve()]
    protected = {str(path.relative_to(REPO)):sha256(path) for path in files}
    write(out/'manifest.json',dict(execution_domain='VALIDATION_SIM',checkpoint_sha256=source_manifest['checkpoint_sha256'],
        onnx_sha256=source_manifest['onnx_sha256'],jobs=source_manifest['jobs'],protected_sha256=protected,
        scheme_names=SCHEMES,contact_columns=CONTACT_COLUMNS,
        scope='exact replay only; 24 old20s zero-command branches, no new inputs/controller/estimator/model/gain',
        decomposition='gap=axis_error+height+world-yaw contact lever-slip-ground; wheel arithmetic mean after contact aggregation',
        attribution='normal-force weighting is explicit; uniform/max-loaded alternatives diagnose non-unique contact allocation'))
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(replay_job,cfg,job,str(out)) for job in source_manifest['jobs']]
        for future in as_completed(futures):results.append(future.result())
    assert all(sha256(REPO/path)==h for path,h in protected.items())
    write(out/'completion.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',results=results,
        total_replays=sum(x['replays'] for x in results),protected_hashes_preserved=True))


if __name__=='__main__':
    main()
