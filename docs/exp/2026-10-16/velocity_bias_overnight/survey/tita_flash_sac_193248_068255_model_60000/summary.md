# tita_flash_sac_193248_068255_model_60000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "duration_s": 60.0,
  "final_drift_m": 0.2910232386346272,
  "max_drift_m": 0.2910232386346272,
  "radial_IAE_m_s": 10.383064369058683,
  "signed_longitudinal_delta_m": -0.2908313999878196,
  "tail_speed_mean_m_s": -0.0030356212455732723,
  "tail_speed_rms_m_s": 0.0030769318710883644,
  "tail_sensor_speed_mean_m_s": -0.0030288912432319113,
  "tail_fk_speed_mean_m_s": -0.003026891045678969,
  "peak_tilt_rad": 0.03421916516630219,
  "peak_wheel_torque_nm": 0.06550079584121704,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.465205214975867
}
```
