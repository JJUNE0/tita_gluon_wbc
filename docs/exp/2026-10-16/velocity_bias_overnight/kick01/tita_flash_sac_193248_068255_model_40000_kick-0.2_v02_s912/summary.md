# tita_flash_sac_193248_068255_model_40000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "db20b1883f79546830231d439a81a0986567927f5085f5547c5a5ef0135504fc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.023089001244364412,
  "max_drift_m": 0.031009640602792068,
  "radial_IAE_m_s": 1.3235436598830481,
  "signed_longitudinal_delta_m": 0.02308899044263858,
  "tail_speed_mean_m_s": 3.0510879298596602e-05,
  "tail_speed_rms_m_s": 3.052349278683326e-05,
  "tail_sensor_speed_mean_m_s": 3.082316671393567e-05,
  "tail_fk_speed_mean_m_s": 3.018067867653692e-05,
  "peak_tilt_rad": 0.12690776630855138,
  "peak_wheel_torque_nm": 1.5278655290603638,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.25851044090384295,
  "final_integral_m_s": 0.25844796297322614,
  "elapsed_wall_s": 15.493147746019531
}
```
