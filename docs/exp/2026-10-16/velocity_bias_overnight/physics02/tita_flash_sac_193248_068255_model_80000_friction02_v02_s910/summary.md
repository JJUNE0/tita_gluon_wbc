# tita_flash_sac_193248_068255_model_80000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
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
  "final_drift_m": 0.017367918235938574,
  "max_drift_m": 0.017367918235938574,
  "radial_IAE_m_s": 0.928140589191191,
  "signed_longitudinal_delta_m": 0.017355733680099628,
  "tail_speed_mean_m_s": 2.1424207185106006e-05,
  "tail_speed_rms_m_s": 2.1427575287258962e-05,
  "tail_sensor_speed_mean_m_s": 2.4473931888455777e-05,
  "tail_fk_speed_mean_m_s": 2.629644863268737e-05,
  "peak_tilt_rad": 0.04978358980349484,
  "peak_wheel_torque_nm": 1.8263370990753174,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18628774236362672,
  "final_integral_m_s": 0.18623738524680164,
  "elapsed_wall_s": 13.858425407030154
}
```
