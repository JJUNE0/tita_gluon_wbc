# tita_flash_sac_193248_068255_model_35000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "checkpoint_sha256": "29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae",
  "onnx_sha256": "a1536d3d580cb29e5617b2c1b7c4a7caef45b7730f864b35d9d082a39fc4ebd6",
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
  "initial_physics_sha256": "30911b8afe93cbfd5f00b7c1cb28ba4d0f957c325dbccde837bb0663bbbf79c8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.029900806257667938,
  "max_drift_m": 0.0383596616415523,
  "radial_IAE_m_s": 1.7387743802296936,
  "signed_longitudinal_delta_m": 0.029900395710034187,
  "tail_speed_mean_m_s": 2.9121514091915252e-05,
  "tail_speed_rms_m_s": 2.9122484243326366e-05,
  "tail_sensor_speed_mean_m_s": 2.885449954491718e-05,
  "tail_fk_speed_mean_m_s": 2.791634974672794e-05,
  "peak_tilt_rad": 0.058401522267092165,
  "peak_wheel_torque_nm": 0.6275672912597656,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.30777135057670696,
  "final_integral_m_s": 0.30771676323883485,
  "elapsed_wall_s": 21.20206652698107
}
```
