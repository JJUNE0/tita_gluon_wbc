# tita_flash_sac_193248_068255_model_25000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5",
  "onnx_sha256": "19391bfb486479152b3d34f022849e6a9a0c6ba15be2cb35b847b19256f6e30b",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "8ab8490dcff4a4cfc51c6677cbadc67a9028900f7b0d4f933022bf753fa1913c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.292550049964179,
  "max_drift_m": 12.292550049964179,
  "radial_IAE_m_s": 370.2339842662908,
  "signed_longitudinal_delta_m": 12.283820642757991,
  "tail_speed_mean_m_s": 0.2034220562060408,
  "tail_speed_rms_m_s": 0.2034220937229818,
  "tail_sensor_speed_mean_m_s": 0.20298166436107998,
  "tail_fk_speed_mean_m_s": 0.20298166042341098,
  "peak_tilt_rad": 0.11178937831157199,
  "peak_wheel_torque_nm": 0.10738861560821533,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.060515079007018
}
```
