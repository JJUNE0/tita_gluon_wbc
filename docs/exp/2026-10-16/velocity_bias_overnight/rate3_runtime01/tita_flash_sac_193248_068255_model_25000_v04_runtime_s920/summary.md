# tita_flash_sac_193248_068255_model_25000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
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
  "initial_physics_sha256": "7e7a5761237b3c96efa812d9d84015a93e488cfbc7b17db8083450f2e4914ae3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.035472749285628456,
  "max_drift_m": 0.06555461258395433,
  "radial_IAE_m_s": 2.0113310485473708,
  "signed_longitudinal_delta_m": -0.035465563384083514,
  "tail_speed_mean_m_s": -6.762683318546713e-05,
  "tail_speed_rms_m_s": 6.762833802415237e-05,
  "tail_sensor_speed_mean_m_s": -6.692823852205715e-05,
  "tail_fk_speed_mean_m_s": -6.699824058740416e-05,
  "peak_tilt_rad": 0.108554083505354,
  "peak_wheel_torque_nm": 1.373676061630249,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3644463782348292,
  "final_integral_m_s": 0.3644463782348292,
  "elapsed_wall_s": 12.042475848982576
}
```
