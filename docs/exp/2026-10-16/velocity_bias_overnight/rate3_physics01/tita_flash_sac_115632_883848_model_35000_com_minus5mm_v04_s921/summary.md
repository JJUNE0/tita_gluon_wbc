# tita_flash_sac_115632_883848_model_35000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "e641c9374af1a2f88da63e83368116b96064f0ec0e5c258641d4dffc8136b310",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.023852077835050212,
  "max_drift_m": 0.0642601899852792,
  "radial_IAE_m_s": 1.4295706005327138,
  "signed_longitudinal_delta_m": 0.023849736251030186,
  "tail_speed_mean_m_s": 1.2125779968608758e-05,
  "tail_speed_rms_m_s": 1.2235037893435191e-05,
  "tail_sensor_speed_mean_m_s": 1.1962166211671859e-05,
  "tail_fk_speed_mean_m_s": 1.4279879137033459e-05,
  "peak_tilt_rad": 0.1351994914175556,
  "peak_wheel_torque_nm": 2.274696111679077,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5538705227048061,
  "final_integral_m_s": 0.5538705227048061,
  "elapsed_wall_s": 10.587880161008798
}
```
