# tita_flash_sac_115632_883848_model_100000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "2f8c5efb10945d6cd30cd22c0c8763ac466d9140f35decdba60af617dfe6e35c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.07933632753636405,
  "max_drift_m": 0.08905829117166193,
  "radial_IAE_m_s": 3.6418508729846755,
  "signed_longitudinal_delta_m": -0.07930110836800734,
  "tail_speed_mean_m_s": -0.0007363824401255471,
  "tail_speed_rms_m_s": 0.020610910807953114,
  "tail_sensor_speed_mean_m_s": -0.00013659721747322865,
  "tail_fk_speed_mean_m_s": 0.00016016530503885353,
  "peak_tilt_rad": 0.19988009275722018,
  "peak_wheel_torque_nm": 5.548288822174072,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4180084538622011,
  "final_integral_m_s": -0.451929589540283,
  "elapsed_wall_s": 12.650990432011895
}
```
