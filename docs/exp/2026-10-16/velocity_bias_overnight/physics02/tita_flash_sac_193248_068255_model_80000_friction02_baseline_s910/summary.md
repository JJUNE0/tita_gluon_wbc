# tita_flash_sac_193248_068255_model_80000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "040b73d922f3c789e4c891882864ceb8ab16961a100e121f46c48683f9db1aca",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.5671199190956213,
  "max_drift_m": 2.5671199190956213,
  "radial_IAE_m_s": 70.64527700263002,
  "signed_longitudinal_delta_m": 2.542918300934098,
  "tail_speed_mean_m_s": 0.04922829567359996,
  "tail_speed_rms_m_s": 0.049323632068089304,
  "tail_sensor_speed_mean_m_s": 0.04983938005103155,
  "tail_fk_speed_mean_m_s": 0.04927298820031683,
  "peak_tilt_rad": 0.05427066442498574,
  "peak_wheel_torque_nm": 1.805317997932434,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.756667842972092
}
```
