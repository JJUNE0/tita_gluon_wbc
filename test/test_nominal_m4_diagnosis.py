"""DESKTOP_DRY_RUN: independent tests of contrasts, affine fit and free rollout."""
import unittest
import numpy as np

from nominal_m4_diagnosis import fit_method,choose,probe_cases,starts,BIAS,unique_baselines
from analyze_flash_stop_local import predict


class NominalDiagnosticsTests(unittest.TestCase):
    def test_quantity_matched_profiles_have_equal_transitions(self):
        records=[dict(j,**c,context=j['id'],start_rl_s=10.)for j in starts('train')for c in probe_cases('train')]
        counts={p:len(choose(records,p))for p in ['small','quantity','waveforms','initials','full','full_replicates']}
        self.assertEqual(counts,dict(small=2,quantity=6,waveforms=6,initials=6,full=78,full_replicates=102))
        self.assertFalse({x['seed']for x in starts('train')}&{x['seed']for x in starts('test')})
        for p in ['quantity','waveforms','initials']:self.assertEqual({r['amplitude']for r in choose(records,p)},{.02})

    def test_nonzero_affine_joint_and_paired_models_recover_known_system(self):
        rng=np.random.default_rng(912);ref=rng.normal(0.,1.,24);A=np.zeros((24,24));A[0,0]=1.;A[0,1]=.02
        # A controllable delay ring excites every nonposition direction above precision.
        A[1:,1:]=.85*np.roll(np.eye(23),1,axis=0)
        B=np.zeros(24);B[1]=.08;c=rng.normal(0.,.001,24);records=[]
        for i in range(100):
            initial=ref+rng.normal(0.,.1,24);z=np.empty((31,24));b=z.copy();z[0]=b[0]=initial
            u=BIAS+rng.normal(0.,.01,30);bu=np.full(30,BIAS)
            for k in range(30):
                z[k+1]=ref+A@(z[k]-ref)+B*(u[k]-BIAS)+c;b[k+1]=ref+A@(b[k]-ref)+c
            records.append(dict(context=str(i),start_rl_s=10.,absolute=z,base=b,delta=z-b,u=u,base_u=bu))
        for method in ['paired_c','joint']:
            m=fit_method(records,method);np.testing.assert_allclose(m['A'],A,atol=1e-7);np.testing.assert_allclose(m['B'],B,atol=1e-7)
            expected=ref-A@ref-B*BIAS+c;np.testing.assert_allclose(m['c_absolute'],expected,atol=1e-7)
            pred=predict(m,records[0]['absolute'][None,0],records[0]['u'][None])[0];np.testing.assert_allclose(pred,records[0]['absolute'],atol=1e-7)

    def test_baselines_not_repeated_per_probe_and_different_times_kept(self):
        z=np.ones((2,24));rows=[dict(context='same',start_rl_s=t,absolute=z,base=z,u=np.zeros(1),base_u=np.zeros(1))for t in [10.,10.,30.]]
        self.assertEqual(len(unique_baselines(rows)),2)

    def test_common_position_translation_does_not_change_fit(self):
        rng=np.random.default_rng(745);rows=[]
        for i in range(100):
            base=rng.normal(size=(2,24));z=base+rng.normal(0.,.001,(2,24));z[0]=base[0]
            rows.append(dict(context=str(i),start_rl_s=10.,absolute=z,base=base,delta=z-base,u=BIAS+rng.normal(0.,.01,1),base_u=np.full(1,BIAS)))
        shifted=[dict(r,absolute=r['absolute']+np.eye(24)[0]*123.,base=r['base']+np.eye(24)[0]*123.)for r in rows]
        for method in ['paired_c','joint']:
            a=fit_method(rows,method);b=fit_method(shifted,method)
            np.testing.assert_allclose(a['A'],b['A'],atol=1e-9);np.testing.assert_allclose(a['B'],b['B'],atol=1e-9)


if __name__=='__main__':unittest.main()
