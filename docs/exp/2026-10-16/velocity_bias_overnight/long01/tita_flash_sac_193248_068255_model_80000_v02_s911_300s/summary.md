# tita_flash_sac_193248_068255_model_80000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "054539ec8e5f9e05227f2c5d4d2b8669245f573099fc676cb91a6b7045d8eb4e",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.018453959998218392,
  "max_drift_m": 0.018453959998218392,
  "radial_IAE_m_s": 4.79828366454216,
  "signed_longitudinal_delta_m": 0.018451171480371512,
  "tail_speed_mean_m_s": 4.573973615205865e-06,
  "tail_speed_rms_m_s": 4.5756904564365025e-06,
  "tail_sensor_speed_mean_m_s": 4.612190901693056e-06,
  "tail_fk_speed_mean_m_s": 5.46165394440056e-06,
  "peak_tilt_rad": 0.05001476788776382,
  "peak_wheel_torque_nm": 2.3872385025024414,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.21451730125142654,
  "final_integral_m_s": 0.21450681194524288,
  "elapsed_wall_s": 87.63103531301022
}
```
