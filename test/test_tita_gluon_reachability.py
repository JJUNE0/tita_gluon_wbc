import numpy as np

from analyze_tita_gluon_reachability import (
    DEFAULT_COMBINED_URDF,
    connected_voxels_from_seed,
    load_tita_to_gluon_transform,
    transform_points,
    voxel_surface_mesh,
)


def test_combined_mount_transform_matches_documented_draft() -> None:
    transform = load_tita_to_gluon_transform(DEFAULT_COMBINED_URDF)
    np.testing.assert_allclose(transform[:3, 3], [0.0, 0.0, 0.1564], atol=1e-12)
    np.testing.assert_allclose(transform[:3, :3] @ [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], atol=1e-10)
    point = transform_points(transform, np.array([[0.1205, 0.0, 0.0]]))[0]
    np.testing.assert_allclose(point, [0.0, 0.0, 0.2769], atol=1e-9)


def test_connected_voxels_keeps_only_seed_component() -> None:
    voxels = np.array(
        [[0, 0, 0], [1, 1, 1], [2, 2, 2], [10, 10, 10]], dtype=np.int32
    )
    mask = connected_voxels_from_seed(voxels, np.array([0, 0, 0]))
    np.testing.assert_array_equal(mask, [True, True, True, False])


def test_voxel_surface_does_not_fill_unoccupied_gap() -> None:
    one_vertices, one_faces = voxel_surface_mesh(np.array([[0, 0, 0]]), 0.01)
    assert one_vertices.shape == (8, 3)
    assert one_faces.shape == (12, 3)

    separated_vertices, separated_faces = voxel_surface_mesh(
        np.array([[0, 0, 0], [2, 0, 0]]), 0.01
    )
    assert separated_vertices.shape == (16, 3)
    assert separated_faces.shape == (24, 3)
