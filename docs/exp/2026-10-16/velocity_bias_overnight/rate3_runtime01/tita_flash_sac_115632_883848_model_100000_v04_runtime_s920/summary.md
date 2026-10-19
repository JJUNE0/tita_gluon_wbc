# tita_flash_sac_115632_883848_model_100000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
  },
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "d8a1507e7b9faf7a8d6359bc54a2d174df567f2f223e62aef1216549bb69272a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09187039634335253,
  "max_drift_m": 0.11395608009996565,
  "radial_IAE_m_s": 5.3148417618778545,
  "signed_longitudinal_delta_m": 0.09187005755932227,
  "tail_speed_mean_m_s": 9.497794507462676e-05,
  "tail_speed_rms_m_s": 9.549387717940232e-05,
  "tail_sensor_speed_mean_m_s": 9.460069270280048e-05,
  "tail_fk_speed_mean_m_s": 9.460621133419932e-05,
  "peak_tilt_rad": 0.08448421614241064,
  "peak_wheel_torque_nm": 0.47156110405921936,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5416762760121092,
  "final_integral_m_s": 0.5416762760121092,
  "elapsed_wall_s": 12.462399972020648
}
```
