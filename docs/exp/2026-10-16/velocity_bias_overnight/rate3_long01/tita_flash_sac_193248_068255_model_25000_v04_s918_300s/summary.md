# tita_flash_sac_193248_068255_model_25000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "initial_physics_sha256": "80f20bafc99e0ab883576cf2e6e259a7435787c8ef1d1e59d544adb0c3939ebb",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.05393622615641519,
  "max_drift_m": 0.06562873000765919,
  "radial_IAE_m_s": 12.814162000957086,
  "signed_longitudinal_delta_m": -0.053801996524452625,
  "tail_speed_mean_m_s": -9.71159453209289e-05,
  "tail_speed_rms_m_s": 0.00010340184887335263,
  "tail_sensor_speed_mean_m_s": -9.433823434344473e-05,
  "tail_fk_speed_mean_m_s": -9.34909123235165e-05,
  "peak_tilt_rad": 0.10852770810177015,
  "peak_wheel_torque_nm": 1.3767801523208618,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.291467228706754,
  "final_integral_m_s": 0.291467228706754,
  "elapsed_wall_s": 43.6972688040114
}
```
