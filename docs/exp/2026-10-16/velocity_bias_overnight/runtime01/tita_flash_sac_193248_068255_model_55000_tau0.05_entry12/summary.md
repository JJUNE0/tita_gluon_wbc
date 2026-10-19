# tita_flash_sac_193248_068255_model_55000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "c241862e4c214fe181ec195099b3949c6834a87f683d7dfbdf072ee40e3d415d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.029276384243361687,
  "max_drift_m": 0.07335979261982248,
  "radial_IAE_m_s": 1.6476292371470445,
  "signed_longitudinal_delta_m": 0.02927598719857307,
  "tail_speed_mean_m_s": 8.674610260631476e-05,
  "tail_speed_rms_m_s": 8.675145030512881e-05,
  "tail_sensor_speed_mean_m_s": 8.713373903444994e-05,
  "tail_fk_speed_mean_m_s": 8.548515589854075e-05,
  "peak_tilt_rad": 0.13808180377919688,
  "peak_wheel_torque_nm": 0.7766963243484497,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.30962834637156506,
  "final_integral_m_s": 0.3094635852293678,
  "elapsed_wall_s": 15.55712642997969
}
```
