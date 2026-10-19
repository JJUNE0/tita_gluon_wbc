# tita_flash_sac_115632_883848_model_100000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
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
  "initial_physics_sha256": "626296b4ffb97098a43630e215acaed163e20e00083f6a26407ba03114d18331",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.09300694421623022,
  "max_drift_m": 0.11352196167601598,
  "radial_IAE_m_s": 28.181180000172866,
  "signed_longitudinal_delta_m": 0.09300449829131752,
  "tail_speed_mean_m_s": -8.062532796349068e-05,
  "tail_speed_rms_m_s": 8.186470257397652e-05,
  "tail_sensor_speed_mean_m_s": -8.015412776908892e-05,
  "tail_fk_speed_mean_m_s": -8.050591494792968e-05,
  "peak_tilt_rad": 0.08457155573092878,
  "peak_wheel_torque_nm": 0.4679277241230011,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5475250647876103,
  "final_integral_m_s": 0.5475250647876103,
  "elapsed_wall_s": 53.318923768994864
}
```
