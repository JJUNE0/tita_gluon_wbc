# Published LPF60 reference pair

Execution Domain: DESKTOP_DRY_RUN / VALIDATION_SIM.

Only Teacher80k (`20261108/80000`) and LPF60 residual10k
(`20261109/10000_d6672529ee24`) are included. Both live under
`mjlab/task/base_velocity/height_roll_pitch/`. The residual bundle contains its
paired Teacher sidecars so native export does not depend on historical logs.
Identical weights in the two domain stores share Git blob objects.

Weight SHA256: Teacher `5487e3584fddbdfc87b7485bb2ad4c7da8069a7679b1975789d64419e7482334`;
residual `d6672529ee247a92b7043f50bb6deb501a65becbf760761a412b33d5701b6002`.
Existing absolute source paths in metadata are provenance, not installation
requirements. Playback regenerates local export caches for the current checkout.
Included hardware export contracts are hash-validated artifacts, not permission
to operate a robot. See [the guide](../../docs/lpf60_residual.md).
