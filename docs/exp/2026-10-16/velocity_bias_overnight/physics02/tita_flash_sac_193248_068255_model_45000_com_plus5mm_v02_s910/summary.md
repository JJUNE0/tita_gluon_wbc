# tita_flash_sac_193248_068255_model_45000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
    },
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
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "9e1ff4037564eb4e59405e08e3f59df8ffee0a6300148401ddab6dc3b2e9dfe5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.015877763311195985,
  "max_drift_m": 0.02742968928428838,
  "radial_IAE_m_s": 0.9905883226330146,
  "signed_longitudinal_delta_m": -0.015871476119502806,
  "tail_speed_mean_m_s": 1.8742810893019867e-05,
  "tail_speed_rms_m_s": 1.8743376974733354e-05,
  "tail_sensor_speed_mean_m_s": 1.9666661172667635e-05,
  "tail_fk_speed_mean_m_s": 1.7353483401704534e-05,
  "peak_tilt_rad": 0.07408042041840002,
  "peak_wheel_torque_nm": 0.35716646909713745,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1648033966741103,
  "final_integral_m_s": -0.16483761102593386,
  "elapsed_wall_s": 15.946566402970348
}
```
