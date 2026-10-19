# Impulse observation erratum

Execution Domain: VALIDATION_SIM / DESKTOP_DRY_RUN

Policy Checkpoint SHA256 (reference): 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05; all 40 hashes in checkpoint_manifest.json.

Evidence Status: SUSPICIOUS for first-sample FD velocity in earlier impulse experiments.

The root-linear-velocity kick refreshed Runner.observe() twice at one MuJoCo timestamp. The second call replaced the finite-difference wheel/base offset derivative with zero, corrupting the first post-kick FK speed. This especially affects velocity-seeded controllers, which use the initial measurement to initialize the bias. Production WheelVelocityBias.update() runs once per control step and has its own observer history; it does not have this harness issue.

The test observer now caches the derivative by physics timestamp. A pure root-linear impulse updates chassis GT but must leave joint/gyro/FK velocity unchanged at that instant. A focused regression checks this invariant.

Preserve kick01 and seeded_kick01, along with kick-bearing development jobs (physics_pilot_v01, combined02, seeded01/02, schedule03), as affected historical evidence. Their first FK measurement must not establish a final kick robustness claim. Re-run frozen v03 parameters at identical seed917 in seeded_kick02. Non-kick experiments and M4 primary comparisons are unaffected. No source or data is overwritten.
