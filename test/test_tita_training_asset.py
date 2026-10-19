"""DESKTOP_DRY_RUN: compare historical TITA assets and verify training relocation."""

import ast
from copy import deepcopy
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OLD_COMMIT = "c8c159d37a6760916ed22a4d029961762bbde7a9"
OLD_PACKAGE = "tita_gluon_ws/src/ddt_ros2_control/urdfs/tita_description"
SOURCE = ROOT / "sim2sim/robot/tita/urdf/tita.urdf"
ASSET_CONFIG = ROOT / "lab/ddt_lab/ddt_lab/assets/ddt_robot.py"
SPHERE_CONFIG = ROOT / (
    "lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/real2sim/env_cfg.py"
)
FIXED_RENAMES = {name: name + "_joint" for name in ("spad", "spad1", "left_camera", "ch201")}


def historical_bytes(path):
    return subprocess.check_output(["git", "show", f"{OLD_COMMIT}:{path}"], cwd=ROOT)


def normalized_xml(root, historical=False):
    root = deepcopy(root)
    for node in root.iter():
        node.text = (node.text or "").strip() or None
        node.tail = None
        node.attrib = {key: value.strip() for key, value in sorted(node.attrib.items())}
        if node.tag == "mesh":
            node.set("filename", Path(node.get("filename")).name)
        if historical and node.tag == "joint" and node.get("name") in FIXED_RENAMES:
            assert node.get("type") == "fixed"
            node.set("name", FIXED_RENAMES[node.get("name")])
    return ET.tostring(root)


def sphere_converter(cache):
    tree = ast.parse(SPHERE_CONFIG.read_text())
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == "sphere_wheel_urdf")
    namespace = dict(Path=Path, ET=ET, os=os, hashlib=hashlib,
                     tempfile=SimpleNamespace(gettempdir=lambda: str(cache)),
                     WHEEL_LINKS=("left_leg_4", "right_leg_4"))
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(SPHERE_CONFIG), "exec"), namespace)
    return namespace["sphere_wheel_urdf"]


class HistoricalAssetTest(unittest.TestCase):
    def test_model_equivalent_except_resource_paths_fixed_names_and_whitespace(self):
        old_bytes = historical_bytes(f"{OLD_PACKAGE}/urdf/robot.urdf")
        old = ET.fromstring(old_bytes)
        new = ET.parse(SOURCE).getroot()
        self.assertNotEqual(old_bytes, SOURCE.read_bytes())
        self.assertEqual(normalized_xml(old, historical=True), normalized_xml(new))
        self.assertEqual(len([j for j in new.findall("joint") if j.get("type") != "fixed"]), 8)
        print(f"\nOld URDF SHA256: {hashlib.sha256(old_bytes).hexdigest()}")
        print(f"New URDF SHA256: {hashlib.sha256(SOURCE.read_bytes()).hexdigest()}")

    def test_all_nine_referenced_meshes_are_byte_identical(self):
        meshes = list(ET.parse(SOURCE).getroot().iter("mesh"))
        self.assertEqual(len(meshes), 9)
        for mesh in meshes:
            path = (SOURCE.parent / mesh.get("filename")).resolve()
            with self.subTest(mesh=path.name):
                self.assertTrue(path.is_file())
                self.assertEqual(path.read_bytes(), historical_bytes(f"{OLD_PACKAGE}/meshes/{path.name}"))


class TrainingAssetTest(unittest.TestCase):
    def test_training_config_references_existing_repository_asset(self):
        tree = ast.parse(ASSET_CONFIG.read_text())
        assignments = [node for node in tree.body if isinstance(node, ast.Assign)
                       and any(isinstance(target, ast.Name) and target.id == "DDT_TITA_URDF"
                               for target in node.targets)]
        namespace = dict(os=os, __file__=str(ASSET_CONFIG))
        exec(compile(ast.Module(body=assignments, type_ignores=[]), str(ASSET_CONFIG), "exec"), namespace)
        self.assertEqual(Path(namespace["DDT_TITA_URDF"]), SOURCE)
        cfg = next(node.value for node in tree.body if isinstance(node, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "DDT_TITA_CFG" for t in node.targets))
        spawn = next(kw.value for kw in cfg.keywords if kw.arg == "spawn")
        asset = next(kw.value for kw in spawn.keywords if kw.arg == "asset_path")
        self.assertEqual(eval(compile(ast.Expression(asset), str(ASSET_CONFIG), "eval"), namespace), str(SOURCE))

    def check_conversion(self, source, convert):
        before = ET.parse(source).getroot()
        output = Path(convert(str(source)))
        self.assertEqual(output, Path(convert(str(source))))
        actual = ET.parse(output).getroot()
        expected = deepcopy(before)
        for link in expected.findall("link"):
            if link.get("name") in ("left_leg_4", "right_leg_4"):
                for geometry in link.findall("collision/geometry"):
                    cylinder = geometry.find("cylinder")
                    radius = cylinder.get("radius")
                    geometry.remove(cylinder)
                    ET.SubElement(geometry, "sphere", radius=radius)
        # All other geometry, inertia, joints, limits, and visual properties must survive.
        self.assertEqual(normalized_xml(actual), normalized_xml(expected))
        for mesh in actual.iter("mesh"):
            path = Path(mesh.get("filename"))
            self.assertTrue(path.is_absolute(), mesh.get("filename"))
            self.assertTrue(path.is_file(), str(path))
            original = SOURCE.parent / "../meshes" / path.name
            self.assertEqual(path.read_bytes(), original.read_bytes())

    def test_relative_meshes_resolve_after_cached_sphere_conversion(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "test") as temporary:
            self.check_conversion(SOURCE, sphere_converter(Path(temporary)))

    def test_legacy_package_meshes_still_resolve_after_conversion(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "test") as temporary:
            package = Path(temporary) / "tita_description"
            source = package / "urdf/robot.urdf"
            source.parent.mkdir(parents=True)
            source.write_bytes(historical_bytes(f"{OLD_PACKAGE}/urdf/robot.urdf"))
            (package / "meshes").symlink_to(SOURCE.parent.parent / "meshes", target_is_directory=True)
            self.check_conversion(source, sphere_converter(Path(temporary) / "cache"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
