# tita_flash_sac_193248_068255_model_35000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
    },
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
  "checkpoint_sha256": "29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae",
  "onnx_sha256": "a1536d3d580cb29e5617b2c1b7c4a7caef45b7730f864b35d9d082a39fc4ebd6",
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
  "initial_physics_sha256": "5f0ad6ef8998820205a5f387ceaa2f47f572f59faebe2a7a7399896fd80d79fc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017642607903497955,
  "max_drift_m": 0.017642607903497955,
  "radial_IAE_m_s": 0.9109030133612048,
  "signed_longitudinal_delta_m": 0.0176425815616366,
  "tail_speed_mean_m_s": 7.689979308441946e-05,
  "tail_speed_rms_m_s": 7.690485711174221e-05,
  "tail_sensor_speed_mean_m_s": 7.634932926665429e-05,
  "tail_fk_speed_mean_m_s": 7.53936726650433e-05,
  "peak_tilt_rad": 0.06547786460521254,
  "peak_wheel_torque_nm": 0.2792307138442993,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.01467598679779759,
  "final_integral_m_s": -0.01467598679779759,
  "elapsed_wall_s": 10.648386302986182
}
```
