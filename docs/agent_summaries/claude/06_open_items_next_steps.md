# Open items / next steps

## Not yet done

- **`04_reference_transform_up_issue.md`**: the structural fix (active balance
  during `reference_transform_up`, or a CoM-balanced `stand_jpos` derivation) has
  not been attempted for any checkpoint. Current state is mitigation-only (user's
  chosen ad-hoc pose).
- **`model_9999.pt` RMATeacher checkpoint has not been driven/evaluated by the user
  yet** beyond the 20s headless no-crash smoke test — the viewer was just launched
  when this handoff doc set was written. Watch for:
  - Whether the `reference_transform_up` tilt is better/worse/same with this
    checkpoint's dynamics vs. prior checkpoints.
  - Whether the RMA privileged_obs assembly (esp. `body_in_contact` threshold,
    `body_mass`/`body_com` reading from the *base_link* body specifically) produces
    sane behavior — this is new code, only shape-validated, not behavior-validated
    against training-time rollouts.
- **`mujoco_env.py::body_quat()`** has its own separate/duplicated body-id-caching
  logic that could be refactored to reuse `_body_id()` (added alongside it for the
  RMA work) — minor cleanliness item, not urgent.
- **No dedicated handoff-stability probe script exists** in `/test/` right now (see
  `05_validation_and_launch.md` — the previously-referenced `moo_handoff_probe.py`
  is not present). If systematic stand_jpos/timer sweeps are needed again, write a
  fresh script under `/test/` rather than assuming one exists.

## Watch out for next time

- If the user hands you a new checkpoint directory, **always re-check the network
  architecture** (`params/agent.yaml` → `policy.class_name`, and cross-check against
  the checkpoint's `state_dict` keys) before assuming it's the same
  `ActorCritic`/`RMATeacher` shape as the last one deployed. This has already changed
  once in this line of work with no advance warning from the run name alone.
- **Re-derive height-command normalization center/half-range per checkpoint** from
  that run's own `feature_functions_common.py` constants or curriculum `end_range` —
  do not carry forward the previous checkpoint's values by default.
- The user's working style: give the checkpoint path, expect autonomous
  inspect → export → config → validate-headless → launch-viewer, minimal
  back-and-forth. See `00_index.md` "Operating pattern" section.
- This repo's `AGENTS.md` still governs: no `git commit`/push without explicit
  request, test/debug scripts belong in `/test/`, never deploy to real hardware
  automatically. None of that changed by this work.
