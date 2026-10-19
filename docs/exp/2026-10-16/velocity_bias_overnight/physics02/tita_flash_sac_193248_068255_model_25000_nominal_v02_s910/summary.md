# tita_flash_sac_193248_068255_model_25000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5",
  "onnx_sha256": "19391bfb486479152b3d34f022849e6a9a0c6ba15be2cb35b847b19256f6e30b",
  "state_columns": [
    "base_x",
    "base_y",
    "base_z",
    "base_forward_speed",
    "roll",
    "pitch",
    "yaw",
    "raw_position",
    "raw_speed",
    "fk_position",
    "fk_speed"
  ],
  "initial_physics_sha256": "6cf7d6d44f8545de0788ad2d05c10304f0fda1957536529effd3e2eed6248baa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03413376960165951,
  "max_drift_m": 0.07580565086202468,
  "radial_IAE_m_s": 2.1217142041811083,
  "signed_longitudinal_delta_m": 0.03413359725575501,
  "tail_speed_mean_m_s": -2.7311645022000784e-05,
  "tail_speed_rms_m_s": 2.7312520128510637e-05,
  "tail_sensor_speed_mean_m_s": -2.670033917190852e-05,
  "tail_fk_speed_mean_m_s": -2.677252090840242e-05,
  "peak_tilt_rad": 0.108572957484947,
  "peak_wheel_torque_nm": 1.1366665363311768,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3640134162688731,
  "final_integral_m_s": 0.3640661313760189,
  "elapsed_wall_s": 14.668713034014218
}
```
