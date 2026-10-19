# tita_flash_sac_193248_068255_model_45000_seeded_v03_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_seeded_v03_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "guarded": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "4352052302a576ccd11d21b120de3904acecd3a254a55f70975fd578ec1a4d01",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006027143883331864,
  "max_drift_m": 0.04272764219276295,
  "radial_IAE_m_s": 0.4797513553102863,
  "signed_longitudinal_delta_m": -0.00602221611529422,
  "tail_speed_mean_m_s": 3.7754365565704774e-05,
  "tail_speed_rms_m_s": 3.775630720901542e-05,
  "tail_sensor_speed_mean_m_s": 3.8469968244634196e-05,
  "tail_fk_speed_mean_m_s": 3.601336688703401e-05,
  "peak_tilt_rad": 0.08000439174071095,
  "peak_wheel_torque_nm": 0.45158717036247253,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.20599302772435008,
  "final_integral_m_s": -0.20599302772435008,
  "elapsed_wall_s": 4.73285227100132
}
```
