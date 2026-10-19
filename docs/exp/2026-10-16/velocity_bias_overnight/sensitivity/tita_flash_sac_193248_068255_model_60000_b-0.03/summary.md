# tita_flash_sac_193248_068255_model_60000_b-0.03

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_b-0.03",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
    "law": {
      "mode": "constant",
      "bias": -0.03
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
  "initial_physics_sha256": "e7b710cff718d1b9352b0809b30515f0409c721e0965f1f5f9510df01396eb4c",
  "complete": true,
  "failure": [],
  "duration_s": 40.0,
  "final_drift_m": 0.04972642322087995,
  "max_drift_m": 0.04972642322087995,
  "radial_IAE_m_s": 0.5961412476340193,
  "signed_longitudinal_delta_m": 0.04966810992181383,
  "tail_speed_mean_m_s": 0.0024193448434417877,
  "tail_speed_rms_m_s": 0.0024742878008411247,
  "tail_sensor_speed_mean_m_s": 0.002413992548163174,
  "tail_fk_speed_mean_m_s": 0.0024156361959180167,
  "peak_tilt_rad": 0.037844282369062565,
  "peak_wheel_torque_nm": 0.07230844348669052,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.03,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 3.0805526369949803
}
```
