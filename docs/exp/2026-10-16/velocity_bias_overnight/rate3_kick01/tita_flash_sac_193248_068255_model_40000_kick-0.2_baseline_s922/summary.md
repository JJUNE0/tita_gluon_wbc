# tita_flash_sac_193248_068255_model_40000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "ee3d701cbfbf3b53a466228d53c1d84c6ce7125a9e00c69f3d76ccf4073041ee",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.882849818796348,
  "max_drift_m": 9.882849818796348,
  "radial_IAE_m_s": 280.2733621166295,
  "signed_longitudinal_delta_m": 9.822854861229851,
  "tail_speed_mean_m_s": 0.17788736604159977,
  "tail_speed_rms_m_s": 0.17788835093451813,
  "tail_sensor_speed_mean_m_s": 0.17750366418157865,
  "tail_fk_speed_mean_m_s": 0.1774945843658894,
  "peak_tilt_rad": 0.12024776990119013,
  "peak_wheel_torque_nm": 1.4799325466156006,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.317234556016047
}
```
