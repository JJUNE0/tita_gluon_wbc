"""DESKTOP_DRY_RUN: export nominal compiled MuJoCo FK constants; no robot access."""
import hashlib
from pathlib import Path
import mujoco
root = Path(__file__).resolve().parents[2]
model = mujoco.MjModel.from_xml_path(str(root/'tita_gluon_ws/src/ddt_ros2_control/urdfs/tita_description/mujoco_corrected/scene.xml'))
def values(a):
    return '{' + ', '.join(format(float(x), '.17g') for x in a) + '}'
lines = ['// Nominal corrected MuJoCo geometry; regenerate with test/sim2real/generate_sit_geometry.py.',
         '// Encoder/IMU only at runtime. No MuJoCo dependency on the robot.', '#pragma once',
         '#include <array>', 'namespace tita {',
         'struct SitBody { int parent; std::array<double, 3> pos; std::array<double, 4> quat;',
         '  std::array<double, 3> com; double mass; };', 'constexpr std::array<SitBody, 9> kSitBodies{{']
for i in range(1, 10):
    pos = model.body_pos[i] if i != 1 else [0., 0., 0.]
    lines.append('  {' + str(int(model.body_parentid[i])-1) + ', ' + values(pos) + ', ' + values(model.body_quat[i]) + ', ' + values(model.body_ipos[i]) + ', ' + format(model.body_mass[i], '.17g') + '},')
lines += ['}};', '}  // namespace tita', '']
p = root/'sim2real/tita_ws/src/tita_controller/include/tita_controller/sit_geometry.hpp'
p.write_text('\n'.join(lines)); print('DESKTOP_DRY_RUN:', p, hashlib.sha256(p.read_bytes()).hexdigest())
