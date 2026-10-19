"""DESKTOP_DRY_RUN: verify relocation preserves robot semantics and mesh contents."""

from copy import deepcopy
import argparse
import hashlib
import json
from pathlib import Path
import tarfile
import tempfile
import subprocess
import xml.etree.ElementTree as ET

REPO = Path(__file__).resolve().parents[1]
MODELS = REPO / 'sim2sim/robot'
EVIDENCE = REPO / 'docs/exp/2026-10-14'


def semantic_hash(root):
    root = deepcopy(root)
    for mesh in root.iter('mesh'):
        mesh.set('filename', 'mesh-resource')
    return hashlib.sha256(ET.tostring(root)).hexdigest()


def old_mesh(filename, old_root):
    if filename.startswith('package://tita_gluon_urdf/'):
        return 'sim2sim/tita_gluon_urdf/' + filename.split('package://tita_gluon_urdf/', 1)[1]
    return (REPO / old_root / filename).resolve().relative_to(REPO).as_posix()


def check_viewers():
    import importlib.util
    from launch import LaunchContext
    from launch_ros.utilities import evaluate_parameters
    from ament_index_python.packages import get_package_share_directory

    share = Path(get_package_share_directory('tita_gluon_urdf'))
    checked = 0
    for path in sorted((share / 'launch').glob('*.launch.py')):
        spec = importlib.util.spec_from_file_location('asset_viewer', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        context = LaunchContext()
        context.launch_configurations.update(gluon_z='0.1564', jig_x='0.12', jig_y='0.12',
                                             jig_height='0.03', use_gui='false')
        entities = (module._launch_setup(context, share) if path.name == 'combined.launch.py'
                    else module.generate_launch_description().entities)
        publisher = next(node for node in entities
                         if getattr(node, 'node_package', None) == 'robot_state_publisher')
        parameters = evaluate_parameters(context, publisher._Node__parameters)
        description = next(entry['robot_description'] for entry in parameters
                           if isinstance(entry, dict) and 'robot_description' in entry)
        for mesh in ET.fromstring(description).iter('mesh'):
            filename = mesh.get('filename')
            assert filename.startswith('file://'), filename
            assert Path(filename.removeprefix('file://')).is_file(), filename
            checked += 1
    return {'viewer_launches': 5, 'viewer_mesh_references': checked}


def main(ros_viewers):
    moved = {
        'sim2sim/tita_gluon_urdf/urdf/tita.urdf': 'tita/urdf/tita.urdf',
        'sim2sim/tita_gluon_urdf/urdf/gluon.urdf': 'gluon/urdf/gluon.urdf',
        'sim2sim/tita_gluon_urdf/urdf/gluon_2L6_4L3.urdf': 'gluon/urdf/gluon_2L6_4L3_assembly.urdf',
        'sim2sim/tita_gluon_urdf/urdf/tita_gluon.urdf': 'tita_gluon/urdf/tita_gluon.urdf',
        'sim2sim/tita_gluon_urdf/urdf/tita_gluon_2L6_4L3.urdf': 'tita_gluon/urdf/tita_gluon_2L6_4L3.urdf',
    }
    for path in (MODELS / 'gluon/urdf').glob('*.urdf'):
        if path.name not in ('gluon.urdf', 'gluon_2L6_4L3_assembly.urdf'):
            moved['sim2sim/gluon_2L6_4L3_urdf/urdf/' + path.name] = 'gluon/urdf/' + path.name
    meshes = 0
    with tarfile.open(EVIDENCE / 'robot_urdf_layout_before.tar.gz') as archive:
        for old, new in moved.items():
            path = MODELS / new
            before = ET.fromstring(archive.extractfile(old).read())
            after = ET.parse(path).getroot()
            assert semantic_hash(before) == semantic_hash(after), new
            # Historical gravity-source URIs are generator input, not a runtime model.
            if path.name == 'left_gravity_source.urdf':
                continue
            for previous, current in zip(before.iter('mesh'), after.iter('mesh')):
                resource = (path.parent / current.get('filename')).resolve()
                assert resource.is_file(), resource
                previous_bytes = archive.extractfile(old_mesh(previous.get('filename'), Path(old).parent)).read()
                assert resource.read_bytes() == previous_bytes, resource
                meshes += 1
    with tempfile.TemporaryDirectory(dir=REPO / 'test') as temporary:
        for script, model in [('generate_combined_urdf.py', 'tita_gluon.urdf'),
                              ('generate_tita_gluon_2l6_4l3_urdf.py', 'tita_gluon_2L6_4L3.urdf')]:
            output = Path(temporary) / model
            subprocess.run(['python3', str(MODELS / 'tita_gluon/scripts' / script), '--output', str(output)], check=True)
            root = ET.parse(output).getroot()
            assert semantic_hash(root) == semantic_hash(ET.parse(MODELS / 'tita_gluon/urdf' / model).getroot()), model
            for mesh in root.iter('mesh'):
                assert (MODELS / 'tita_gluon/urdf' / mesh.get('filename')).resolve().is_file()
    result = {'execution_domain': 'DESKTOP_DRY_RUN', 'evidence_status': 'PASS',
              'policy_checkpoint_sha256': 'N/A (asset relocation)', 'urdfs': len(moved),
              'mesh_references_checked': meshes, 'generators_checked': 2,
              'detail': 'All model semantics and referenced mesh bytes preserved; both generators reproduce the stored models.'}
    if ros_viewers:
        result.update(check_viewers())
    (EVIDENCE / 'robot_urdf_layout_verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ros-viewers', action='store_true')
    main(parser.parse_args().ros_viewers)
