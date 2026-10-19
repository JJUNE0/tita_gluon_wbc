# MOO reference-parity 4096-env validation

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS`
- Task: `DDT-Velocity-Flat-Tita-MOO-RSL-v0`
- Run: 4096 environments, 24 steps/environment, 100 learning iterations, headless CUDA
- Checkpoint: `logs/moo_rsl_rl/tita_flat_moo_rslrl/2026-07-25_19-11-43/model_99.pt`
- Checkpoint SHA256: `2380078591cfa4e4ab04d15179f1b7fa1aa22a90680b9097e2fc4f9fd566f1af`

## Reference alignment

The working Flamingo MOO implementation was used as the canonical configuration:

- MOO feature set: 9 terms and 14 scalar dimensions after TITA joint mapping
- reward: `0.2 * reward_disc + 0.8 * reward_fm`
- discriminator: spectral-normalized MLP `[256, 256]`, learning rate `1e-4`
- gradient penalty: `0.1`
- logit regularization: `1e-4`
- actor/critic observation normalization: disabled
- reward normalization: disabled
- delta statistics updated during discriminator mini-batch updates
- initial environment distribution mapped from the Flamingo flat task

TITA's nominal joint angles are non-zero, so Flamingo's zero-angle joint feature
was mapped to deviation from TITA's default joint pose. This preserves a zero
feature at each robot's nominal standing configuration.

## Observed metrics

- Iteration 0: mean episode length `10.10`
- Iteration 23: mean episode length `17.88`
- Iteration 50: mean episode length `113.77`
- Iteration 99: mean episode length `148.03`
- Iteration 99 mean reward: `21.25`
- Iteration 99 episode return: `20.1482`
- Iteration 99 discriminator loss: `0.6656`
- Iteration 99 MOO raw reward: `0.1448`
- Total timesteps: `9,830,400`
- Elapsed training time: `00:04:01`

The increasing episode length and return demonstrate that the previously stalled
training signal is restored. Most completed episodes still ended in base contact
at iteration 99, so convergence and command-tracking quality require a full run.
