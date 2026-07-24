from glob import glob

from setuptools import find_packages, setup


package_name = "tita_low_level_sdk"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", glob("launch/*.launch.py")),
        ("share/" + package_name + "/config", glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="cocel",
    maintainer_email="cocel@example.com",
    description="Fail-closed TITA low-level precheck, ownership lifecycle, and asynchronous logging.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "dryrun_node = tita_low_level_sdk.dryrun_node:main",
            "low_level_discovery = tita_low_level_sdk.low_level_discovery:main",
            "direct_rl_controller_node = tita_low_level_sdk.direct_rl_controller_node:main",
            "stage1_production_preflight = tita_low_level_sdk.stage1_production_preflight:main",
            "stage2_production_preflight = tita_low_level_sdk.stage2_production_preflight:main",
            "estimator_diagnostic_logger = tita_low_level_sdk.estimator_diagnostic_logger:main",
        ],
    },
)
