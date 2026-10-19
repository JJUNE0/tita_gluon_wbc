# tita_flash_sac_193248_068255_model_75000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
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
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
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
  "initial_physics_sha256": "1fcd56bc99c4746ef9666921faf80980d5f02af3ec4982694f65ffb563da8f6e",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.025363693841681467,
  "max_drift_m": 0.04746310531441907,
  "radial_IAE_m_s": 7.878378303084419,
  "signed_longitudinal_delta_m": -0.025336297097076986,
  "tail_speed_mean_m_s": 4.3538795052080775e-06,
  "tail_speed_rms_m_s": 4.354065819091557e-06,
  "tail_sensor_speed_mean_m_s": 4.341717177671823e-06,
  "tail_fk_speed_mean_m_s": 4.013124852105383e-06,
  "peak_tilt_rad": 0.08461683125210673,
  "peak_wheel_torque_nm": 0.4291240870952606,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2631725177552357,
  "final_integral_m_s": -0.2631803950109988,
  "elapsed_wall_s": 79.83509979996597
}
```
