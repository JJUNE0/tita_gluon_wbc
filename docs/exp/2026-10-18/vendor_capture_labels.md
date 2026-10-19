# Vendor capture: custom labels rejected before recording

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domain: `DESKTOP_DRY_RUN` only; no SBC access, deployment, capture or control commands.
- Evidence Status: diagnosis PASS from unchanged original script and operator console; shell/mock regression4 PASS. Hardware capture with the corrected script NOT_TESTED.
- Vendor checkpoint SHA256: N/A. Comparison FlashSAC checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c` (no policy execution).
- Branch: `agent/codex/dev_tita_gluon`; no commit/push.

The operator ran `60 stand_high`, `120 stand_high_push`, and `60 stand_mid`. Each returned immediately without a RUN_ID or CAPTURE_READY. The original script accepts only literal labels `stand` or `commands`, then silently exits2 for any other label **before defining/creating the output directory or starting rosbag/candump**. The listed destination contains only the older11:10 and17:14 runs. These three commands therefore did not create new recordings; movement already performed cannot be recovered through this recorder. The assistant previously called the second argument a log label without clearly stating its restriction.

## Local correction

`test/sim2real/capture_vendor_baseline.sh` now accepts1–64 ASCII letters/digits/underscore/hyphen, beginning with a letter or digit. This accepts the operator's high/mid/push labels and preserves existing labels. Invalid labels and invalid duration ranges now print explicit errors saying capture did not start. No capture, process cleanup, ROS/CAN, service-check, MCU or output logic changed.

The original script snapshot/hash is preserved as `vendor_capture_labels/capture_vendor_baseline.before.txt`, SHA256 `8b83dc2597f6b651324038e47319b19c9f49ef421eaff9d6ca6c188a8f9b9665`.

## Manual correction in the already-open robot terminal

No extra SSH or SCP is needed. The following narrow command replaces only the original label regular expression and saves the prior file as `capture_vendor_baseline.sh.before_labels.bak`:

```bash
cd ~/tita_ws
sed -i.before_labels.bak \
  's/\^(stand|commands)\$/^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$/' \
  capture_vendor_baseline.sh

bash ./capture_vendor_baseline.sh 60 stand_high
```

The manual sed correction is tested on the exact original script, including backup-byte equality and acceptance of all three requested labels. It applies the label fix only; it does not install the PC version's additional invalid-argument error messages. It was not remotely executed by the agent. The PC script's full correction can be copied later at the operator's discretion.

A recording must print `RUN_ID` and `CAPTURE_READY`; the specified duration then elapses before it returns. Existing output remains `~/tita_ws/docs/exp/2026-10-18/vendor_baseline_capture/`, using `vendor_<label>_<time>_*` names. The label does not command posture, height, probing or motion; operator conditions must still be documented separately. Keep the existing SSH session open while distinguishing the separate logout/idle incident.

## Executed checks and scope

- `bash -n`: PASS.
- New `test/sim2real/test_vendor_capture_labels.py`:4 PASS, covering requested/legacy/bounded labels, malformed labels, invalid duration ranges and the exact manual sed patch/backup.
- Test source setup is stubbed and capture is intercepted before mkdir/systemctl, so no ROS environment, service, recorder or CAN socket is touched.
- [Test output](vendor_capture_labels/tests.log). Required agent-check and final scoped diff/source hashes are preserved in `vendor_capture_labels/`.
- Only the existing recorder argument validation, new regression test and this report/evidence were changed. Production controller/policy/config and all hardware state remain unchanged.
