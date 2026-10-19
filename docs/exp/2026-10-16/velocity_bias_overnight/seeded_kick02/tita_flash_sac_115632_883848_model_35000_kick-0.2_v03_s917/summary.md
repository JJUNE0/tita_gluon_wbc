# tita_flash_sac_115632_883848_model_35000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
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
  "initial_physics_sha256": "b39a35fdaca0eee26c0bae9f25d21e9f3084fcb648320af10d868868b63fdb0d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.023577074353311137,
  "max_drift_m": 0.023577074353311137,
  "radial_IAE_m_s": 1.301213293597995,
  "signed_longitudinal_delta_m": 0.023574946251761673,
  "tail_speed_mean_m_s": 4.898259535345966e-05,
  "tail_speed_rms_m_s": 4.926685126136448e-05,
  "tail_sensor_speed_mean_m_s": 4.878839648908588e-05,
  "tail_fk_speed_mean_m_s": 5.10209560175707e-05,
  "peak_tilt_rad": 0.12588886250124864,
  "peak_wheel_torque_nm": 1.2030457258224487,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6015013184915048,
  "final_integral_m_s": 0.6015013184915048,
  "elapsed_wall_s": 13.418785672984086
}
```
