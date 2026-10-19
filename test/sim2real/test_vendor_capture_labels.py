"""DESKTOP_DRY_RUN: capture argument gates with all robot/environment calls stubbed."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT/'test/sim2real/capture_vendor_baseline.sh'
STUB = '''
source() { :; }
mkdir() { echo ARGUMENTS_ACCEPTED_NO_CAPTURE_STARTED; exit 77; }
systemctl() { echo UNEXPECTED_ROBOT_CALL >&2; exit 91; }
export -f source mkdir systemctl
exec bash "$@"
'''


class CaptureLabels(unittest.TestCase):
    def run_gate(self, duration, label):
        return subprocess.run(['bash', '-c', STUB, 'capture-label-test', str(SCRIPT), duration, label],
                              text=True, capture_output=True, timeout=3)

    def test_user_labels_and_original_labels_reach_capture_boundary(self):
        for duration, label in [('60', 'stand_high'), ('120', 'stand_high_push'), ('60', 'stand_mid'),
                                ('60', 'stand'), ('120', 'commands'), ('180', 'Trial-2_push'),
                                ('10', 'x'*64)]:
            with self.subTest(label=label):
                result = self.run_gate(duration, label)
                self.assertEqual(result.returncode, 77, result.stderr)
                self.assertIn('ARGUMENTS_ACCEPTED_NO_CAPTURE_STARTED', result.stdout)

    def test_invalid_labels_are_explicit_and_do_not_start_capture(self):
        for label in ['../escape', 'stand high', '-stand', '_stand', 'x'*65, 'stand;true', '$(true)']:
            with self.subTest(label=label):
                result = self.run_gate('60', label)
                self.assertEqual(result.returncode, 2)
                self.assertIn('ERROR: label', result.stderr)
                self.assertIn('capture not started', result.stderr)
                self.assertEqual(result.stdout, '')

    def test_invalid_durations_are_explicit_and_do_not_start_capture(self):
        for duration in ['9', '181', '-1', '60.5', 'abc']:
            with self.subTest(duration=duration):
                result = self.run_gate(duration, 'stand_high')
                self.assertEqual(result.returncode, 2)
                self.assertIn('ERROR: duration', result.stderr)
                self.assertEqual(result.stdout, '')

    def test_operator_sed_patch_on_original_script(self):
        original = ROOT/'docs/exp/2026-10-18/vendor_capture_labels/capture_vendor_baseline.before.txt'
        with tempfile.TemporaryDirectory(dir=ROOT/'test/sim2real') as tmp:
            target = Path(tmp)/'capture_vendor_baseline.sh'
            target.write_bytes(original.read_bytes())
            result = subprocess.run(['sed', '-i.before_labels.bak',
                r's/\^(stand|commands)\$/^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$/', str(target)],
                text=True, capture_output=True, timeout=3)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(Path(str(target)+'.before_labels.bak').read_bytes(), original.read_bytes())
            self.assertNotIn('^(stand|commands)$', target.read_text())
            for label in ['stand_high', 'stand_high_push', 'stand_mid']:
                result = subprocess.run(['bash', '-c', STUB, 'patched-label-test', str(target), '60', label],
                                        text=True, capture_output=True, timeout=3)
                self.assertEqual(result.returncode, 77, result.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
