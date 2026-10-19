# tita_flash_sac_115632_883848_model_35000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "0ef6ab55bbc18928cd0e6406efd8eeca222366e346705c2f6672eeabf109e2f5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02496033701315226,
  "max_drift_m": 0.07688437675403598,
  "radial_IAE_m_s": 1.4670139083756257,
  "signed_longitudinal_delta_m": 0.024960331731360256,
  "tail_speed_mean_m_s": 4.841937576320022e-05,
  "tail_speed_rms_m_s": 4.8752270215772646e-05,
  "tail_sensor_speed_mean_m_s": 4.824395311646932e-05,
  "tail_fk_speed_mean_m_s": 5.0458588390628155e-05,
  "peak_tilt_rad": 0.13726974545163406,
  "peak_wheel_torque_nm": 1.4039523601531982,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6018651742295182,
  "final_integral_m_s": 0.6018651742295182,
  "elapsed_wall_s": 12.577711849007756
}
```
