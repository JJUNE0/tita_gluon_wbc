"""ROBOT_STATE_CHANGING: current Teacher plus the hardware-tested48k torque residual."""
import importlib.util
from pathlib import Path


def generate_launch_description():
    spec=importlib.util.spec_from_file_location('_policy_launch',Path(__file__).with_name('_policy_launch.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.description(module.RESIDUAL_NAME)
