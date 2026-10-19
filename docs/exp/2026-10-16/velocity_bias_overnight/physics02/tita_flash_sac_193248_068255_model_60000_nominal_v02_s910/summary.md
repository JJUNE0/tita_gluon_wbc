# tita_flash_sac_193248_068255_model_60000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
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
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
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
  "initial_physics_sha256": "d9199b200c2c644ccfbdfc9d0af19c6feb366938727bf749fcd8fe6fb9b01b1d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0011516017713589584,
  "max_drift_m": 0.004939745455151045,
  "radial_IAE_m_s": 0.12961278935813036,
  "signed_longitudinal_delta_m": -0.0010804227583129204,
  "tail_speed_mean_m_s": 3.391320148824228e-05,
  "tail_speed_rms_m_s": 3.391656852913534e-05,
  "tail_sensor_speed_mean_m_s": 3.360078688236218e-05,
  "tail_fk_speed_mean_m_s": 3.582559872383397e-05,
  "peak_tilt_rad": 0.03916998228841018,
  "peak_wheel_torque_nm": 0.13805851340293884,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.010879799694423951,
  "final_integral_m_s": -0.010949884478142118,
  "elapsed_wall_s": 19.620435415999964
}
```
