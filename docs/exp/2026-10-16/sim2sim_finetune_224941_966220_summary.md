# MuJoCo FlashSAC fine-tuning

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "source_checkpoint": "/home/cocel/Desktop/Research/tita_gluon_wbc/lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_60000/actor.pt",
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "steps": 1200,
  "updates": 945,
  "actor_updates": 345,
  "falls": 0,
  "timeouts": 2,
  "implementation_sha256": "1fa201c0324157a4605614e60401f3fd587c451bda82cde669b4885a45bff53e",
  "reward_objective": "sensor_reward_v1",
  "critic_velocity": "rolling_axle_proxy",
  "mode": "actor_warm_start",
  "args": {
    "ckpt": "/home/cocel/Desktop/Research/tita_gluon_wbc/lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_60000",
    "steps": 1200,
    "min_buffer": 256,
    "batch_size": 64,
    "buffer_size": 50000,
    "critic_warmup": 256,
    "learning_rate": 1e-05,
    "noise_scale": 0.1,
    "device": "cpu",
    "seed": 42,
    "vx": 0.0,
    "yaw_rate": 0.0,
    "episode_seconds": 10.0,
    "save_every": 1200,
    "viewer": false,
    "eval": false
  },
  "control_dt": 0.02,
  "wheel_radius_m": 0.0925,
  "reward_mean": 0.04132639311398649,
  "speed_proxy_rmse_m_s": 0.40432338207969326,
  "diagnostic_gt_vx_rmse_m_s": 0.08979181054499161,
  "output_checkpoint": "/home/cocel/Desktop/Research/tita_gluon_wbc/docs/exp/2026-10-16/sim2sim_finetune_224941_966220/model_1200",
  "output_actor_sha256": "ce04cbbfaffb6372a2e0b36d4c0b5434ac4d28b681dc2c4bbbf0c0ae9331ebdd",
  "detail": "Finite execution only; policy improvement and hardware readiness are not established."
}
```
