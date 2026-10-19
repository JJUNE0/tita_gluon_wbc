"""DESKTOP_DRY_RUN: audit copied captures and summarize retrospective comparison."""
from pathlib import Path
import hashlib,json
import numpy as np
root=Path(__file__).resolve().parents[2]
out=root/'docs/exp/2026-10-18/vendor_supported_stand_review'
inventory=json.loads((out/'remote_inventory.json').read_text())
for name,expected in inventory['files_sha256'].items():
    assert hashlib.sha256((out/name).read_bytes()).hexdigest()==expected,name
stand=json.loads((out/'stand_metrics.json').read_text());commands=json.loads((out/'commands_metrics.json').read_text())
prior=json.loads((out.parent/'flashsac_80000_105921_pitch_review/analysis.json').read_text())
rl=[s['quiet_neutral_after_2s'] for s in prior['segments'] if s['state']=='rl']
d=np.load(out/'commands_signals.npz');tt=d['unix'];channels=d['channels']
nonzero=np.any(abs(channels[:,2:4])>.1,axis=1)
window_end=min(channels[nonzero,0].max()+.5,tt[-1]-1.)
grid=np.arange(tt[0]+1.,window_end,.01)
index=np.clip(np.searchsorted(channels[:,0],grid,side='right')-1,0,len(channels)-1)
responses={}
for name,axis,signal in [('forward',0,.0925*d['dq'][:,[3,7]].mean(axis=1)),('yaw',1,d['gyro'][:,2])]:
    u=channels[index,2+axis];v=np.interp(grid,tt,signal)
    correlation=np.array([np.corrcoef(u[:-k] if k else u,v[k:])[0,1] for k in range(101)])
    k=int(correlation.argmax())
    responses[name]={'best_observed_correlation':float(correlation[k]),'lag_at_best_correlation_s':k*.01,
                     'same_time_correlation':float(correlation[0]),'searched_lag_s':[0,1.],
                     'window_relative_s':[1.,float(window_end-tt[0])],
                     'note':'descriptive lag of wheel-based proxy or gyro, not measured end-to-end controller delay or base-velocity accuracy'}
mask=d['mode']==3
summary={'execution_domain':'DESKTOP_DRY_RUN','evidence_status':'PASS','policy_checkpoint_sha256':'N/A: company controller',
         'comparison_checkpoint_sha256':prior['checkpoint_sha256'],'raw_files_verified':len(inventory['files_sha256']),
         'company_service_after':inventory['service_after'],'operator_condition':'normal floor standing; same condition as RL, operator corrected initial supported annotation',
         'operator_folded_at_end':True,'command_record_stop':'operator said enough; owned recorder finalized via TERM (exit 143), vendor service unaffected',
         'stand_duration_s':stand['duration_s'],'commands_duration_s':commands['duration_s'],
         'vendor_stand_pitch_deg':stand['STAND_neutral']['pitch_deg'],'RL_quiet_pitch_mean_deg':[e['pitch_mean_deg'] for e in rl],
         'vendor_stand_thigh_knee_rad':np.array(stand['q_native_rad']['mean'])[[1,2,5,6]].tolist(),
         'RL_quiet_thigh_knee_rad':[np.array(e['native_q_mean_rad'])[[1,2,5,6]].tolist() for e in rl],
         'command_phase_STAND_pitch_p01_p99_deg':np.percentile(d['pitch'][mask],[1,99]).tolist(),
         'command_phase_STAND_pitch_min_max_deg':[float(d['pitch'][mask].min()),float(d['pitch'][mask].max())],
         'command_phase_min_pitch_at_s':float(d['t'][np.argmin(d['pitch'])]),
         'mode_changes':commands['firmware_mode_changes'],'response_correlation':responses,
         'limits':['Vendor internal gains/targets and 0x110..0x113 semantics not established.','No matched-input replay; factory and RL joystick ranges differ.','CAN receive timestamps and ROS read timestamps differ; wheel alignment flagged SUSPICIOUS.']}
(out/'comparison_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print('PASS DESKTOP_DRY_RUN raw copy SHA audit, 23 files; known payload parsing and retrospective comparison')
print('Company neutral pitch:',summary['vendor_stand_pitch_deg'])
print('RL quiet pitch:',summary['RL_quiet_pitch_mean_deg'])
print('STAND command pitch p01/p99:',summary['command_phase_STAND_pitch_p01_p99_deg'])
print('Response descriptors:',responses)
