"""VALIDATION_SIM: sensor-only M4 dynamics and operating-point estimators.

This experiment module is not imported by ROS/runtime code. Regression stays
in the immutable nominal centered coordinates when the control reference moves.
"""
import copy
import numpy as np

from diagnose_m4_adaptive_causes import nominal,fixed_gain,BIAS
from eval_m4_bias_reference import gain_changes,DT,LOW,HIGH
from m4_shadow_stages import ConstrainedRLS
from flash_overnight_model_stages import lqr_gain

# K, bias, internal reference, in the user's E0--E7 order.
MASKS={'E0':(0,0,0),'E1':(1,0,0),'E2':(0,1,0),'E3':(0,0,1),
    'E4':(1,1,0),'E5':(1,0,1),'E6':(0,1,1),'E7':(1,1,1)}
REF_LIMIT=np.r_[.03,.15,np.full(8,.7),np.full(6,.15),np.full(6,.7)]
SUPPORT_HALF_WIDTH=np.r_[.25,.05,.15,.5,np.full(8,1.5),np.full(6,.35),np.full(6,3.)]


def advance(model,z,u):
    ref=np.asarray(model['state_reference'])
    return ref+np.asarray(model['A'])@(z-ref)+np.asarray(model['B'])*(u-BIAS)+model['c_center']


def offset(K,bias,reference):return float(bias+np.asarray(K)@np.asarray(reference))


def reference_target(states,original,leg_limits):
    x=np.asarray(states)
    if len(x)<1000:return None,'history<20s'
    x=x[-1000:]
    if not np.isfinite(x).all() or np.sqrt(np.mean(x[:,1]**2))>.001 or np.std(x[:,2])>.002:
        return None,'moving_or_attitude_variation'
    if np.any(x[:,12:18]<leg_limits[:,0]+.01) or np.any(x[:,12:18]>leg_limits[:,1]-.01):
        return None,'leg_margin'
    target=np.asarray(original).copy();target[2:]=np.clip(x[:,2:].mean(0),x[:,2:].min(0),x[:,2:].max(0));target[:2]=0.
    if np.any(abs(target[2:]-np.asarray(original)[2:])>REF_LIMIT):return None,'nominal_reference_distance'
    assert np.all(target[2:]>=x[:,2:].min(0)) and np.all(target[2:]<=x[:,2:].max(0))
    return target,'observed_mean'


def predicted_bias(model,z,K,reference,bias,previous=BIAS):
    candidates=np.unique(np.clip(bias+np.array([-.001,-.0005,0.,.0005,.001]),LOW,HIGH))
    costs=[]
    for candidate in candidates:
        state=np.asarray(z).copy();score=0.;last=previous
        for _ in range(100):
            target=float(np.clip(candidate-K@(state-reference),LOW,HIGH))
            u=float(np.clip(target,last-.04,last+.04));last=u
            state=advance(model,state,u)
            if not np.isfinite(state).all() or np.max(abs(state[:4]))>2.:
                score=None;break
            score+=DT*(250000.*(state[0]**2+state[1]**2)+400.*(candidate-bias)**2)
        costs.append(score)
    valid=[i for i,v in enumerate(costs) if v is not None and np.isfinite(v)]
    if not valid:return bias,dict(gate=False,reason='nonfinite_or_outside_prediction',candidates=candidates.tolist(),costs=costs)
    best=min(valid,key=lambda i:costs[i]);value=float(candidates[best])
    return value,dict(gate=True,candidates=candidates.tolist(),costs=costs,selected=value,
        horizon_s=2.,static_equilibrium_solve=False)


def gain_candidate(model,old,nominal_K,error,scale):
    g=fixed_gain();raw,diagnostics=lqr_gain(np.asarray(model['A']),np.asarray(model['B']),
        model['state_std'],np.asarray(g['Q']),g['R'])
    K=.9*np.asarray(old)+.1*raw
    per,cumulative=gain_changes(K,old,nominal_K,scale)
    radii={name:float(max(abs(np.linalg.eigvals(np.asarray(m['A'])-np.outer(m['B'],K)))))
        for name,m in [('nominal',nominal()),('identified',model)]}
    jump=float(abs((K-old)@error))
    gate=bool(np.isfinite(K).all() and per<=.25 and cumulative<=.25 and max(radii.values())<1.-1e-8 and jump<=.003)
    return K,dict(gate=gate,per_update_change=per,cumulative_nominal_change=cumulative,
        raw_jump=jump,radii=radii,DARE=diagnostics)


class JointEstimator:
    """All arguments to observe are measured sensor state and applied residual.

    No MuJoCo object, ground truth, dynamics label or change schedule is held by
    this class. Reference means and bias position compensation use different
    measured information; bias is not claimed to be a unique equilibrium input.
    """
    def __init__(self,mask=(1,1,1),method='B1',leg_limits=None,rls=None):
        g=fixed_gain();self.mask=tuple(mask);self.method=method
        self.K0=np.asarray(g['K']);self.reference0=np.asarray(g['reference'])
        self.K=self.K0.copy();self.reference=self.reference0.copy();self.bias=BIAS
        self.rls=copy.deepcopy(rls) if rls is not None else ConstrainedRLS(nominal())
        self.regression_center=self.rls.ref.copy()
        self.scale=np.maximum(nominal()['state_std'],1e-9)
        self.leg_limits=np.asarray(leg_limits if leg_limits is not None else [[-3.,3.]]*6)
        self.states=[];self.inputs=[];self.count=0;self.pending=None;self.model_valid=False
        self.information={'gate':False};self.reference_goal=None;self.events=[];self.models=[]
        self.accepted=dict(K=0,bias=0,reference=0);self.paused=0

    def seed_history(self,states,inputs):
        # Used only for a declared common past prefix, never evaluation future.
        self.states=[x.copy() for x in np.asarray(states)]
        self.inputs=list(np.asarray(inputs));self.count=len(inputs)

    def values(self):return self.K.copy(),float(self.bias),self.reference.copy()

    def observe(self,before,u,after,clipped=False):
        self.count+=1;self.states.append(np.asarray(after).copy());self.inputs.append(float(u))
        # Explicit24-state operational envelope. This is a conservative sensor
        # support bound, not a claim that marginal boxes prove model validity.
        supported=bool(np.all(abs(after-self.reference0)<=SUPPORT_HALF_WIDTH))
        healthy=bool(np.isfinite(np.r_[before,u,after]).all() and supported and not clipped)
        if not healthy:
            self.paused+=1;self.pending=None;self.model_valid=False;return
        self.rls.update(before,u,after)
        old_K,old_bias,old_reference=self.values();changes=[];k_event=None
        if self.pending is not None:
            p=self.pending;p['prediction']=advance(p['model'],p['prediction'],u)
            p['errors'].append(p['prediction'][:2]-after[:2])
            if len(p['errors'])==100:
                error=np.sqrt(np.mean(np.asarray(p['errors'])**2,axis=0))
                valid=bool(p['information']['gate'] and np.all(error<=[.00002,.00002]))
                self.model_valid=valid
                record=dict(kind='model',step=self.count,created=p['created'],prediction_RMSE=error.tolist(),
                    information=p['information'],gate=valid,K_adopted=False)
                if valid and self.mask[0]:
                    try:
                        candidate,guard=gain_candidate(p['model'],self.K,self.K0,after-self.reference,self.scale)
                        record['gain_guard']=guard
                        if guard['gate']:
                            self.K=candidate;changes.append('K');record['K_adopted']=True
                            self.models.append(dict(step=self.count,model=p['model'],K=candidate.tolist()))
                    except Exception as exc:record['gain_error']=type(exc).__name__+': '+str(exc)
                self.events.append(record);k_event=record;self.pending=None
        if self.count%250==0:
            self.information=self.rls.diagnostics()
            if self.pending is None:
                self.pending=dict(model=self.rls.model(),prediction=after.copy(),errors=[],created=self.count,
                    information=copy.deepcopy(self.information))
        quiet=False
        if len(self.states)>=250:
            window=np.asarray(self.states[-250:]);last_u=np.asarray(self.inputs[-250:])
            quiet=bool(np.sqrt(np.mean(window[:,1]**2))<=.001 and np.std(window[:,2])<=.002
                and np.all(last_u>LOW+1e-6) and np.all(last_u<HIGH-1e-6))
        eligible=quiet and self.information.get('gate',False)
        if self.mask[1] and self.count%50==0 and eligible:
            if self.method=='B1':
                # Integral compensation, not a direct physical equilibrium solve.
                delta=float(np.clip(.5*window[:,0].mean(),-.0005,.0005))
                candidate=float(np.clip(self.bias+delta,LOW,HIGH));details=dict(position_mean=float(window[:,0].mean()))
            elif self.method=='B2' and self.model_valid:
                candidate,details=predicted_bias(self.rls.model(),after,self.K,self.reference,self.bias,self.inputs[-1])
                candidate=float(np.clip(candidate,self.bias-.0005,self.bias+.0005))
            else:candidate=self.bias;details=dict(reason='model_validation_pending')
            if candidate!=self.bias:
                self.bias=candidate;changes.append('bias')
                self.events.append(dict(kind='bias',step=self.count,method=self.method,candidate=candidate,details=details))
        if self.mask[2] and self.count%500==0 and self.information.get('gate',False):
            target,reason=reference_target(self.states,self.reference0,self.leg_limits)
            self.events.append(dict(kind='reference_target',step=self.count,reason=reason,
                candidate=None if target is None else target.tolist(),gate=target is not None))
            if target is not None:self.reference_goal=target
        if self.mask[2] and self.reference_goal is not None and eligible:
            difference=self.reference_goal-self.reference
            alpha=min(.02,.002/max(abs(self.K@difference),1e-12))
            proposed=self.reference+alpha*difference;proposed[:2]=0.
            if np.max(abs(proposed-self.reference))>1e-14:
                self.reference=proposed;changes.append('reference')
        if changes:
            jump=float(abs((self.bias-self.K@(after-self.reference))-(old_bias-old_K@(after-old_reference))))
            valid=bool(jump<=.005+1e-12 and LOW<=self.bias<=HIGH
                and np.array_equal(self.reference[:2],[0.,0.])
                and np.all(abs(self.reference[2:]-self.reference0[2:])<=REF_LIMIT+1e-12))
            if not valid:
                self.K,self.bias,self.reference=old_K,old_bias,old_reference
                if k_event is not None:k_event['K_adopted']=False
                if 'K' in changes and self.models and self.models[-1]['step']==self.count:self.models.pop()
                self.events.append(dict(kind='joint_rejection',step=self.count,changes=changes,raw_jump=jump))
            else:
                for key in changes:self.accepted[key]+=1
        assert np.array_equal(self.reference[:2],[0.,0.])
        assert np.array_equal(self.rls.ref,self.regression_center)


class Command:
    def __init__(self,previous=BIAS):self.feedback=0.;self.previous=float(previous);self.count=0

    def compute(self,z,K,bias,reference,probe=0.):
        raw=float(-np.asarray(K)@(z-reference))+probe
        requested=float(bias+raw)
        phase=min(1.,self.count*DT/1.5);activation=phase*phase*(3.-2.*phase)
        target=BIAS+activation*(float(np.clip(requested,LOW,HIGH))-BIAS)
        u=float(np.clip(target,self.previous-.04,self.previous+.04))
        feedback=u-(BIAS+activation*(float(bias)-BIAS))
        self.feedback=feedback;self.previous=u;self.count+=1
        return u,dict(raw_correction=raw,correction=feedback,bias=float(bias),
            effective_offset=offset(K,bias,reference),pre_global_clip=requested,
            global_clipped=bool(requested<LOW or requested>HIGH or u<=LOW+1e-7 or u>=HIGH-1e-7),
            K_used=np.asarray(K).copy(),reference_used=reference.copy())
