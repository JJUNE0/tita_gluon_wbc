"""DESKTOP_DRY_RUN: body-frame telemetry and encoded video with fake Isaac."""

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import test_flash_sac_entrypoints as fixture
import numpy as np
import torch
import torch._dynamo  # Initialize before fake-module contexts.

play, train = fixture.play, fixture.train


def telemetry_env(command=(0.25, -0.5, 0.0), actual=(-0.125, 0.375, 0.0)):
    return SimpleNamespace(
        command_manager=SimpleNamespace(get_command=lambda name: torch.tensor([command])),
        scene={"robot": SimpleNamespace(data=SimpleNamespace(
            root_lin_vel_b=torch.tensor([actual]), root_lin_vel_w=torch.tensor([[9., 9., 9.]]),
        ))},
    )


class VelocityOverlayTest(unittest.TestCase):
    def test_reads_emitted_command_and_body_velocity_without_scaling(self):
        sample = play.read_velocity_sample(telemetry_env())
        self.assertEqual(sample, {"command": [0.25, -0.5], "actual": [-0.125, 0.375]})

    def test_nonfinite_command_or_actual_velocity_rejected(self):
        for args in ({"command": (float("nan"), 0., 0.)}, {"actual": (0., float("inf"), 0.)}):
            with self.subTest(args=args), self.assertRaisesRegex(RuntimeError, "Non-finite velocity"):
                play.read_velocity_sample(telemetry_env(**args))

    def test_overlay_preserves_rgb_dimensions_and_original_scene(self):
        frame = np.full((480, 640, 3), 90, dtype=np.uint8)
        before = frame.copy()
        drawn = play.draw_velocity_overlay(frame, play.read_velocity_sample(telemetry_env()))
        self.assertEqual(drawn.shape, frame.shape)
        self.assertEqual(drawn.dtype, frame.dtype)
        np.testing.assert_array_equal(frame, before)
        np.testing.assert_array_equal(drawn[130:], frame[130:])
        self.assertTrue(np.any(np.all(drawn[:, :, :3] == (255, 210, 90), axis=2)))
        self.assertTrue(np.any(np.all(drawn[:, :, :3] == (100, 230, 255), axis=2)))

    def test_play_encodes_overlay_and_records_matching_telemetry(self):
        import imageio.v2 as imageio

        class VideoEnv(fixture.FakeNativeEnv):
            def __init__(self, cfg, render_mode=None):
                super().__init__(cfg)
                values = telemetry_env()
                self.command_manager, self.scene = values.command_manager, values.scene
                self.step_dt = 0.02

            def render(self):
                return np.full((480, 640, 3), 90, dtype=np.uint8)

        modules = fixture.mocked_isaac_modules()
        modules["isaaclab.envs"].ManagerBasedRLEnv = VideoEnv
        original_parse = modules["isaaclab_tasks.utils"].parse_env_cfg

        def parse(*args, **kwargs):
            cfg = original_parse(*args, **kwargs)
            cfg.viewer = SimpleNamespace()
            cfg.decimation = 4
            return cfg

        modules["isaaclab_tasks.utils"].parse_env_cfg = parse
        with tempfile.TemporaryDirectory(prefix="flash_sac_velocity_", dir=fixture.REPO / "test") as directory:
            root = Path(directory)
            video, result = root / "overlay.mp4", root / "overlay.json"
            with patch.dict(sys.modules, modules), patch.object(train, "REPO_ROOT", root), \
                    patch.object(play, "REPO_ROOT", root), redirect_stdout(io.StringIO()):
                with patch.object(sys, "argv", [
                    "train.py", "--device", "cpu", "--num_envs", "4", "--steps", "2",
                    "--buffer_size", "64", "--min_buffer", "8", "--batch_size", "4", "--n_step", "1",
                    "--updates_per_step", "1", "--save_every", "2", "--log_every", "1", "--logger", "console",
                ]):
                    train.main()
                checkpoint = next(root.glob("isaac_lab/ddt_lab/logs/flash_sac/*/model_2"))
                with patch.object(sys, "argv", [
                    "play.py", "--checkpoint", str(checkpoint), "--num_envs", "1", "--steps", "2",
                    "--device", "cpu", "--headless", "--video", str(video), "--video_result", str(result),
                ]):
                    play.main()
            recorded = json.loads(result.read_text())
            self.assertEqual(recorded["evidence_status"], "PASS")
            self.assertEqual((recorded["frames"], recorded["fps"]), (2, 50))
            overlay = recorded["velocity_overlay"]
            self.assertEqual((overlay["enabled"], overlay["frame"], overlay["units"]), (True, "body", "m/s"))
            self.assertEqual(overlay["samples"], [
                {"frame": i, "command": [0.25, -0.5], "actual": [-0.125, 0.375]} for i in range(2)
            ])
            reader = imageio.get_reader(video)
            try:
                self.assertEqual(reader.count_frames(), 2)
                frame = reader.get_data(0)
                self.assertGreater(float(frame[10:112, 10:330].std()), 20.)
            finally:
                reader.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
