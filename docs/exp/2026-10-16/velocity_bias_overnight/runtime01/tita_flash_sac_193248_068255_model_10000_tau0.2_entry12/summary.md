# tita_flash_sac_193248_068255_model_10000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "7cbf09f6def3e7621b868c5b66ee501302caa95ce44779512b14a4d932341888",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01026380347660182,
  "max_drift_m": 0.01026380347660182,
  "radial_IAE_m_s": 0.4998457800872651,
  "signed_longitudinal_delta_m": 0.0100903511357458,
  "tail_speed_mean_m_s": 5.504724371831456e-05,
  "tail_speed_rms_m_s": 5.507840568558006e-05,
  "tail_sensor_speed_mean_m_s": 6.853279059497775e-05,
  "tail_fk_speed_mean_m_s": 7.520308625784526e-05,
  "peak_tilt_rad": 0.02469899501167908,
  "peak_wheel_torque_nm": 0.8979452848434448,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.11371267637825891,
  "final_integral_m_s": 0.11356919899945929,
  "elapsed_wall_s": 6.562699228001293
}
```
