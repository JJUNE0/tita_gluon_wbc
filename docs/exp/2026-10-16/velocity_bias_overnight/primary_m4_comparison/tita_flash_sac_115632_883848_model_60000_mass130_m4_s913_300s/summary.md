# tita_flash_sac_115632_883848_model_60000_mass130_m4_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: FAIL

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "FAIL",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass130_m4_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "controller": "m4",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "m4"
    }
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
  "input_columns": [
    "total_residual_nm",
    "lqr_correction_nm",
    "fixed_bias_nm"
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
  "error": "Traceback (most recent call last):\n  File \"/home/cocel/Desktop/Research/tita_gluon_wbc/test/velocity_bias_campaign.py\", line 229, in trial\n    runner.step_bias(0.)\n  File \"/home/cocel/Desktop/Research/tita_gluon_wbc/test/velocity_bias_campaign.py\", line 189, in step_bias\n    env.step_with_torque_callback(callback)\n  File \"/home/cocel/Desktop/Research/tita_gluon_wbc/test/static_target_domain.py\", line 63, in step_with_torque_callback\n    command = np.asarray(callback(self.joint_pos(), self.joint_vel())).copy()\n                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/cocel/Desktop/Research/tita_gluon_wbc/test/velocity_bias_campaign.py\", line 182, in callback\n    torque = self.fixed_m4.apply(baseline)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/residual_wheel_pd.py\", line 68, in apply\n    torque[[3, 7]] = np.clip(torque[[3, 7]] + self.u * self.signs / 2, -self.limit, self.limit)\n                                                       ^^^^^^^^^^\nAttributeError: 'ResidualWheelLQR' object has no attribute 'signs'\n",
  "elapsed_wall_s": 0.3656807479565032
}
```
