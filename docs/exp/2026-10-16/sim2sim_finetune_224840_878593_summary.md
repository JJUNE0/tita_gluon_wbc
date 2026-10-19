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
  "steps": 32,
  "updates": 25,
  "actor_updates": 11,
  "falls": 0,
  "timeouts": 3,
  "mode": "actor_warm_start",
  "args": {
    "ckpt": "/home/cocel/Desktop/Research/tita_gluon_wbc/lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_60000",
    "steps": 32,
    "min_buffer": 8,
    "batch_size": 4,
    "buffer_size": 64,
    "critic_warmup": 4,
    "learning_rate": 1e-05,
    "noise_scale": 0.1,
    "device": "cpu",
    "seed": 42,
    "vx": 0.0,
    "yaw_rate": 0.0,
    "episode_seconds": 0.2,
    "save_every": 32,
    "viewer": false,
    "eval": false
  },
  "reward_mean": 0.03908744908475572,
  "speed_proxy_rmse_m_s": 0.2880847579153429,
  "diagnostic_gt_vx_rmse_m_s": 0.03718028195870915,
  "output_checkpoint": "/home/cocel/Desktop/Research/tita_gluon_wbc/docs/exp/2026-10-16/sim2sim_finetune_224840_878593/model_32",
  "output_actor_sha256": "9c0028a073d04dcc1456b54bf1ee9bcabee6dc208d4d7d5243c04e8631d1f701",
  "detail": "Finite execution only; policy improvement and hardware readiness are not established."
}
```
