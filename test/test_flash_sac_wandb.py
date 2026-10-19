"""DESKTOP_DRY_RUN: W&B wiring with a fake SDK/Isaac and real CPU FlashSAC.

No credentials, network connection or W&B backend process are used. Temporary
checkpoints and evidence directories are created only inside test/ and removed.
"""

import builtins
from contextlib import ExitStack, redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

from test_flash_sac_entrypoints import FakeApp, FakeNativeEnv, REPO, mocked_isaac_modules, train


class FakeWandbRun:
    def __init__(self, values, count, fail_log=False, fail_finish=False):
        self.id = values["id"] or f"fake-run-{count}"
        self.name = values["name"]
        self.offline = values["mode"] == "offline"
        self.url = None
        self.summary = {}
        self.metrics = []
        self.definitions = []
        self.finish_codes = []
        self.fail_log = fail_log
        self.fail_finish = fail_finish

    def define_metric(self, name, **kwargs):
        self.definitions.append((name, kwargs))

    def log(self, metrics):
        if self.fail_log:
            raise RuntimeError("injected W&B log failure")
        self.metrics.append(dict(metrics))

    def finish(self, exit_code):
        self.finish_codes.append(exit_code)
        if self.fail_finish:
            raise RuntimeError("injected W&B finish failure")


class FakeWandbSDK(ModuleType):
    def __init__(self, fail_log=False, fail_finish=False):
        super().__init__("wandb")
        self.calls = []
        self.runs = []
        self.fail_log = fail_log
        self.fail_finish = fail_finish

    def init(self, **values):
        self.calls.append(values)
        run = FakeWandbRun(values, len(self.calls), self.fail_log, self.fail_finish)
        self.runs.append(run)
        return run


class FlashSACWandbTest(unittest.TestCase):
    def setUp(self):
        FakeApp.instances.clear()
        FakeNativeEnv.instances.clear()

    def invoke(self, fixture, sdk, extra=(), logger="wandb", import_events=None):
        modules = mocked_isaac_modules()
        original_parse = modules["isaaclab_tasks.utils"].parse_env_cfg

        def parse_env_cfg(*args, **kwargs):
            cfg = original_parse(*args, **kwargs)
            cfg.rewards = SimpleNamespace(
                zero_command_position_drift=SimpleNamespace(weight=1.0),
                zero_command_wheel_action=SimpleNamespace(weight=-0.05),
            )
            return cfg

        modules["isaaclab_tasks.utils"].parse_env_cfg = parse_env_cfg
        modules["wandb"] = sdk  # None models an unavailable optional SDK.
        argv = [
            "train.py", "--num_envs", "4", "--device", "cpu", "--steps", "4",
            "--buffer_size", "64", "--min_buffer", "8", "--batch_size", "4",
            "--n_step", "1", "--updates_per_step", "2", "--save_every", "4",
            "--log_every", "1", "--logger", logger, "--wandb_mode", "offline", *extra,
        ]
        original_import = builtins.__import__

        def record_import(name, *args, **kwargs):
            if name in ("wandb", "torch", "isaaclab.app"):
                import_events.append(name)
            return original_import(name, *args, **kwargs)

        with ExitStack() as stack:
            stack.enter_context(patch.dict(sys.modules, modules))
            stack.enter_context(patch.object(train, "REPO_ROOT", fixture))
            stack.enter_context(patch.object(sys, "argv", argv))
            stack.enter_context(redirect_stdout(io.StringIO()))
            if import_events is not None:
                stack.enter_context(patch.object(builtins, "__import__", side_effect=record_import))
            train.main()

    def test_config_defaults_and_cli_wandb_overrides(self):
        runner = train.load_default_runner_cfg()
        self.assertEqual(runner.wandb_project, "tita_flat_flash_sac")
        self.assertEqual(runner.logger, "tensorboard")
        runner.wandb_project = "config-project"
        runner.wandb_entity = "config-team"
        runner.run_name = "config-run"
        runner.wandb_mode = "offline"
        args = train.build_parser(runner).parse_args(["--logger", "wandb", "--wandb_project", "cli-project"])
        self.assertEqual(args.wandb_project, "cli-project")
        self.assertEqual(args.wandb_entity, "config-team")
        self.assertEqual(args.run_name, "config-run")
        self.assertEqual(args.wandb_mode, "offline")

    def test_real_cpu_training_logs_config_losses_and_local_run_metadata(self):
        sdk = FakeWandbSDK()
        events = []
        with tempfile.TemporaryDirectory(prefix="flash_sac_wandb_", dir=REPO / "test") as temporary:
            fixture = Path(temporary)
            self.invoke(fixture, sdk, [
                "--wandb_project", "tita-test-project", "--wandb_entity", "test-team",
                "--run_name", "cpu-test",
            ], import_events=events)
            self.assertLess(events.index("wandb"), events.index("torch"))
            self.assertLess(events.index("wandb"), events.index("isaaclab.app"))
            call, run = sdk.calls[0], sdk.runs[0]
            self.assertEqual(call["project"], "tita-test-project")
            self.assertEqual(call["entity"], "test-team")
            self.assertEqual(call["name"], "cpu-test")
            self.assertEqual(call["mode"], "offline")
            self.assertIsNone(call["resume"])
            self.assertTrue(Path(call["dir"]).is_relative_to(fixture / "docs/exp"))
            self.assertEqual(call["config"]["agent"]["sample_batch_size"], 4)
            self.assertEqual(call["config"]["reward_weights"], {
                "zero_command_position_drift": 1.0, "zero_command_wheel_action": -0.05,
            })
            self.assertEqual(call["config"]["actor_obs_dim"], 33)
            self.assertEqual(run.definitions, [("step", {}), ("*", {"step_metric": "step"})])
            self.assertEqual([row["step"] for row in run.metrics], [1, 2, 3, 4])
            self.assertEqual(run.metrics[-1]["updates"], 6)
            for row in run.metrics[1:]:
                self.assertIn("actor/loss", row)  # Last critic-only update must not discard this.
                self.assertIn("critic/loss", row)
                self.assertIn("env/mock_metric", row)
            local = next(fixture.glob("docs/exp/*/*_wandb.json"))
            self.assertEqual(json.loads(local.read_text())["id"], run.id)
            self.assertEqual(run.summary["evidence_status"], "PASS")
            self.assertEqual(len(run.summary["actor_sha256"]), 64)
            self.assertEqual(run.finish_codes, [0])
        self.assertTrue(all(app.closed for app in FakeApp.instances))
        self.assertTrue(all(env.closed for env in FakeNativeEnv.instances))

    def test_checkpoint_resume_can_continue_a_wandb_run_on_vector_step_axis(self):
        sdk = FakeWandbSDK()
        with tempfile.TemporaryDirectory(prefix="flash_sac_wandb_resume_", dir=REPO / "test") as temporary:
            fixture = Path(temporary)
            self.invoke(fixture, sdk, ["--wandb_mode", "online"])
            checkpoint = next(fixture.glob("lab/ddt_lab/logs/flash_sac/*/model_4"))
            self.invoke(fixture, sdk, [
                "--resume", str(checkpoint), "--steps", "6",
                "--wandb_run_id", sdk.runs[0].id, "--wandb_mode", "online",
            ])
            self.assertEqual(sdk.calls[1]["id"], sdk.runs[0].id)
            self.assertEqual(sdk.calls[1]["resume"], "allow")
            self.assertEqual(sdk.calls[1]["mode"], "online")
            self.assertEqual(sdk.calls[1]["config"]["resume"], str(checkpoint))
            self.assertEqual([row["step"] for row in sdk.runs[1].metrics], [5, 6])
            self.assertEqual(sdk.runs[1].summary["vector_steps"], 6)
            self.assertEqual(sdk.runs[1].finish_codes, [0])

    def test_logging_failure_finishes_failed_run_and_closes_simulation(self):
        sdk = FakeWandbSDK(fail_log=True)
        with tempfile.TemporaryDirectory(prefix="flash_sac_wandb_failure_", dir=REPO / "test") as temporary:
            with self.assertRaisesRegex(RuntimeError, "injected W&B log failure"):
                self.invoke(Path(temporary), sdk)
            self.assertEqual(sdk.runs[0].summary["evidence_status"], "FAIL")
            self.assertEqual(sdk.runs[0].finish_codes, [1])
        self.assertTrue(all(app.closed for app in FakeApp.instances))
        self.assertTrue(all(env.closed for env in FakeNativeEnv.instances))

    def test_sdk_finish_failure_still_closes_simulation(self):
        sdk = FakeWandbSDK(fail_finish=True)
        with tempfile.TemporaryDirectory(prefix="flash_sac_wandb_finish_failure_", dir=REPO / "test") as temporary:
            with self.assertRaisesRegex(RuntimeError, "injected W&B finish failure"):
                self.invoke(Path(temporary), sdk)
            self.assertEqual(sdk.runs[0].finish_codes, [0])
        self.assertTrue(all(app.closed for app in FakeApp.instances))
        self.assertTrue(all(env.closed for env in FakeNativeEnv.instances))

    def test_console_does_not_import_or_require_wandb(self):
        events = []
        with tempfile.TemporaryDirectory(prefix="flash_sac_no_wandb_", dir=REPO / "test") as temporary:
            self.invoke(Path(temporary), None, logger="console", import_events=events)
        self.assertNotIn("wandb", events)

    def test_missing_wandb_reports_dependency_before_simulator_launch(self):
        with tempfile.TemporaryDirectory(prefix="flash_sac_missing_wandb_", dir=REPO / "test") as temporary:
            with self.assertRaisesRegex(RuntimeError, "python -m pip install wandb"):
                self.invoke(Path(temporary), None)
            summary = next(Path(temporary).glob("docs/exp/*/*_summary.md")).read_text()
            self.assertIn("Evidence Status: BLOCKED", summary)
        self.assertEqual(FakeApp.instances, [])
        self.assertEqual(FakeNativeEnv.instances, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
