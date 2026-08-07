# TITA-mounted GLUON collision-aware reachability map

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `SUSPICIOUS`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (deterministic FK and collision sampling; no learned policy)
- GLUON URDF SHA256: `b9b25074b7a417a9e499f14fee852699ac6f8a00ab4b137f90ec843eccc8ede4`
- Combined TITA+GLUON URDF SHA256: `2db28c8a6a685c0a8238628ab697904193759549079782fbfeea8f7e015fded7`
- Reachability NPZ SHA256: `d08ea2ca5b1d66e34a15e7298d750db8174f002aab599a783ed0a6e5ed003a0a`
- Reachability PLY SHA256: `23d65c003bdd8c04789f3aa62fcad8aee8851537ad04dfa35dd9ba4079b3493f`
- Robot hardware commands: none

## Purpose

The previous W2 cylindrical sector is a controller command gate, not a full
workspace model. This run computes a non-primitive, collision-filtered sampled
reachability map for mounting GLUON on TITA. The map uses the link6 origin as
the end effector and records a representative joint configuration in every
occupied voxel.

## Configuration

- Input samples: `262,144` scrambled Sobol samples over q1-q5
- q6: fixed at `0 rad`
- Joint-limit margin: `5 deg`
- Manipulability gate: q1-q5 linear Jacobian `sigma_min >= 0.01`
- TITA standing pose: `[0.1, 0.8, -1.5, 0, 0.1, 0.8, -1.5, 0] rad`
- Collision backend: Pinocchio 2.7.0 with hpp-fcl 2.4.4
- Collision pairs: `51`
- Collision security margin: `10 mm`
- Voxel resolution: `10 mm`
- Connectivity: 26-neighbor Cartesian voxel component containing the WORK pose
- WORK pose: `[0, 0.8, 1.6, 0.8, 0, 0] rad`
- Provisional TITA-to-GLUON mount: translation `[0, 0, 0.1564] m`, rotation
  `-90 deg` about Y

Command:

```bash
/home/cocel/isaac/env_isaaclab/bin/python \
  test/analyze_tita_gluon_reachability.py \
  --output test/eval_logs/tita_gluon_reachability_q6_zero.npz
```

## Observed metrics and behavior

- Samples above manipulability threshold: `260,248 / 262,145` including WORK
- Collision-free samples after the 10 mm margin: `248,163 / 260,248`
- Samples in the WORK-connected Cartesian voxel component: `247,433`
- WORK-connected occupied voxels: `141,632`
- Disconnected occupied voxels removed from the displayed component: `682`
- WORK link6 position in TITA base: `[0.135892, 0.021868, 0.618438] m`
- WORK `sigma_min`: `0.0206012`
- Sampled connected XYZ bounds in TITA base:
  - X: `[-0.471951, 0.473111] m`
  - Y: `[-0.471188, 0.472505] m`
  - Z: `[0.033265, 0.733978] m`
- Horizontal radius about the mounted joint1 center:
  - minimum: `0.103009 m`
  - p01 / median / p99: `0.109686 / 0.241185 / 0.452382 m`
  - sampled maximum: `0.474326 m`
- Surface mesh: `283,989` vertices, `759,216` triangles
- Dense analysis elapsed time: `34.387 s`

The most frequent first collision hits were link5 against the TITA base
(`3,894`), link3 against the TITA base (`2,380`), link2 against link5
(`1,965`), and link4 against the TITA base (`1,206`). This confirms that a
simple sphere, box, or full cylinder would include configurations excluded by
the mounted collision model.

## Verification

Pure geometry tests:

```text
/home/cocel/isaac/env_isaaclab/bin/python -m pytest -q \
  test/test_tita_gluon_reachability.py test/test_gluon_ik_math.py
22 passed
```

An initial invocation with system `python3` could not collect the existing IK
tests because that interpreter has no PyTorch installation. It was an
environment mismatch rather than a test assertion failure; the project Isaac
Python command above is the recorded result.

Isaac Sim surface-load and controller smoke:

```bash
/home/cocel/isaac/env_isaaclab/bin/python \
  lab/ddt_lab/scripts/gluon/run_gluon_keyboard_ik.py \
  --headless --max-steps 800 --status-log-every-controls 0 \
  --reachability-map test/eval_logs/tita_gluon_reachability_q6_zero.npz
```

Observed result:

- reachability mesh loaded: `283,989` vertices / `759,216` faces
- HOME-to-WORK transition completed
- final Cartesian error: `2.597 mm`
- joint/velocity-limit violations: `0 / 0`
- result: `GLUON_KEYBOARD_IK: PASS`

## Evidence assessment and limitations

The deterministic run and GUI-loading path are `PASS`, but the map remains
overall `SUSPICIOUS` because:

1. The mount/jig dimensions and transform are draft values, not physical
   measurements.
2. The combined TITA URDF has simplified or absent collision geometry on some
   links.
3. The map applies only to the recorded TITA standing pose.
4. No gripper/tool collision, mass, or TCP offset is modeled.
5. Occupancy proves at least one sampled configuration for a voxel; it does
   not prove the full voxel or an inter-voxel joint trajectory.
6. Unoccupied space is unknown rather than proven unreachable.

The next acceptance step is to measure the mounting transform and jig, add the
tool0/gripper model, then validate candidate task paths by continuous
joint-space collision checking. No result here authorizes hardware motion.

## Combined-model viewer follow-up

The first interactive overlay reused the standalone GLUON controller and
transformed the TITA-frame surface back into the GLUON base frame. It therefore
did not display the TITA body and was rejected by operator review.

`test/view_tita_gluon_reachability.py` now imports the actual combined draft
URDF and displays:

- TITA in policy standing pose
- the mounted 2L6/4L3 GLUON in WORK pose
- the reachability surface directly in TITA `base_link`
- no physics stepping and no hardware interface

Runtime model evidence reported 14 joints and 23 bodies with all eight TITA
and six GLUON joint names present. The surface loaded with 283,989 vertices and
759,216 faces at opacity 0.04. Isaac's importer emits warnings for empty TITA
sensor links and for the intentionally unconfigured static-view actuators;
these remain `SUSPICIOUS` cleanup items but did not prevent the combined model
or surface from loading.
