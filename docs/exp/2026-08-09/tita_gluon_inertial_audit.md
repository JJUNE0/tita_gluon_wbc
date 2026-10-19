# TITA+GLUON URDF-to-PhysX inertial audit

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS` — phantom sensor mass removed and runtime revalidated
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` — asset-only audit; no policy was loaded
- Asset: `sim2sim/tita_gluon_urdf/urdf/tita_gluon_2L6_4L3.urdf`
- Task: `Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-Play-v0-moo-ppo`

## Result

The GLUON arm mass and full inertia tensors are preserved correctly by the
URDF-to-USD importer and are present in the PhysX articulation.  The audit
initially found five TITA auxiliary links receiving an importer-default mass of
1 kg each.  Restoring fixed-joint merging removed those frame-only bodies and
the corrected runtime mass now matches the explicit URDF mass.

This is not a defect introduced by the GLUON link descriptions, and it does
not occur in the existing TITA-only runtime.  The empty auxiliary links already
exist in the source TITA xacro and TITA URDF.  The combined configuration makes
them separate rigid bodies by setting `merge_fixed_joints=False`; that setting
is the trigger that turns the pre-existing incomplete link descriptions into
five 1 kg bodies.

## Root-cause comparison with TITA-only import

| Case | Fixed-joint import | Explicit URDF mass | PhysX mass | Result |
|---|---|---:|---:|---|
| TITA only | `merge_fixed_joints=True` (Isaac Lab default) | 25.690957890000 kg | 25.690956115723 kg | `PASS` |
| TITA + GLUON, before fix | `merge_fixed_joints=False` (explicit) | 30.958569270597 kg | 35.958568572998 kg | `SUSPICIOUS` (+5 kg) |
| TITA + GLUON, corrected | `merge_fixed_joints=True` (explicit) | 30.958569270597 kg | 30.958568572998 kg | `PASS` |

In the TITA-only runtime the five fixed auxiliary links are merged/ignored and
do not contribute phantom mass; the articulation has nine bodies and its total
mass matches the explicitly defined URDF mass within floating-point precision.
Consequently, ordinary TITA-only URDF-to-USD conversion is not the source of
the observed +5 kg.  The causal chain is:

1. The original TITA description contains five empty sensor/frame links with
   no inertial definitions.
2. The original TITA asset relies on Isaac Lab's default fixed-joint merging,
   so the incomplete links do not become independent rigid bodies.
3. The combined TITA+GLUON asset disables fixed-joint merging, exposing all
   five links as rigid bodies; Isaac Sim then assigns 1 kg to each.

The GLUON merge itself merely motivated/introduced the importer-setting change;
the GLUON mass and inertia declarations are not responsible for the 5 kg error.

## Remediation validation

The combined `UrdfFileCfg` now explicitly sets `merge_fixed_joints=True`.
Headless PhysX validation produced:

- Runtime total mass: `30.958568572998 kg`
- Explicit URDF total mass: `30.958569270597 kg`
- Runtime body count: 15 (TITA's 9 bodies plus GLUON's 6 moving links)
- Runtime joint count: 14 (8 TITA plus 6 GLUON)
- Frame-only auxiliary bodies present: none
- Combined MOO environment smoke: `PASS` for 25 steps
- Policy action dimension: 8, policy observation dimension: 44
- Maximum GLUON WORK-pose hold error: `0.0191404819 rad`

The fixed mount and GLUON base inertia are transformed and accumulated into
`base_link`; the six revolute GLUON links and joints remain independent.  Isaac
Sim 5.1 emits a deprecation warning for merging fixed bodies that have inertia,
so a future-proof asset should eventually represent sensor poses as non-rigid
frames and pre-combine the mount/base inertias in the URDF.  This warning does
not invalidate the current runtime result.

## GLUON import fidelity

- GLUON bodies checked: base link plus links 1 through 6 (7 bodies)
- URDF GLUON mass: `4.267611380597 kg`
- PhysX runtime GLUON mass: `4.267611473799 kg`
- URDF mount mass: `1.000000000000 kg`
- PhysX GLUON plus mount mass: `5.267611473799 kg`
- Maximum per-body mass absolute error: `8.65340356038e-08 kg`
- Maximum inertia-tensor component absolute error: `2.32830643654e-10 kg m^2`
- GLUON URDF-to-PhysX comparison: `PASS`

The articulation uses `merge_fixed_joints=False`; the 1 kg mount,
GLUON base, and six moving links remain distinct PhysX rigid bodies.  Runtime
mass and inertia were read through `root_physx_view.get_masses()` and
`root_physx_view.get_inertias()` after the headless environment was created.

## Pre-fix combined-model defect evidence

The following URDF links contain no inertial definition.  Isaac Sim assigned
each one a runtime mass of exactly 1 kg:

| Body | Runtime mass |
|---|---:|
| `spad` | 1.0 kg |
| `spad1` | 1.0 kg |
| `left_camera` | 1.0 kg |
| `ch201` | 1.0 kg |
| `right_camara` | 1.0 kg |

- Phantom auxiliary mass: `5.000000000000 kg`
- Sum of explicitly defined URDF masses: `30.958569270597 kg`
- PhysX runtime total mass: `35.958568572998 kg`

These links are fixed around `x=0.2195` to `0.2405 m` ahead of `base_link`, so
the pre-fix defect changed not only total mass but also the combined center of
mass and rotational inertia.  Fixed-joint merging now prevents the importer-
default masses from entering the corrected articulation.

## Domain randomization scope

- Training-time mass and COM randomization selects only `base_link`.
- Broad startup all-body inertia and COM randomization is disabled in the
  combined TITA+GLUON configuration.
- GLUON mass and inertia therefore remain at the imported URDF values during
  training.

## Remaining physical-model uncertainty

This audit proves import fidelity, not hardware fidelity.  The GLUON and mount
values used by PhysX are exactly the values declared in the URDF, but the
`1.0 kg` mount value and all GLUON CAD-derived inertias still need comparison
against the measured real assembly, including cables and the eventual gripper.
