"""DESKTOP_DRY_RUN: C++/Python MA2 sequence parity and policy-rate placement contract."""
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO/'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.adapter import LegActionFilter


class FilterParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(dir=REPO/'test/sim2real',prefix='ma2_parity_')
        cls.binary=Path(cls.tmp.name)/'filter'
        subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror','-pedantic',
            '-I',str(REPO/'sim2real/tita_ws/src/tita_controller/include'),
            str(REPO/'test/sim2real/test_leg_action_filter.cpp'),'-o',str(cls.binary)],check=True)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_production_adapter_and_teacher_contract(self):
        subprocess.run([str(self.binary)],check=True)

    def test_random_permuted_order_reset_and_off_cross_language(self):
        rng=np.random.default_rng(25)
        for mode in ('none','ma2_legs','ma2_notch_legs'):
            for order in (list(range(8)),[3,0,7,1,2,4,5,6]):
                raw=rng.uniform(-4,4,(500,8)).astype(np.float32)
                resets=np.zeros(500,dtype=int);resets[[0,79,80,200,450]]=1
                f=LegActionFilter(mode,order);expected=[]
                for i,row in enumerate(raw):
                    if resets[i]: f.reset()
                    expected.append(f.update(row))
                stream=io.StringIO();stream.write(mode+' '+' '.join(map(str,order))+'\n')
                if mode=='ma2_notch_legs':stream.write('8.3 3.0\n')
                np.savetxt(stream,np.c_[resets,raw],fmt='%.17g')
                result=subprocess.run([str(self.binary),'stream'],input=stream.getvalue(),
                    text=True,capture_output=True,check=True)
                actual=np.loadtxt(io.StringIO(result.stdout))
                if mode=='ma2_notch_legs':
                    np.testing.assert_allclose(actual,np.array(expected),atol=2e-6,rtol=1e-6)
                else:
                    np.testing.assert_array_equal(actual,np.array(expected))
                wheels=[i for i,j in enumerate(order) if j in (3,7)]
                np.testing.assert_array_equal(actual[:,wheels],raw[:,wheels])
                np.testing.assert_array_equal(actual[resets==1],raw[resets==1])

    def test_period_two_dc_and_validation(self):
        f=LegActionFilter('ma2_legs',list(range(8)))
        f.update(np.ones(8))
        for i in range(100):
            raw=np.full(8,-1 if i%2==0 else 1,dtype=np.float32)
            out=f.update(raw)
            np.testing.assert_array_equal(out[[0,1,2,4,5,6]],0.)
        f.reset();np.testing.assert_array_equal(f.update(np.full(8,3.)),3.)
        np.testing.assert_array_equal(f.update(np.full(8,3.)),3.)
        for raw in (np.zeros(7),np.full(8,np.nan)):
            with self.assertRaises(ValueError): f.update(raw)
        with self.assertRaises(ValueError): LegActionFilter('ma2_all',list(range(8)))

    def test_custom_notch_coefficients_cross_language(self):
        raw=np.random.default_rng(835).uniform(-4,4,(500,8)).astype(np.float32)
        for hz,q in ((7.5,2.),(8.3,3.),(9.,4.)):
            f=LegActionFilter('ma2_notch_legs',list(range(8)),hz,q)
            expected=np.array([f.update(row) for row in raw])
            stream=io.StringIO();stream.write(f'ma2_notch_legs 0 1 2 3 4 5 6 7 {hz} {q}\n')
            np.savetxt(stream,np.c_[np.zeros(500),raw],fmt='%.17g')
            run=subprocess.run([str(self.binary),'stream'],input=stream.getvalue(),
                               text=True,capture_output=True,check=True)
            np.testing.assert_allclose(np.loadtxt(io.StringIO(run.stdout)),expected,atol=2e-6,rtol=1e-6)


if __name__=='__main__':
    unittest.main(verbosity=2)
