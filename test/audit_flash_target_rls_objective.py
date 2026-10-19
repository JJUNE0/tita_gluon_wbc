"""DESKTOP_DRY_RUN: QR/SVD solution of the exact existing RLS prior/forgetting cost.

Post-hoc numerical diagnosis only. No candidate tuning, replacement or gain use.
"""
import argparse
import json
from pathlib import Path

import numpy as np

from flash_cold_start_abc import verify,nominal,BIAS,write,sha256
from collect_flash_target_offline_id import streams_from
from m4_shadow_stages import ConstrainedRLS


def audit(root):
    plan=verify(root,full=True);frozen=root/'C_models_frozen.json';before=sha256(frozen)
    models=json.loads(frozen.read_text())['models'];rows=[]
    for domain in plan['domains']:
        name=domain['name'];streams=streams_from(root,name,plan['C']['training_windows']['post'])
        original=ConstrainedRLS(nominal());features=[];targets=[]
        for z,u,mask in streams:
            x=(z[:-1]-original.ref)/original.scale;y=(z[1:]-original.ref)/original.scale;y[:,0]-=x[:,0]
            features.append(np.column_stack([x[:,1:],(u-BIAS)/.05,np.ones(len(u))])[mask]);targets.append(y[mask])
        X,Y=np.concatenate(features),np.concatenate(targets);n=len(X)
        weights=original.forgetting**np.arange(n-1,-1,-1);prior_weight=original.forgetting**n/100.
        online=models[name]['post_RLS']['model'];A=np.asarray(online['A']);B=np.asarray(online['B']);c=np.asarray(online['c_center'])
        online_theta=np.column_stack([A[:,1:]*original.scale[None,1:]/original.scale[:,None],B*.05/original.scale,c/original.scale])
        group_stats=[]
        for group in original.groups:
            columns=group['columns'];indices=group['rows'];p=len(columns)
            design=np.vstack([np.sqrt(weights)[:,None]*X[:,columns],np.sqrt(prior_weight)*np.eye(p)])
            target=np.vstack([np.sqrt(weights)[:,None]*Y[:,indices],np.sqrt(prior_weight)*group['theta'].T])
            coefficient,_,rank,singular=np.linalg.lstsq(design,target,rcond=None)
            reference=coefficient.T;actual=online_theta[np.ix_(indices,columns)]
            group_stats.append(dict(rows=indices.tolist(),rank=int(rank),weighted_augmented_condition=float(singular[0]/singular[-1]),
                theta_relative_difference=float(np.linalg.norm(reference-actual)/max(np.linalg.norm(reference),1e-15)),
                theta_max_difference=float(np.max(abs(reference-actual))),
                scaled_training_prediction_difference_RMS=float(np.sqrt(np.mean((X[:,columns]@(reference-actual).T)**2)))))
            group['theta']=reference
        reference_model=original.model()
        rows.append(dict(domain=name,samples=n,forgetting=original.forgetting,prior_covariance=100.,prior_weight=prior_weight,
            groups=group_stats,online_rho=float(max(abs(np.linalg.eigvals(A[1:,1:])))),
            equivalent_batch_rho=float(max(abs(np.linalg.eigvals(np.asarray(reference_model['A'])[1:,1:]))))))
    assert sha256(frozen)==before;verify(root,full=True)
    write(root/'RLS_objective_audit.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',rows=rows,
        meaning='Independent weighted/prior LS objective cross-check completed. Numerical differences are reported, not automatically judged as control success.',
        posthoc_diagnostic=True,model_file_unchanged=True,source_sha256=sha256(Path(__file__)),
        no_hyperparameter_or_model_selection=True,no_new_controller=True))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();audit(a.root.resolve())
