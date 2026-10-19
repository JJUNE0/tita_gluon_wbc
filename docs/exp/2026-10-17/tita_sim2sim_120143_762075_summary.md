# TITA sim2sim

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

ONNX SHA256: f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "checkpoint": "/home/cocel/Desktop/Research/tita_gluon_wbc/lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_60000/actor.pt",
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
  "policy_steps": 1000,
  "headless": true,
  "residual_wheel_pd": false,
  "fixed_residual_lqr": false,
  "velocity_bias": true,
  "velocity_bias_acquisition_s": 2.0,
  "velocity_bias_parameters": {
    "kp": 0.0,
    "ki": 4.0,
    "tau": 0.1,
    "limit": 2.0,
    "slew": 3.0,
    "ramp": 0.25,
    "response_sign": 1.0,
    "seed_gain": 3.0
  },
  "wheel_radius_m": 0.0925,
  "velocity_bias_source_sha256": "af6cb6304b6b0e2d373fc80b3bf24f4ed1b3e181c2ef5978480e781fdfd7bd39",
  "residual_wheel_pd_source_sha256": "6a3e75399f8124c3d17c74c2a8ba78597db958395d41a5b1e0b2cf8dc5997dda",
  "detail": "Finite MuJoCo playback completed; this is not a locomotion quality evaluation.",
  "final_base_position_m": [
    -0.007602570112794638,
    0.04072791710495949,
    0.33654317259788513
  ],
  "viewer_threads_stopped": true
}
```
