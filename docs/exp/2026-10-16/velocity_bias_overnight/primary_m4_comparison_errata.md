Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: FAIL for three initial M4 harness jobs.

The warmup invoked apply() before the M4 observer initialized wheel signs. These fail before control testing and are not controller evidence. Kept original failures; comparison02 only applies the M4 residual after common warmup, exactly preserving the baseline acquisition. Baseline/velocity PI jobs in comparison01 are unaffected.
