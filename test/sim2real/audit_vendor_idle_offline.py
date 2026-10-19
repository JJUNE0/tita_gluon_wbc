"""DESKTOP_DRY_RUN: compare copied healthy/idle vendor bags; no ROS node or network."""
from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import struct

import numpy as np
from diagnostic_msgs.msg import DiagnosticArray
from rclpy.serialization import deserialize_message
from sensor_msgs.msg import Imu, JointState, Joy

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'docs/exp/2026-10-18'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_bag(path):
    with sqlite3.connect(f'file:{path.resolve()}?mode=ro', uri=True) as conn:
        assert conn.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        topics = dict(conn.execute('SELECT name,id FROM topics'))
        counts = dict(conn.execute('SELECT t.name,COUNT(m.id) FROM topics t LEFT JOIN messages m '
                                  'ON m.topic_id=t.id GROUP BY t.id'))
        rows = lambda name: conn.execute('SELECT timestamp,data FROM messages WHERE topic_id=? '
                                        'ORDER BY timestamp', (topics[name],)).fetchall()
        diagnostics = Counter()
        status = rows('/tita4252763/system/status')
        for _, blob in status:
            for item in deserialize_message(blob, DiagnosticArray).status:
                diagnostics.update((v.key, v.value) for v in item.values)
        timings = {}
        for name, cls in (('joy', Joy), ('imu_sensor_broadcaster/imu', Imu), ('joint_states', JointState)):
            data = rows('/tita4252763/'+name)
            timing = []
            messages = []
            for received, blob in data:
                msg = deserialize_message(blob, cls)
                stamp = msg.header.stamp.sec+msg.header.stamp.nanosec*1e-9
                timing.append((received*1e-9, stamp))
                if cls is Joy:
                    messages.append(list(msg.axes))
            a = np.array(timing)
            assert len(a) > 1
            timings[name] = dict(samples=len(a), first_receive_s=float(a[0, 0]),
                last_receive_s=float(a[-1, 0]),
                approximate_hz=float((len(a)-1)/(a[-1, 0]-a[0, 0])),
                header_monotonic=bool((np.diff(a[:, 1]) > 0).all()),
                receive_minus_header_ms_p0_p50_p100=np.percentile((a[:, 0]-a[:, 1])*1000, [0, 50, 100]).tolist())
            if messages:
                x = np.array(messages)
                timings[name]['axes_min'] = x.min(0).tolist()
                timings[name]['axes_max'] = x.max(0).tolist()
    return dict(source_db=str(path), sha256=digest(path), sqlite_quick_check='PASS',
                topic_counts=counts, diagnostic_samples=len(status),
                diagnostics={key: dict((state, n) for (name, state), n in diagnostics.items() if name == key)
                             for key, _ in diagnostics}, sensor_timing=timings)


def audit_can(path):
    ids, modes = Counter(), Counter()
    first = None
    last = None
    pattern = re.compile(r'\(([^)]+)\)\s+\S+\s+([0-9A-Fa-f]+)(?:##[0-9A-Fa-f]|#)([0-9A-Fa-f]*)\s*')
    for line in path.open():
        m = pattern.fullmatch(line)
        assert m, line[:100]
        stamp, cid, payload = float(m[1]), int(m[2], 16), bytes.fromhex(m[3])
        if first is None:
            first = stamp
        last = stamp
        ids[cid] += 1
        if cid == 0x103 and len(payload) >= 7 and struct.unpack_from('<H', payload, 4)[0] == 0x1001:
            modes[payload[6]] += 1
    assert first is not None and last > first
    return dict(source=str(path), sha256=digest(path), seconds=last-first,
                id_counts={hex(k): v for k, v in sorted(ids.items())}, locomotion_status_0x1001=dict(modes),
                rpc_0x170=ids[0x170], direct_motor_frames=sum(ids[i] for i in range(0x120, 0x124)),
                channel_input_0x12d=ids[0x12d],
                limitation='Locomotion status0 is not MCU Direct mode. Capture starts after fault; prior mode unknown.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    paths = {
        'healthy_stand': next((BASE/'vendor_supported_stand_review/vendor_supported_stand_capture').glob('*_bag/*.db3')),
        'healthy_commands': next((BASE/'vendor_supported_stand_review/vendor_baseline_capture').glob('*_bag/*.db3')),
        'idle_problem': next((BASE/'vendor_lqr_capture_session').glob('*_bag/*.db3'))}
    cases = {name: audit_bag(path) for name, path in paths.items()}
    for key in ('Joy', 'BodyImu', 'Robot'):
        for name in ('healthy_stand', 'healthy_commands'):
            assert cases[name]['diagnostics'][key] == {'OK': cases[name]['diagnostic_samples']}
        assert cases['idle_problem']['diagnostics'][key] == {'Timeout': cases['idle_problem']['diagnostic_samples']}
    problem = cases['idle_problem']['topic_counts']
    assert problem['/tita4252763/command/passive/command'] == 0
    assert problem['/tita4252763/robot_vel'] == 0
    for signal in cases['idle_problem']['sensor_timing'].values():
        assert signal['header_monotonic']
        assert signal['receive_minus_header_ms_p0_p50_p100'][2] < 20
    report = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS (extraction); SUSPICIOUS (cause)',
        vendor_checkpoint_sha256='N/A', cases=cases,
        can=audit_can(BASE/'vendor_lqr_capture_session/vendor_stand_171439_905205199_can.log'),
        source_sha256=digest(Path(__file__)),
        limitations=['No healthy-to-idle transition in copied trace.',
                     'Header freshness at recorder does not prove another vendor node receives data.',
                     'No new hardware access; source-to-SBC copy verification remains pending.'])
    (args.output/'audit.json').write_text(json.dumps(report, indent=2)+'\n')
    for name, case in cases.items():
        print(name, 'diagnostics', case['diagnostic_samples'],
              {k: case['diagnostics'][k] for k in ('Joy', 'BodyImu', 'Robot')},
              'passive frames', case['topic_counts']['/tita4252763/command/passive/command'])
    print('PASS DESKTOP_DRY_RUN: readonly SQLite/CAN decode, healthy comparison, sensor header checks')


if __name__ == '__main__':
    main()
