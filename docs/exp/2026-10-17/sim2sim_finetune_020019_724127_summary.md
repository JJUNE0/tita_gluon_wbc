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
  "steps": 2000,
  "updates": 2745,
  "actor_updates": 872,
  "falls": 0,
  "timeouts": 4,
  "implementation_sha256": "90f89e7fa5541b889857e2846b7ada630fdd199671d4797bc4cd04808ed7baf3",
  "reward_objective": "sensor_reward_v2_fk",
  "critic_velocity": "encoder_imu_base_fk",
  "prior_transitions": 3000,
  "bc_updates": 500,
  "actor_scope": "eight_mean_biases",
  "algorithm": "FlashSAC_critic_BC_constrained_actor",
  "mode": "demonstration_assisted_online_finetune",
  "args": {
    "ckpt": "/home/cocel/Desktop/Research/tita_gluon_wbc/lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_60000",
    "steps": 2000,
    "min_buffer": 256,
    "batch_size": 64,
    "buffer_size": 50000,
    "critic_warmup": 1000,
    "teacher_steps": 3000,
    "bc_steps": 500,
    "bc_learning_rate": 0.0001,
    "rl_weight": 1e-05,
    "learning_rate": 1e-05,
    "noise_scale": 0.1,
    "device": "cpu",
    "seed": 42,
    "vx": 0.0,
    "yaw_rate": 0.0,
    "episode_seconds": 10.0,
    "save_every": 2000,
    "viewer": false,
    "eval": false
  },
  "control_dt": 0.02,
  "wheel_radius_m": 0.0925,
  "output_checkpoint": "/home/cocel/Desktop/Research/tita_gluon_wbc/docs/exp/2026-10-17/sim2sim_finetune_020019_724127/model_2000",
  "output_actor_sha256": "86ae7466db5680d41038d230cee0fec347c100a7139060b21dc40af96bc57baf",
  "reward_mean": 0.05946030819154508,
  "speed_proxy_rmse_m_s": 0.014398575316036388,
  "diagnostic_gt_vx_rmse_m_s": 0.01521205913428506,
  "detail": "Finite execution only; policy improvement and hardware readiness are not established."
}
```
