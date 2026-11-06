"""DESKTOP_DRY_RUN: checkpoint/video cadence and W&B media ownership.

Uses real CPU learner updates with fake Isaac/W&B and a fake render process.
All fixture/checkpoint files are under test/. No GPU or network is requested.
"""

import json
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest
from unittest.mock import patch

import test_flash_sac_wandb as wandb_tests
import torch._dynamo  # Keep C++ registrations alive across patch.dict(sys.modules) contexts.
from runtime import validate_training_args

REPO, train = wandb_tests.REPO, wandb_tests.train


class VideoSDK(wandb_tests.FakeWandbSDK):
    @staticmethod
    def Video(path, format):
        return {"video_path": path, "format": format}


def render_fixture(command, **kwargs):
    """Emulate a completed, hash-bound evaluation without launching Isaac."""
    assert kwargs["check"] and kwargs["timeout"] == 300
    checkpoint = Path(command[command.index("--checkpoint") + 1])
    video = Path(command[command.index("--video") + 1])
    result = Path(command[command.index("--video_result") + 1])
    count = int(command[command.index("--steps") + 1])
    metadata = json.loads((checkpoint / "ddt.json").read_text())
    video.write_bytes(b"fake-mp4-for-orchestration-check")
    result.write_text(json.dumps({"evidence_status": "PASS", "frames": count,
                                  "checkpoint_sha256": metadata["actor_sha256"]}))


class FlashSACVideoTest(unittest.TestCase):
    def invoke(self, directory, sdk, extra=()):
        # Reuse the fixture setup; these are not separate inherited test cases.
        helper = wandb_tests.FlashSACWandbTest()
        helper.setUp()
        helper.invoke(directory, sdk, ["--steps", "6", "--video_interval", "3", "--video_length", "2", *extra])

    def test_new_defaults_and_invalid_video_parameters(self):
        args = train.build_parser().parse_args([])
        self.assertEqual((args.logger, args.wandb_mode, args.video_interval, args.video_length),
                         ("wandb", "online", 10000, 500))
        for option, value in (("--video_interval", "-1"), ("--video_length", "0")):
            with self.assertRaisesRegex(ValueError, "video_interval"):
                validate_training_args(train.build_parser().parse_args([option, value]))
        validate_training_args(train.build_parser().parse_args(["--video_interval", "0"]))

    def test_video_interval_saves_its_checkpoint_even_between_regular_saves(self):
        sdk = VideoSDK()
        with tempfile.TemporaryDirectory(prefix="flash_sac_video_", dir=REPO / "test") as directory:
            fixture = Path(directory)
            with patch("video_logging.subprocess.run", side_effect=render_fixture) as renderer:
                self.invoke(fixture, sdk)
            self.assertEqual(renderer.call_count, 2)
            checkpoints = list(fixture.glob("isaac_lab/ddt_lab/logs/flash_sac/*/model_*"))
            self.assertEqual({p.name for p in checkpoints}, {"model_3", "model_4", "model_6"})
            run = sdk.runs[0]
            videos = [row for row in run.metrics if "video/rollout" in row]
            self.assertEqual([row["video/checkpoint_step"] for row in videos], [3, 6])
            for row in videos:
                self.assertNotIn("step", row)  # No backdated training/history step.
                self.assertEqual(len(row["video/checkpoint_sha256"]), 64)
                self.assertEqual(row["video/rollout"]["format"], "mp4")
            records = list(fixture.glob("docs/exp/*/*_videos/*_wandb.json"))
            self.assertEqual(len(records), 2)
            self.assertTrue(all(json.loads(p.read_text())["evidence_status"] == "PASS" for p in records))
            self.assertEqual(run.summary["video/failures"], 0)
            self.assertEqual(run.finish_codes, [0])  # Final clip is drained before run.finish.

    def test_training_reaches_final_step_while_video_renderer_is_waiting(self):
        reached_final = threading.Event()

        class ProgressSDK(VideoSDK):
            def init(self, **values):
                run = super().init(**values)
                original_log = run.log

                def log(row):
                    if row.get("step") == 6:
                        reached_final.set()
                    original_log(row)

                run.log = log
                return run

        def delayed_render(command, **kwargs):
            if not reached_final.wait(timeout=10):
                raise RuntimeError("Learning blocked while video rendering was pending")
            render_fixture(command, **kwargs)

        sdk = ProgressSDK()
        with tempfile.TemporaryDirectory(prefix="flash_sac_video_async_", dir=REPO / "test") as directory:
            with patch("video_logging.subprocess.run", side_effect=delayed_render):
                self.invoke(Path(directory), sdk)
            self.assertTrue(reached_final.is_set())
            self.assertEqual(sdk.runs[0].summary["video/failures"], 0)

    def test_render_failure_is_recorded_without_killing_learning(self):
        sdk = VideoSDK()
        with tempfile.TemporaryDirectory(prefix="flash_sac_video_failure_", dir=REPO / "test") as directory:
            fixture = Path(directory)
            with patch("video_logging.subprocess.run", side_effect=subprocess.TimeoutExpired("renderer", 300)):
                self.invoke(fixture, sdk)
            self.assertEqual(sdk.runs[0].summary["vector_steps"], 6)
            self.assertEqual(sdk.runs[0].summary["video/failures"], 2)
            records = list(fixture.glob("docs/exp/*/*_videos/*_wandb.json"))
            self.assertTrue(all(json.loads(p.read_text())["evidence_status"] == "FAIL" for p in records))
            self.assertFalse(any("video/rollout" in row for row in sdk.runs[0].metrics))

    def test_video_disabled_does_not_launch_a_renderer(self):
        sdk = VideoSDK()
        with tempfile.TemporaryDirectory(prefix="flash_sac_video_disabled_", dir=REPO / "test") as directory:
            with patch("video_logging.subprocess.run") as renderer:
                self.invoke(Path(directory), sdk, ["--video_interval", "0"])
            renderer.assert_not_called()

    def test_wrong_checkpoint_hash_prevents_media_upload(self):
        def wrong_hash(command, **kwargs):
            render_fixture(command, **kwargs)
            result = Path(command[command.index("--video_result") + 1])
            values = json.loads(result.read_text())
            values["checkpoint_sha256"] = "0" * 64
            result.write_text(json.dumps(values))

        sdk = VideoSDK()
        with tempfile.TemporaryDirectory(prefix="flash_sac_video_hash_", dir=REPO / "test") as directory:
            with patch("video_logging.subprocess.run", side_effect=wrong_hash):
                self.invoke(Path(directory), sdk)
            self.assertEqual(sdk.runs[0].summary["video/failures"], 2)
            self.assertFalse(any("video/rollout" in row for row in sdk.runs[0].metrics))


if __name__ == "__main__":
    unittest.main(verbosity=2)
