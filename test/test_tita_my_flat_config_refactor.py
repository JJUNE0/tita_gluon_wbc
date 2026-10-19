"""DESKTOP_DRY_RUN: preserve resolved TITA config values without starting Isaac Sim.

Execute the config declarations using Isaac Lab's real configclass decorator,
with symbolic MDP functions and simulator config leaves. The frozen snapshot
was generated from the pre-refactor rough -> flat -> my inheritance chain.
This checks configuration composition and manager term order, not physics.
"""

import ast
from copy import deepcopy
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest


ROOT = Path(__file__).resolve().parents[1]
TITA = ROOT / "lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita"
BASELINE = ROOT / "test/fixtures/tita_my_flat_config_before_refactor.json"


class ConfigLeaf:
    """Symbolic simulator/manager constructor retaining arguments and defaults."""

    def __init__(self, *args, **kwargs):
        self.__dict__.update(deepcopy(getattr(type(self), "defaults", {})))
        if args:
            self.name = args[0]
        self.__dict__.update(kwargs)

    def replace(self, **kwargs):
        result = deepcopy(self)
        result.__dict__.update(kwargs)
        return result


def leaf_type(name, defaults=None):
    return type(name, (ConfigLeaf,), {"defaults": defaults or {}})


class Symbols:
    def __init__(self, prefix):
        self.prefix = prefix
        self.values = {}

    def __getattr__(self, name):
        if name not in self.values:
            if name.endswith("Cfg"):
                value = leaf_type(name)
                value.Ranges = leaf_type("Ranges")
                value.OffsetCfg = leaf_type("OffsetCfg")
                value.InitialStateCfg = leaf_type("InitialStateCfg")
                value.JointDriveCfg = leaf_type("JointDriveCfg")
                value.JointDriveCfg.PDGainsCfg = leaf_type("PDGainsCfg")
            else:
                def value(*args, **kwargs):
                    raise AssertionError("Symbolic MDP functions must not run in a config test")
                value._symbol_name = f"{self.prefix}.{name}"
            self.values[name] = value
        return self.values[name]


def real_configclass():
    spec = importlib.util.find_spec("isaaclab")
    if spec is None:
        raise unittest.SkipTest("Run this config regression using the Isaac Lab Python environment")
    path = Path(next(iter(spec.submodule_search_locations))) / "utils/configclass.py"
    tree = ast.parse(path.read_text())
    # The real decorator is simulator-independent; dict conversion helpers are
    # unused here and would otherwise import the larger isaaclab.utils package.
    tree.body = [node for node in tree.body if not isinstance(node, ast.ImportFrom) or not node.level]
    module = ModuleType("_my_flat_real_configclass")
    sys.modules[module.__name__] = module
    module.class_to_dict = normalize
    module.update_class_from_dict = lambda *args, **kwargs: None
    exec(compile(tree, str(path), "exec"), module.__dict__)
    return module.configclass


def normalize(value):
    if isinstance(value, str) and value.startswith(str(ROOT)):
        return "<REPO_ROOT>" + value[len(str(ROOT)):]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        return {str(key): normalize(item) for key, item in value.items()}
    if callable(value):
        return getattr(value, "_symbol_name", value.__name__)
    fields = {key: normalize(item) for key, item in vars(value).items() if not key.startswith("_")}
    if isinstance(value, ConfigLeaf):
        fields["constructor"] = type(value).__name__
    return fields


def namespace():
    configclass = real_configclass()
    sim = Symbols("sim")
    sim.PhysxCfg.defaults = {"gpu_max_rigid_patch_count": 5 * 2**15}
    sim.SimulationCfg.defaults = {
        "dt": 0.01, "render_interval": 1, "disable_contact_processing": False,
        "physx": sim.PhysxCfg(), "physics_material": sim.RigidBodyMaterialCfg(),
    }

    default_simulation = sim.SimulationCfg()

    @configclass
    class ManagerBasedRLEnvCfg:
        sim: object = default_simulation
        seed: int | None = None

    @configclass
    class InteractiveSceneCfg:
        num_envs: int = 4096
        env_spacing: float = 2.5

    @configclass
    class ObsGroup:
        concatenate_terms: bool = True
        concatenate_dim: int = -1
        enable_corruption: bool = False
        history_length: int | None = None
        flatten_history_dim: bool = True

    sensor = leaf_type("ContactSensorCfg", {"update_period": 0.0})
    values = {
        "math": math, "os": os, "configclass": configclass, "mdp": Symbols("mdp"), "sim_utils": sim,
        "ManagerBasedRLEnvCfg": ManagerBasedRLEnvCfg, "InteractiveSceneCfg": InteractiveSceneCfg,
        "ObsGroup": ObsGroup, "ObsTerm": leaf_type("ObservationTermCfg"),
        "EventTerm": leaf_type("EventTermCfg"), "RewTerm": leaf_type("RewardTermCfg"),
        "DoneTerm": leaf_type("TerminationTermCfg"), "CurrTerm": leaf_type("CurriculumTermCfg"),
        "SceneEntityCfg": leaf_type("SceneEntityCfg"), "Unoise": leaf_type("AdditiveUniformNoiseCfg"),
        "ArticulationCfg": sim.ArticulationCfg, "AssetBaseCfg": leaf_type("AssetBaseCfg"),
        "ContactSensorCfg": sensor, "RayCasterCfg": sim.RayCasterCfg,
        "patterns": Symbols("patterns"), "TerrainImporterCfg": leaf_type("TerrainImporterCfg"),
        "ROUGH_TERRAINS_CFG": SimpleNamespace(curriculum=False),
        "DelayedPDActuatorCfg": leaf_type("DelayedPDActuatorCfg"),
        "DCMotorCfg": leaf_type("DCMotorCfg"), "ImplicitActuatorCfg": leaf_type("ImplicitActuatorCfg"),
    }
    asset_path = ROOT / "lab/ddt_lab/ddt_lab/assets/ddt_robot.py"
    asset_tree = ast.parse(asset_path.read_text())
    asset_tree.body = [node for node in asset_tree.body if isinstance(node, ast.Assign)
                       and isinstance(node.targets[0], ast.Name)
                       and node.targets[0].id in ("DDT_MODEL_DIR", "DDT_TITA_CFG")]
    values["__file__"] = str(asset_path)
    exec(compile(asset_tree, str(asset_path), "exec"), values)
    return values


def load_configs(legacy=False, values=None):
    values = namespace() if values is None else values
    paths = [TITA / "my_flat_env_cfg.py"]
    if legacy:
        paths = [TITA / "rough_env_cfg.py", TITA / "flat_env_cfg.py", *paths]
    module = ModuleType("_my_flat_config_fixture")
    sys.modules[module.__name__] = module
    module.__dict__.update(values)
    for path in paths:
        tree = ast.parse(path.read_text())
        tree.body = [node for node in tree.body if not isinstance(node, (ast.Import, ast.ImportFrom))]
        module.__file__ = str(path)
        exec(compile(tree, str(path), "exec"), module.__dict__)
    return module


def snapshot(cfg):
    result = {"config": normalize(cfg), "manager_order": {}}
    for name in ("actions", "commands", "rewards", "events", "terminations", "curriculum"):
        result["manager_order"][name] = [key for key, value in vars(getattr(cfg, name)).items()
                                        if isinstance(value, ConfigLeaf)]
    result["manager_order"]["observation_groups"] = [
        key for key, value in vars(cfg.observations).items() if value is not None
    ]
    for name, group in vars(cfg.observations).items():
        if group is not None:
            result["manager_order"][f"observations.{name}"] = [
                key for key, value in vars(group).items() if isinstance(value, ConfigLeaf)
            ]
    return result


class MyFlatConfigRefactorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_configs()
        cls.baseline = json.loads(BASELINE.read_text())

    def test_train_and_play_keep_all_pre_refactor_values_and_term_order(self):
        for name in ("MyTitaFlatEnvCfg", "MyTitaFlatEnvCfg_PLAY"):
            with self.subTest(config=name):
                self.assertEqual(snapshot(getattr(self.module, name)()), self.baseline[name])

    def test_task_is_independent_of_rough_and_flat_configs(self):
        tree = ast.parse((TITA / "my_flat_env_cfg.py").read_text())
        self.assertFalse(any(isinstance(node, ast.ImportFrom)
                             and node.module in ("rough_env_cfg", "flat_env_cfg") for node in ast.walk(tree)))
        self.assertEqual(self.module.MyTitaFlatEnvCfg.__bases__, (self.module.ManagerBasedRLEnvCfg,))
        cfg = self.module.MyTitaFlatEnvCfg()
        for name in ("scene", "actions", "commands", "observations", "rewards", "events", "terminations", "curriculum"):
            self.assertEqual(type(getattr(cfg, name)).__module__, self.module.__name__)

    def test_instance_and_play_mutations_do_not_leak_into_training(self):
        first = self.module.MyTitaFlatEnvCfg()
        second = self.module.MyTitaFlatEnvCfg()
        self.module.MyTitaFlatEnvCfg_PLAY()
        first.events.reset_base.params["pose_range"]["x"] = (-99.0, 99.0)
        first.scene.robot.actuators["legs"].max_delay = 999
        first.rewards.track_lin_vel_xy_exp.weight = 999
        self.assertEqual(snapshot(second), self.baseline["MyTitaFlatEnvCfg"])

    def test_legacy_config_class_names_remain_resolvable(self):
        self.assertIs(self.module.MyEventCfg, self.module.EventCfg)
        self.assertIs(self.module.MyRampedCommandsCfg, self.module.CommandsCfg)
        self.assertIs(type(self.module.MyTitaFlatEnvCfg().observations.estimator_target), self.module.EstimatorTargetCfg)

    def test_installed_simulation_config_accepts_train_and_play_declarations(self):
        # Use the installed constructor to catch API changes hidden by symbolic
        # leaves, while keeping simulator/native modules out of this test.
        values = namespace()
        spec = importlib.util.find_spec("isaaclab")
        path = Path(next(iter(spec.submodule_search_locations))) / "sim/simulation_cfg.py"
        tree = ast.parse(path.read_text())
        tree.body = [node for node in tree.body if not isinstance(node, ast.ImportFrom)
                     or (not node.level and node.module != "isaaclab.utils")]
        simulation = ModuleType("_my_flat_installed_sim_config")
        sys.modules[simulation.__name__] = simulation
        simulation.configclass = values["configclass"]
        simulation.RigidBodyMaterialCfg = values["sim_utils"].RigidBodyMaterialCfg
        exec(compile(tree, str(path), "exec"), simulation.__dict__)
        values["sim_utils"].SimulationCfg = simulation.SimulationCfg
        values["sim_utils"].PhysxCfg = simulation.PhysxCfg
        module = load_configs(values=values)
        for name in ("MyTitaFlatEnvCfg", "MyTitaFlatEnvCfg_PLAY"):
            with self.subTest(config=name):
                cfg = getattr(module, name)()
                self.assertIsInstance(cfg.sim, simulation.SimulationCfg)
                self.assertTrue(cfg.sim.disable_contact_processing)
                self.assertEqual(cfg.sim.dt, 0.005)
                self.assertEqual(cfg.sim.render_interval, cfg.decimation)


if __name__ == "__main__":
    if "--write-baseline" in sys.argv:
        module = load_configs(legacy=True)
        values = {name: snapshot(getattr(module, name)())
                  for name in ("MyTitaFlatEnvCfg", "MyTitaFlatEnvCfg_PLAY")}
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps(values, indent=2) + "\n")
        print(f"DESKTOP_DRY_RUN baseline saved: {BASELINE}")
    else:
        unittest.main(verbosity=2)
