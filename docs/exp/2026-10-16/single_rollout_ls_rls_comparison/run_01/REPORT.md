# Single-rollout LS/RLS — saved-data comparison

Execution Domain: **DESKTOP_DRY_RUN**

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: PASS/FAIL model gates below; same data are reused, no new physical validation.

Observed Metrics / Behavior / Log Summary: same training transitions and same subsequent sensor/command windows for every paired comparison.

| Split / domain / amplitude | Window / RLS setting | N | Plain LS prediction | Raw RLS prediction | Candidate RLS prediction | Same-cost Batch prediction | Full PASS, all methods |
|---|---|---:|---:|---:|---:|---:|---|
|development/nominal/0.01|local20|9|4|0|0|0|0/0/0/0|
|development/nominal/0.01|local10|9|4|0|0|0|0/0/0/0|
|development/nominal/0.01|cumulative_weak|9|2|0|0|0|0/0/0/0|
|development/nominal/0.01|cumulative_original|9|2|0|0|0|0/0/0/0|
|development/nominal/0.01|cumulative_P100|9|2|0|0|0|0/0/0/0|
|development/nominal/0.02|local20|9|4|0|0|0|0/0/0/0|
|development/nominal/0.02|local10|9|4|0|0|0|0/0/0/0|
|development/nominal/0.02|cumulative_weak|9|2|0|0|0|0/0/0/0|
|development/nominal/0.02|cumulative_original|9|2|0|0|0|0/0/0/0|
|development/nominal/0.02|cumulative_P100|9|2|0|0|0|0/0/0/0|
|development/friction0.2/0.01|local20|9|6|0|0|0|0/0/0/0|
|development/friction0.2/0.01|local10|9|6|0|0|0|0/0/0/0|
|development/friction0.2/0.01|cumulative_weak|9|0|0|0|0|0/0/0/0|
|development/friction0.2/0.01|cumulative_original|9|0|0|0|0|0/0/0/0|
|development/friction0.2/0.01|cumulative_P100|9|0|0|0|0|0/0/0/0|
|development/friction0.2/0.02|local20|9|6|0|0|0|0/0/0/0|
|development/friction0.2/0.02|local10|9|6|2|1|1|0/0/0/0|
|development/friction0.2/0.02|cumulative_weak|9|0|0|0|0|0/0/0/0|
|development/friction0.2/0.02|cumulative_original|9|0|0|0|0|0/0/0/0|
|development/friction0.2/0.02|cumulative_P100|9|0|0|0|0|0/0/0/0|
|test/nominal/0.01|local20|18|7|0|0|0|0/0/0/0|
|test/nominal/0.01|local10|18|7|0|0|0|0/0/0/0|
|test/nominal/0.01|cumulative_weak|18|4|0|0|0|0/0/0/0|
|test/nominal/0.01|cumulative_original|18|4|0|0|0|0/0/0/0|
|test/nominal/0.01|cumulative_P100|18|4|0|0|0|0/0/0/0|
|test/nominal/0.02|local20|18|6|0|0|0|0/0/0/0|
|test/nominal/0.02|local10|18|7|0|0|0|0/0/0/0|
|test/nominal/0.02|cumulative_weak|18|4|0|0|0|0/0/0/0|
|test/nominal/0.02|cumulative_original|18|4|0|0|0|0/0/0/0|
|test/nominal/0.02|cumulative_P100|18|4|0|0|0|0/0/0/0|
|test/friction0.2/0.01|local20|18|12|0|0|0|0/0/0/0|
|test/friction0.2/0.01|local10|18|12|0|0|0|0/0/0/0|
|test/friction0.2/0.01|cumulative_weak|18|0|0|0|0|0/0/0/0|
|test/friction0.2/0.01|cumulative_original|18|0|0|0|0|0/0/0/0|
|test/friction0.2/0.01|cumulative_P100|18|0|0|0|0|0/0/0/0|
|test/friction0.2/0.02|local20|18|12|1|2|2|0/0/0/0|
|test/friction0.2/0.02|local10|18|12|3|2|2|0/0/0/0|
|test/friction0.2/0.02|cumulative_weak|18|0|0|0|0|0/0/0/0|
|test/friction0.2/0.02|cumulative_original|18|0|0|0|0|0/0/0/0|
|test/friction0.2/0.02|cumulative_P100|18|0|0|0|0|0/0/0/0|
