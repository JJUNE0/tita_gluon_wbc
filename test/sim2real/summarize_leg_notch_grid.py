"""DESKTOP_DRY_RUN: paired finite-grid regression gates, not a hardware safety proof."""
import argparse
import json
from pathlib import Path
import numpy as np


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('results',type=Path)
    args=p.parse_args();rows=json.loads(args.results.read_text())
    baselines={tuple((k,str(v)) for k,v in sorted(r['job'].items()) if k!='filter'):r
               for r in rows if r['job']['filter']=='ma2_legs'}
    paired=[]
    for r in rows:
        if not r['job']['filter'].startswith('notch:'):continue
        key=tuple((k,str(v)) for k,v in sorted(r['job'].items()) if k!='filter')
        base=baselines[key];failures=[]
        if r['fault'] and not base['fault']:failures.append('new_fault')
        values={}
        if r['fault'] or base['fault']:
            values['fault_pair']=[base['fault'],r['fault']]
        else:
            values['startup_pitch_delta_deg']=r['startup_pitch_peak_deg']-base['startup_pitch_peak_deg']
            if values['startup_pitch_delta_deg']>2.:failures.append('startup_pitch_delta_over_2deg')
            if r['job']['scenario']=='stand':
                values['pitch_std_delta_deg']=r['pitch_std_deg']-base['pitch_std_deg']
                values['speed_delta_m_s']=r['speed']-base['speed']
                if values['pitch_std_delta_deg']>1.:failures.append('pitch_std_delta_over_1deg')
                if abs(values['speed_delta_m_s'])>.03:failures.append('speed_delta_over_.03')
            else:
                errors=[]
                for a,b in zip(base['segments'],r['segments']):
                    for k,limit in [('vx_error',.05),('wz_error',.05),('stop_speed',.03)]:
                        if k in a and k in b:
                            errors.append(dict(metric=k,segment_start=b['start_s'],delta=b[k]-a[k]))
                            if (abs(b[k])-abs(a[k]))>limit:failures.append(k+'_degraded')
                values['segment_deltas']=errors
            for k in ('leg_ticks','wheel_ticks'):
                delta=r['clips'][k]/r['clips']['rl_ticks']-base['clips'][k]/base['clips']['rl_ticks']
                values[k+'_clip_fraction_delta']=delta
                if delta>.01:failures.append(k+'_clipping_increased')
        paired.append(dict(id=r['id'],failures=failures,**values))
    result=dict(execution_domain='DESKTOP_DRY_RUN',
        evidence_status='PASS' if not any(x['failures'] for x in paired) else 'FAIL',
        pairs=len(paired),cases=paired,
        note='Predefined engineering comparison gates on this grid; not a hardware stability guarantee.')
    path=args.results.with_name('assessment.json');path.write_text(json.dumps(result,indent=2)+'\n')
    print(result['evidence_status'],'pairs',len(paired))
    for e in paired:
        if e['failures']:print(e['id'],e['failures'],e)
    if paired:
        print('max startup delta',max((e.get('startup_pitch_delta_deg',0) for e in paired)))


if __name__=='__main__':main()
