# tita_flash_sac_193248_068255_model_80000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "3d031d68b0ed49e3f2a3c90802f8a8db44e3fdf004f9ff5638e1fe8c68376c7d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06408384103332763,
  "max_drift_m": 0.11897332874998591,
  "radial_IAE_m_s": 3.7858599871121674,
  "signed_longitudinal_delta_m": 0.06408101355616216,
  "tail_speed_mean_m_s": 6.202801697784088e-05,
  "tail_speed_rms_m_s": 6.231029742572907e-05,
  "tail_sensor_speed_mean_m_s": 6.151573349181774e-05,
  "tail_fk_speed_mean_m_s": 6.298083670373307e-05,
  "peak_tilt_rad": 0.06386347163685135,
  "peak_wheel_torque_nm": 2.9832000732421875,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18071213093870903,
  "final_integral_m_s": 0.18071213093870903,
  "elapsed_wall_s": 10.870294345950242
}
```
