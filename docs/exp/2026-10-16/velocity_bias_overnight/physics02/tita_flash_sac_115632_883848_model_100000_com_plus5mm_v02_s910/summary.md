# tita_flash_sac_115632_883848_model_100000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "7eda3ed9698619490c7e56b5cfb17a5a1bbf8b5ca36f95bb86fcfdfdf5364107",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.059177400207715246,
  "max_drift_m": 0.07721442102955207,
  "radial_IAE_m_s": 3.4957011373381186,
  "signed_longitudinal_delta_m": 0.059176138942086946,
  "tail_speed_mean_m_s": 3.248020827309213e-05,
  "tail_speed_rms_m_s": 3.265268587632723e-05,
  "tail_sensor_speed_mean_m_s": 3.234177228439618e-05,
  "tail_fk_speed_mean_m_s": 3.208809144848054e-05,
  "peak_tilt_rad": 0.08663378081069983,
  "peak_wheel_torque_nm": 0.6718471646308899,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.600270866143989,
  "final_integral_m_s": 0.6002394890277938,
  "elapsed_wall_s": 12.65068116702605
}
```
