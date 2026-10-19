"""DESKTOP_DRY_RUN: production Python MA2/notch vs SciPy reference, no plant."""
from pathlib import Path
import sys
import unittest
import numpy as np
from scipy.signal import iirnotch, lfilter, lfilter_zi

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.adapter import LegActionFilter


class NotchMath(unittest.TestCase):
    def test_reference_dc_reset_and_wheel_mapping(self):
        rng=np.random.default_rng(83)
        order=[3,0,7,1,2,4,5,6];legs=[1,3,4,5,6,7]
        for hz,q in [(7.5,2.),(8.3,3.),(9.,4.)]:
            raw=rng.uniform(-3,3,(2000,8)).astype(np.float32)
            ma=LegActionFilter('ma2_legs',order)
            inputs=np.array([ma.update(row) for row in raw])
            b,a=iirnotch(hz,q,fs=50)
            reference=inputs.copy()
            for j in legs:
                reference[:,j]=lfilter(b,a,inputs[:,j],zi=lfilter_zi(b,a)*inputs[0,j])[0]
            f=LegActionFilter('ma2_notch_legs',order,hz,q)
            actual=np.array([f.update(row) for row in raw])
            np.testing.assert_allclose(actual,reference,atol=2e-6,rtol=1e-6)
            np.testing.assert_array_equal(actual[:,[0,2]],raw[:,[0,2]])
            np.testing.assert_array_equal(actual[0],raw[0])
            f.reset();np.testing.assert_array_equal(f.update(raw[-1]),raw[-1])
            f.reset()
            constant=np.array([f.update(np.full(8,2.5)) for _ in range(500)])
            np.testing.assert_array_equal(constant,2.5)

    def test_stopband_and_parameter_validation(self):
        t=np.arange(3000)/50
        raw=np.tile((np.sin(2*np.pi*8.3*t)+.3*(-1.)**np.arange(len(t)))[:,None],(1,8))
        f=LegActionFilter('ma2_notch_legs',list(range(8)))
        out=np.array([f.update(row) for row in raw])
        self.assertLess(np.max(abs(out[1000:,0])),1e-6)
        self.assertGreater(np.std(out[1000:,3]),.5)
        for hz,q in [(0,3),(25,3),(8.3,0),(8.3,float('nan')),(24,.5)]:
            with self.assertRaises(ValueError):LegActionFilter('ma2_notch_legs',list(range(8)),hz,q)


if __name__=='__main__':unittest.main(verbosity=2)
