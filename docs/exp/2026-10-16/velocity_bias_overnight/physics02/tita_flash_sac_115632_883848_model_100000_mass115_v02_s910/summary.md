# tita_flash_sac_115632_883848_model_100000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "cdc1ca16b7ccfc546e34a988c70bf9ec3aaaa7058731a821a731a322d61acb15",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0361598779135814,
  "max_drift_m": 0.036203422115760026,
  "radial_IAE_m_s": 1.8713086933586864,
  "signed_longitudinal_delta_m": -0.036159697516186626,
  "tail_speed_mean_m_s": -0.000184206065883779,
  "tail_speed_rms_m_s": 0.0072915768573737555,
  "tail_sensor_speed_mean_m_s": 0.0008325740072086714,
  "tail_fk_speed_mean_m_s": 0.0001084915396798808,
  "peak_tilt_rad": 0.11626509235933558,
  "peak_wheel_torque_nm": 3.199599027633667,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.24630618966156728,
  "final_integral_m_s": -0.2691106968115511,
  "elapsed_wall_s": 11.884641860960983
}
```
