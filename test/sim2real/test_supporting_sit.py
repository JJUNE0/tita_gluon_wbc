"""DESKTOP_DRY_RUN: native FK/torque parity and latched-stop fault precedence."""
import json
import numpy as np
import mujoco
from validate_sit_transitions import library, parameters, SupportingSit, REPO, LEGS, WHEELS
lib = library()
cfg = json.loads((REPO/'sim2real/tita_ws/src/tita_controller/policies/flashsac_80000/config.json').read_text())
model = mujoco.MjModel.from_xml_path(str(REPO/cfg['model']['scene_xml']))
data = mujoco.MjData(model)
from sim2sim_ros2_jazzy.adapter import NATIVE_JOINTS
addresses = [model.jnt_qposadr[model.joint(n).id] for n in NATIVE_JOINTS]
rng = np.random.default_rng(80000)
maximum = 0.
for _ in range(1000):
    q = rng.normal(size=8)
    quat = rng.normal(size=4); quat /= np.linalg.norm(quat)
    data.qpos[:3] = 0.; data.qpos[3:7] = quat; data.qpos[addresses] = q
    mujoco.mj_kinematics(model, data)
    com = (data.xipos*model.body_mass[:, None]).sum(axis=0)/model.body_mass.sum()
    com -= data.xpos[[model.body('left_leg_4').id, model.body('right_leg_4').id]].mean(axis=0)
    w,x,y,z = quat
    yaw = np.arctan2(2*(w*z+x*y), 1-2*(y*y+z*z))
    expected = np.arctan2(com[0]*np.cos(yaw)+com[1]*np.sin(yaw),com[2])
    delta = abs(np.arctan2(np.sin(lib.sit_angle(q,quat)-expected), np.cos(lib.sit_angle(q,quat)-expected)))
    maximum = max(maximum, delta)
assert maximum < 1e-11, maximum
limits = np.array(cfg['robot']['torque_limit'])
max_tau = 0.
for ending in [5,6]:
    h = lib.sit_create(parameters(cfg)); assert h
    q = np.array([.01,.8,-1.5,0.,-.01,.8,-1.5,0.])
    dq = rng.normal(0,.4,8); prev=rng.normal(0,1,8)
    quat=np.array([np.cos(.04),0.,np.sin(.04),0.]); gyro=np.array([.01,.02,.03])
    lib.sit_request(h,2,q,np.zeros(8)); lib.sit_update(h,20.)
    assert lib.sit_request(h,4,q,prev)
    lib.sit_sensors(h,q,dq,quat,gyro,1)
    assert lib.sit_request(h,ending,q,prev)
    reference = SupportingSit(q,dq,prev,limits,4.,quat,gyro,0.,[30.,5.,1.],lib.sit_angle(q,quat),.3)
    tau=np.zeros(8)
    # Time zero verifies continuity from the final computed RL+bias torque.
    lib.sit_torque(h,q,dq,tau); np.testing.assert_allclose(tau,prev,atol=1e-10,rtol=0)
    for tick in range(1,2501):
        sample=q+rng.normal(0,.02,8); vel=dq+rng.normal(0,.1,8)
        lib.sit_sensors(h,sample,vel,quat,gyro,1);lib.sit_update(h,.002)
        expected=reference.torque(sample,vel,tick*.002,quat,gyro,lib.sit_angle(sample,quat))
        lib.sit_torque(h,sample,vel,tau)
        max_tau=max(max_tau,float(abs(tau-expected).max()))
        assert not lib.sit_request(h,4,q,prev) if tick < 1999 or ending==6 else True
    assert lib.sit_state(h)==(3 if ending==5 else 6)
    if ending==6:
        # Hard fault cancels support even though EStop remains latched.
        lib.sit_request(h,1,q,prev)
        lib.sit_torque(h,q,dq,tau)
        np.testing.assert_allclose(tau,np.clip(-np.array([8,8,8,.5,8,8,8,.5])*dq,-limits,limits))
        assert lib.sit_state(h)==6 and not lib.sit_request(h,4,q,prev)
        assert not lib.sit_request(h,2,q,prev)
    lib.sit_destroy(h)
assert max_tau < 1e-9,max_tau
print(f'PASS DESKTOP_DRY_RUN: 1000 random FK poses max angle error={maximum:.3e}; 5000 torque samples max error={max_tau:.3e}; bumpless entry, 4 s completion, EStop latch and hard-fault damping')
