from glob import glob
from setuptools import setup

name = 'sim2sim_ros2_jazzy'
setup(name=name, version='0.1.0', packages=[name],
      data_files=[('share/ament_index/resource_index/packages', ['resource/' + name]),
                  ('share/' + name, ['package.xml']), ('share/' + name + '/launch', glob('launch/*.launch.py')),
                  ('share/' + name + '/config', glob('config/*.yaml'))],
      install_requires=['setuptools', 'numpy', 'PyYAML'], zip_safe=True,
      maintainer='TITA research', maintainer_email='research@example.com',
      description='TITA PPO and FlashSAC MuJoCo playback and read-only ROS state mirror', license='BSD-3-Clause',
      entry_points={'console_scripts': ['sim2sim = sim2sim_ros2_jazzy.cli:main',
                                        'real2sim = sim2sim_ros2_jazzy.real2sim_node:main']})
