"""DESKTOP_DRY_RUN / VALIDATION_SIM: contact, yaw and GT reference diagnostics."""

import argparse
import gzip
import json
from pathlib import Path
import pickle

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from diagnose_flash_odometry import SOURCE, SCHEMES, CONTACT_COLUMNS, sample
from eval_flash_state_learning import StateRunner, STATE_KEYS
from eval_flash_pv_models import REPO, CKPT, prepared_config, write, sha256


def integrate_path(position,yaw):
    delta = np.diff(position,axis=0)
    angle = yaw[:-1]+((np.diff(yaw)+np.pi)%(2*np.pi)-np.pi)/2
    directions = np.column_stack([np.cos(angle),np.sin(angle),np.zeros(len(angle))])
    return np.r_[0.,np.cumsum(np.sum(delta*directions,axis=1))]


def substep_check(root):
    manifest = json.loads((root/'manifest.json').read_text())
    job = sorted(manifest['jobs'],key=lambda j:j['id'])[0]
    tick = 50000
    archive = SOURCE/'control'/job['id']/f'fixed_LQR_zero_+0_t{tick}.npz'
    cfg = json.loads(prepared_config(CKPT).read_text())
    r = StateRunner(cfg,job)
    metadata = {}
    try:
        with gzip.open(SOURCE/'fresh'/job['id']/f'snapshot_t{tick}.pkl.gz','rb') as f:r.restore(pickle.load(f))
        # Preserve actual contact settings/forces at the initial snapshot, rather
        # than inferring effective friction or dimension from one geom alone.
        m,d,mj = r.env.model,r.sensors,r.env.mujoco
        gids = {m.geom('floor').id}
        contact_metadata = []
        for ci in range(d.ncon):
            contact = d.contact[ci]
            gids.update(int(g) for g in contact.geom)
            force = np.zeros(6)
            mj.mj_contactForce(m,d,ci,force)
            contact_metadata.append(dict(geoms=contact.geom.tolist(),dimension=int(contact.dim),
                friction=contact.friction.tolist(),distance=float(contact.dist),
                include_margin=float(contact.includemargin),solref=contact.solref.tolist(),solimp=contact.solimp.tolist(),
                contact_force6=force.tolist(),tangential_force_over_normal=float(np.linalg.norm(force[1:3])/force[0])))
        geoms = {str(i):dict(name=m.geom(i).name,body=m.body(int(m.geom_bodyid[i])).name,
            condim=int(m.geom_condim[i]),priority=int(m.geom_priority[i]),margin=float(m.geom_margin[i]),
            friction=m.geom_friction[i].tolist()) for i in sorted(gids)}
        write(root/'contact_settings.json',dict(execution_domain='VALIDATION_SIM',geoms=geoms,
            contacts=contact_metadata,cone=str(m.opt.cone),mj_contactForce_doc=mj.mj_contactForce.__doc__))
        clone = r.env.mujoco.MjData(r.env.model)
        initial = r.env.data.time
        rows,contacts = [],[]
        original = r.env.step_with_torque_callback
        def instrument(callback):
            def observe(q,dq):
                r.env.mujoco.mj_copyData(clone,r.env.model,r.env.data)
                r.env.mujoco.mj_forward(r.env.model,clone)
                values,points = sample(r,clone)
                values['t'] = float(clone.time-initial)
                contacts.extend(np.column_stack([np.full(len(points),len(rows)),points]))
                rows.append(values)
                return callback(q,dq)
            original(observe)
        r.env.step_with_torque_callback = instrument
        with np.load(archive) as old:
            for i,u in enumerate(old['requested_u']):
                result = r.step(float(u))
                for k in result:np.testing.assert_array_equal(result[k],old[k][i])
                for k in STATE_KEYS:np.testing.assert_array_equal(r.observation[k],old[k][i+1])
        values = {k:np.asarray([row[k] for row in rows]) for k in rows[0]}
        values['contacts'] = np.asarray(contacts)
        assert len(rows)==4000
        np.savez_compressed(root/'physics_substeps.npz',**values)
        m,d = r.env.model,r.sensors
        for wheel,body in enumerate(r.wheel_bodies):
            gids = [i for i in range(m.ngeom) if m.geom_bodyid[i]==body and
                    m.geom_type[i]==r.env.mujoco.mjtGeom.mjGEOM_CYLINDER]
            metadata[f'wheel{wheel}'] = [dict(geom_id=i,size=m.geom_size[i].tolist(),
                local_position=m.geom_pos[i].tolist(),margin=float(m.geom_margin[i]),gap=float(m.geom_gap[i]),
                friction=m.geom_friction[i].tolist(),condim=int(m.geom_condim[i])) for i in gids]
        t = values['t'];selected=(t>=15.-1e-7)&(t<20.-1e-7)
        summary = {k:float(np.mean(values[k][selected])) for k in ['sensor_v','gt_axle_v','gt_base_v']}
        summary['gap'] = summary['sensor_v']-summary['gt_axle_v']
        for key in ['geometry_height','geometry_yaw','slip']:
            summary[key] = np.mean(values[key][selected],axis=(0,2)).tolist()
        write(root/'substep_check.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',
            context=job['id'],group='fixed_LQR',start_hold_s=1000.,samples=4000,dt=.005,
            exact_control_and_motor_replay=True,measurement_clone_only=True,tail15_20=summary,
            radius_URDF=r.description.radius,geometry=metadata,mujoco_version=r.env.mujoco.__version__,
            note='Normal forces refreshed on clone at the same time; no physics state or control input changes.'))
    finally:r.env.close()


def analyze(root):
    manifest = json.loads((root/'manifest.json').read_text())
    rows = []
    for path in sorted(root.glob('*/results.json')):
        info = json.loads(path.read_text())
        for run in info['runs']:
            with np.load(path.parent/run['trace']) as z, np.load(SOURCE/'control'/info['job']['id']/run['archive']) as old:
                t = np.arange(len(z['sensor_v']))*.02
                tail = (t>=15)&(t<20)
                row = dict(context=info['job']['id'],**run)
                for k in ['sensor_v','gt_axle_v','gt_base_v','axis_and_sensor_error','transport_pitch','transport_yaw',
                          'transport_articulation','axle_minus_base_lateral','gt_body_heading_v']:
                    row[k] = float(np.mean(z[k][tail]))
                row['gap'] = row['sensor_v']-row['gt_axle_v']
                row['gap_at_base_origin'] = row['sensor_v']-row['gt_base_v']
                row['float32_minus64_v'] = float(np.mean(z['sensor_v'][tail]-z['urdf_float64_v'][tail]))
                row['max_URDF_angular_error'] = float(max(z['omega_urdf_MuJoCo_error']))
                row['yaw_rate_world_z'] = float(np.mean(z['wheel_omega'][tail,:,2]))
                row['scheme_terms'] = {}
                for si,name in enumerate(SCHEMES):
                    row['scheme_terms'][name] = {key:float(np.mean(z[key][tail,si,:]))
                        for key in ['geometry_height','geometry_yaw','slip','ground']}
                row['normal_force_per_wheel_terms'] = {key:np.mean(z[key][tail,0,:],axis=0).tolist()
                    for key in ['geometry_height','geometry_yaw','slip']}
                row['closure_max'] = float(np.max(abs(z['closure_error'])))
                row['transport_closure_max'] = float(max(abs(z['transport_closure'])))
                row['frame_invariance_max'] = float(max(z['heading_rotation_invariance_error']))
                yaw = z['rpy'][:,2]
                axle_path = integrate_path(z['axle_position'],yaw)
                base_path = integrate_path(z['base_position'],yaw)
                logged_path = old['gt'][:,0]-old['gt'][0,0]
                np.testing.assert_allclose(axle_path,logged_path,atol=2e-14,rtol=0)
                sensor_path = old['sensor'][:,0]-old['sensor'][0,0]
                row['paths'] = {}
                for key,values in [('axle',axle_path),('base',base_path),('sensor',sensor_path)]:
                    row['paths'][key] = dict(final=float(values[-1]),last5_rmse=float(np.sqrt(np.mean(values[tail]**2))),
                        IAE=float(np.trapz(abs(values),t)))
                row['planar_radius'] = {key:float(max(np.linalg.norm(z[key+'_position'][:,:2]-z[key+'_position'][0,:2],axis=1)))
                    for key in ['base','axle']}
                # The old GT uses midpoint-heading displacement integration, not world x.
                trap = np.r_[0.,np.cumsum((z['gt_axle_v'][:-1]+z['gt_axle_v'][1:])*.01)]
                row['GT_position_vs_velocity_integral_max'] = float(max(abs(axle_path-trap)))
                sensor_integral = np.r_[0.,np.cumsum((z['sensor_v'][:-1]+z['sensor_v'][1:])*.01)]
                row['sensor_position_vs_velocity_integral_max'] = float(max(abs(sensor_path-sensor_integral)))
                contacts = z['contacts'];mask=(contacts[:,0]>=750)&(contacts[:,0]<1000)
                contacts = contacts[mask]
                row['contact_records'] = {str(w):dict(
                    normal_force_range=[float(v) for v in [contacts[contacts[:,1]==w,3].min(),contacts[contacts[:,1]==w,3].max()]],
                    slip_f_range=[float(v) for v in [contacts[contacts[:,1]==w,7].min(),contacts[contacts[:,1]==w,7].max()]],
                    offset_l_range=[float(v) for v in [contacts[contacts[:,1]==w,5].min(),contacts[contacts[:,1]==w,5].max()]]) for w in [0,1]}
                rows.append(row)
    groups = {}
    for group in ['bias_only','fixed_LQR']:
        selected = [x for x in rows if x['group']==group]
        fields = ['gap','gap_at_base_origin','gt_axle_v','gt_base_v','sensor_v','axis_and_sensor_error',
                  'transport_pitch','transport_yaw','transport_articulation','axle_minus_base_lateral','yaw_rate_world_z',
                  'float32_minus64_v','max_URDF_angular_error','GT_position_vs_velocity_integral_max','sensor_position_vs_velocity_integral_max']
        groups[group] = dict(count=len(selected),
            median={k:float(np.median([x[k] for x in selected])) for k in fields},
            range={k:[float(min(x[k] for x in selected)),float(max(x[k] for x in selected))] for k in fields},
            scheme_terms={scheme:{k:float(np.median([x['scheme_terms'][scheme][k] for x in selected]))
                for k in ['geometry_height','geometry_yaw','slip','ground']} for scheme in SCHEMES},
            path_medians={point:{key:float(np.median([x['paths'][point][key] for x in selected]))
                for key in ['final','last5_rmse','IAE']} for point in ['axle','base','sensor']},
            planar_radius_median={key:float(np.median([x['planar_radius'][key] for x in selected])) for key in ['base','axle']})
    invariance=max(x['frame_invariance_max'] for x in rows)
    closure=max(x['closure_max'] for x in rows)
    assert len(rows)==24 and closure<1e-12 and invariance<1e-12
    write(root/'summary.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',groups=groups,
        closure_max=closure,frame_invariance_max=invariance,rows=rows,
        attribution='Two identities describe the same gap: contact geometry/slip and reference-point transport. Do not sum their separate attributions.',
        no_controller_or_estimator_correction=True,old_GT_criterion_preserved=True))
    substep_path = root/'substep_check.json'
    if substep_path.exists():
        substeps = json.loads(substep_path.read_text())
        with np.load(root/substeps['context']/'fixed_LQR_t50000.npz') as z:
            times = np.arange(len(z['sensor_v']))*.02
            selected = (times>=15)&(times<20)
            comparison = dict(gap=float(np.mean(z['sensor_v'][selected]-z['gt_axle_v'][selected])))
            for key in ['geometry_height','geometry_yaw','slip']:
                comparison[key] = np.mean(z[key][selected],axis=(0,2)).tolist()
        write(root/'sampling_check.json',dict(execution_domain='DESKTOP_DRY_RUN',control50Hz=comparison,
            physics200Hz=substeps['tail15_20'],
            gap_difference_mm_s=(substeps['tail15_20']['gap']-comparison['gap'])*1000,
            point='samecontext fixed_LQR at hold1000s; interval15<=t<20'))
    chosen = rows[0]
    with np.load(root/chosen['context']/chosen['trace']) as z:
        t=np.arange(len(z['sensor_v']))*.02
        fig,axes=plt.subplots(2,1,figsize=(11,7),sharex=True)
        axes[0].plot(t,z['sensor_v']*1000,label='encoder/IMU')
        axes[0].plot(t,z['gt_axle_v']*1000,label='GT wheel-center midpoint')
        axes[0].plot(t,z['gt_base_v']*1000,label='GT base_link origin')
        terms=[('geometry_height','height/radius',1),('geometry_yaw','yaw/contact lateral offset',1),('slip','negative contact slip',-1)]
        for field,label,sign in terms:axes[1].plot(t,sign*z[field][:,0,:].mean(1)*1000,label=label)
        axes[1].plot(t,(z['sensor_v']-z['gt_axle_v'])*1000,'k--',label='measured gap')
        axes[0].set_ylabel('sagittal velocity [mm/s]');axes[1].set(ylabel='normal-force mean terms [mm/s]',xlabel='time [s]')
        for ax in axes:ax.legend(fontsize=8);ax.grid(alpha=.3)
        fig.tight_layout();fig.savefig(root/'velocity_decomposition.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,5))
    for group in ['bias_only','fixed_LQR']:
        selected=next(x for x in rows if x['group']==group and x['context']==chosen['context'] and x['start_hold_s']==chosen['start_hold_s'])
        with np.load(root/selected['context']/selected['trace']) as z:
            t=np.arange(len(z['sensor_v']))*.02
            for point in ['axle','base']:
                ax.plot(t,integrate_path(z[point+'_position'],z['rpy'][:,2])*1000,label=group+' '+point)
    ax.set(xlabel='time [s]',ylabel='GT sagittal path at specified point [mm]');ax.legend();ax.grid(alpha=.3)
    fig.tight_layout();fig.savefig(root/'reference_point_paths.png',dpi=150);plt.close(fig)
    assert all(sha256(REPO/p)==h for p,h in manifest['protected_sha256'].items())
    write(root/'analysis_integrity.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        protected_hashes_preserved=True,geometric_identity_closed=True,reference_point_transport_closed=True,
        heading_rotation_invariant=True,old_path_definition_reconstructed=True,source_sha256=sha256(Path(__file__))))
    print('[DESKTOP_DRY_RUN]',json.dumps(groups,indent=2),flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--substeps',action='store_true')
    args=p.parse_args()
    if args.substeps:substep_check(args.root.resolve())
    analyze(args.root.resolve())


if __name__=='__main__':
    main()
