# tita_flash_sac_193248_068255_model_45000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "5811362e6da617bdbc27b6c1c48d31dbcd6d78360e177a7ce5fce0139b6d3a6e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0065706520290103685,
  "max_drift_m": 0.14025931622743804,
  "radial_IAE_m_s": 0.7389938446183735,
  "signed_longitudinal_delta_m": -0.00656502909296571,
  "tail_speed_mean_m_s": 3.914473225580937e-05,
  "tail_speed_rms_m_s": 3.9148566636460286e-05,
  "tail_sensor_speed_mean_m_s": 3.995505261868294e-05,
  "tail_fk_speed_mean_m_s": 3.747617422379644e-05,
  "peak_tilt_rad": 0.11874703067625925,
  "peak_wheel_torque_nm": 1.7016905546188354,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.20937018342041253,
  "final_integral_m_s": -0.20937018342041253,
  "elapsed_wall_s": 9.24302571901353
}
```
