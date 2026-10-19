# tita_flash_sac_193248_068255_model_75000_friction08_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_friction08_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
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
  "initial_physics_sha256": "e8a4623f7f53cc13aabe2380e950e9f3a20ef182293c7531daff52269ec21edb",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 3.8668003089945597,
  "max_drift_m": 16.4639541846896,
  "radial_IAE_m_s": 2478.637472483574,
  "signed_longitudinal_delta_m": 1.4261408642447961,
  "tail_speed_mean_m_s": -0.01241380839740307,
  "tail_speed_rms_m_s": 0.012413809354033904,
  "tail_sensor_speed_mean_m_s": -0.012318199657947422,
  "tail_fk_speed_mean_m_s": -0.012283413190966756,
  "peak_tilt_rad": 0.10223506974602037,
  "peak_wheel_torque_nm": 0.28730353713035583,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 24.48493156704353
}
```
