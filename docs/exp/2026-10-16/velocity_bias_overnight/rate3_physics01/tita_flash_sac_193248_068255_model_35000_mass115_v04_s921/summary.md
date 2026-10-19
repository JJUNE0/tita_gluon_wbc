# tita_flash_sac_193248_068255_model_35000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae",
  "onnx_sha256": "a1536d3d580cb29e5617b2c1b7c4a7caef45b7730f864b35d9d082a39fc4ebd6",
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
  "initial_physics_sha256": "d071c3d1c1987660df7a12f56a2afad78c5c877a8ba52c1402ab09b48b2f4367",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017642602912122364,
  "max_drift_m": 0.017642602912122364,
  "radial_IAE_m_s": 0.9109036181309942,
  "signed_longitudinal_delta_m": 0.01764257657496994,
  "tail_speed_mean_m_s": 7.689887778098976e-05,
  "tail_speed_rms_m_s": 7.690405148353396e-05,
  "tail_sensor_speed_mean_m_s": 7.63473218777973e-05,
  "tail_fk_speed_mean_m_s": 7.539272800733684e-05,
  "peak_tilt_rad": 0.06547795660982492,
  "peak_wheel_torque_nm": 0.27922311425209045,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.01467611127815255,
  "final_integral_m_s": -0.01467611127815255,
  "elapsed_wall_s": 9.14969365397701
}
```
