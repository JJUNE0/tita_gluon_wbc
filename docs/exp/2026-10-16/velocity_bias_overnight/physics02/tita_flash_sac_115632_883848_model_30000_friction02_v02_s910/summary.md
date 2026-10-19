# tita_flash_sac_115632_883848_model_30000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
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
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "bf3e5e71f6cca5c18334a5f4e30b104f2529276bd1b815f045693752d53722b1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04013763789436315,
  "max_drift_m": 0.10420404255187178,
  "radial_IAE_m_s": 2.3947330498446755,
  "signed_longitudinal_delta_m": 0.04012963284409675,
  "tail_speed_mean_m_s": 2.251213627733528e-05,
  "tail_speed_rms_m_s": 2.2978827874633467e-05,
  "tail_sensor_speed_mean_m_s": 2.2339592583067218e-05,
  "tail_fk_speed_mean_m_s": 2.2598184166145028e-05,
  "peak_tilt_rad": 0.10608993135394629,
  "peak_wheel_torque_nm": 0.8210616111755371,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.42000476434711753,
  "final_integral_m_s": 0.41997352333439525,
  "elapsed_wall_s": 11.094846524007153
}
```
