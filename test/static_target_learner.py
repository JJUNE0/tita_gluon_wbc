"""VALIDATION_SIM: causal single-rollout adaptation with frozen-candidate validation.

Independent same-state Direct B forks remain offline diagnostics. The online B
check is explicitly a conditional held-out regression, never an oracle Direct B.
"""
import copy
import numpy as np

from m4_joint_adaptation import JointEstimator, gain_candidate, advance, SUPPORT_HALF_WIDTH
from m4_shadow_stages import ConstrainedRLS


MASKS = {'Flash':(0,0,0), 'Bias':(0,0,0), 'Fixed':(0,0,0), 'BiasOnline':(0,1,0),
         'RefOnline':(0,0,1), 'E6':(0,1,1), 'KOnly':(1,0,0), 'E7':(1,1,1)}


def causal_validation(model, states, inputs):
    """Candidate fixed before this entire validation sequence was observed."""
    x, u = np.asarray(states), np.asarray(inputs)
    A, B = np.asarray(model['A']), np.asarray(model['B'])
    scores = {}
    for horizon in [5,25,50,100]:
        errors, signals = [], []
        for start in range(0,len(u)-horizon+1,5):
            pred=x[start].copy()
            for step in range(start,start+horizon):pred=advance(model,pred,u[step])
            errors.append(pred[:2]-x[start+horizon,:2])
            signals.append(x[start+horizon,:2]-x[start,:2])
        rmse=np.sqrt(np.mean(np.asarray(errors)**2,axis=0))
        signal=np.maximum(np.sqrt(np.mean(np.asarray(signals)**2,axis=0)),[1e-7,1e-5])
        scores[str(horizon)]=dict(RMSE=rmse.tolist(),NRMSE=(rmse/signal).tolist())
    ref=np.asarray(model['state_reference']);scale=np.maximum(model['state_std'],1e-7)
    features=np.column_stack([(x[:-1,1:]-ref[1:])/scale[1:],(u-.4828)/.05,np.ones(len(u))])
    rms=np.maximum(np.sqrt(np.mean(features**2,axis=0)),1e-12)
    singular=np.linalg.svd(features/rms,compute_uv=False)
    rank=int(np.sum(singular>singular[0]*1e-8));condition=float(singular[0]/max(singular[-1],1e-300))
    # v is translation-invariant: independent regression on subsequent samples.
    coeff=np.linalg.lstsq(features/rms,x[1:,1],rcond=1e-8)[0]/rms
    measured_B=float(coeff[23]/.05)
    error=float(abs(measured_B-B[1])/max(abs(measured_B),1e-12))
    b_gate=bool(rank==25 and condition<=1e6 and measured_B*B[1]>0 and error<=.3)
    gate=bool(b_gate and all(np.all(np.asarray(s['NRMSE'])<=.3) and np.all(np.asarray(s['RMSE'])<=2e-5)for s in scores.values()))
    return dict(gate=gate,horizons=scores,causal_B=dict(kind='conditional held-out regression, not same-state Direct B',
        value=measured_B,relative_difference=error,rank=rank,condition=condition,gate=b_gate))


class StaticLearner(JointEstimator):
    def __init__(self, mask, leg_limits, permit_K=False):
        super().__init__((0,mask[1],mask[2]),'B1',leg_limits)
        self.requested_mask=tuple(mask);self.permit_K=permit_K
        self.partial=ConstrainedRLS(copy.deepcopy(self.rls.original),partial=True)
        self.candidate=None;self.validated_model=None;self.K_adoptions=[];self.candidate_events=[]
        self.B2_shadow=[]

    def observe(self,before,u,after,clipped=False):
        previous_K,previous_bias,previous_reference=self.values()
        super().observe(before,u,after,clipped)
        healthy=bool(np.isfinite(np.r_[before,u,after]).all() and not clipped
            and np.all(abs(after-self.reference0)<=SUPPORT_HALF_WIDTH))
        if healthy:self.partial.update(before,u,after)
        if not healthy:
            if self.candidate is not None:self.candidate_events.append(dict(step=self.count,gate=False,reason='unsafe_or_saturated_validation'))
            self.candidate=None
            return
        if self.candidate is not None:
            pending=self.candidate;pending['states'].append(after.copy());pending['inputs'].append(float(u))
            if len(pending['inputs'])==200:
                score=causal_validation(pending['model'],pending['states'],pending['inputs'])
                entry=dict(step=self.count,created=pending['created'],validation=score,adopted=False)
                if score['gate'] and pending['information']['gate']:
                    self.validated_model=copy.deepcopy(pending['model'])
                    if self.requested_mask[0] and self.permit_K:
                        try:
                            K,guard=gain_candidate(pending['model'],self.K,self.K0,after-self.reference,self.scale)
                            entry['gain_guard']=guard
                            joint=abs((self.bias-K@(after-self.reference))-(previous_bias-previous_K@(after-previous_reference)))
                            entry['joint_raw_jump']=float(joint)
                            if guard['gate'] and joint<=.005:
                                self.K=K;self.accepted['K']+=1;entry['adopted']=True
                                self.K_adoptions.append(dict(step=self.count,K=K.tolist(),model=pending['model'],validation=score))
                        except Exception as exc:entry['exception']=type(exc).__name__+': '+str(exc)
                if not self.permit_K and self.requested_mask[0]:entry['reason']='independent_domain_or_strict_online_Direct_B_admission_not_met'
                self.candidate_events.append(entry);self.candidate=None
        if self.count%250==0 and self.candidate is None and self.rls.count>=250:
            self.candidate=dict(model=self.rls.model(),created=self.count,information=self.rls.diagnostics(),states=[after.copy()],inputs=[])
        if self.count%500==0:
            # B2 proposals are strictly shadow. Exact model/source hash is retained.
            from m4_joint_adaptation import predicted_bias
            model=copy.deepcopy(self.validated_model)
            if model is not None:
                value,details=predicted_bias(model,after,self.K,self.reference,self.bias,u)
                self.B2_shadow.append(dict(step=self.count,proposed=value,details=details,applied=False))

    def report(self):
        return dict(events=self.events,candidates=self.candidate_events,accepted=self.accepted,
            new_target_K_adoptions=self.K_adoptions,B2_shadow=self.B2_shadow,
            full_model=self.rls.model(),partial_model=self.partial.model(),
            information=self.rls.diagnostics() if self.rls.count>=25 else dict(gate=False,samples=self.rls.count),
            RLS_history=self.rls.history,regression_center=self.regression_center.tolist(),
            source='nominal MuJoCo pre-calibrated prior, no target model initialization',
            limitation='Online conditional B check differs from offline same-state Direct B; independent posthoc model verification also required.')
