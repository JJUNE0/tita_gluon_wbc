# tita_flash_sac_193248_068255_model_45000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
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
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "c128858e36a2a3dbcec1d9a23513ef7e7e1d6482d0d183fa14f699329164b975",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005878482925665334,
  "max_drift_m": 0.04389034213713347,
  "radial_IAE_m_s": 0.4774565324867398,
  "signed_longitudinal_delta_m": -0.005873769734292783,
  "tail_speed_mean_m_s": 4.0159782387308145e-05,
  "tail_speed_rms_m_s": 4.0161522548954964e-05,
  "tail_sensor_speed_mean_m_s": 4.103767003665469e-05,
  "tail_fk_speed_mean_m_s": 3.8551938406090685e-05,
  "peak_tilt_rad": 0.08079348538056186,
  "peak_wheel_torque_nm": 0.46634387969970703,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.21208989175450493,
  "final_integral_m_s": -0.21208989175450493,
  "elapsed_wall_s": 8.505556499003433
}
```
