# tita_flash_sac_115632_883848_model_70000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "checkpoint_sha256": "936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189",
  "onnx_sha256": "70370bc52ceb9baf1dff730e385c0d358159b39521a99f56af139ca34bbdccf1",
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
  "initial_physics_sha256": "223ca29bf09101a95dd8d596ea10bb4e5f88dab080dab1b6b51d4066484c19da",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011841311558790583,
  "max_drift_m": 0.02206810823961562,
  "radial_IAE_m_s": 0.7149063880321407,
  "signed_longitudinal_delta_m": -0.011820515758827197,
  "tail_speed_mean_m_s": -5.136280929099791e-07,
  "tail_speed_rms_m_s": 8.38034468219464e-07,
  "tail_sensor_speed_mean_m_s": -5.041477772968781e-07,
  "tail_fk_speed_mean_m_s": -6.469043338428355e-07,
  "peak_tilt_rad": 0.03799657468583262,
  "peak_wheel_torque_nm": 0.38550880551338196,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12257018664189136,
  "final_integral_m_s": -0.12256868268973525,
  "elapsed_wall_s": 12.209041895985138
}
```
