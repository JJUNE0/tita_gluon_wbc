# Student 0809 PlotJuggler startup

- Execution Domain: VALIDATION_SIM
- Evidence Status: PASS (MuJoCo, plot publishers, PlotJuggler GUI and ROS2 plugin); NOT_TESTED (GUI streaming selection and plotted curves)
- Policy checkpoint: 2026-08-09_15-40-20/model_999.pt
- Policy Checkpoint SHA256: e37f6c1936d699627afb109ef141138958a3f0890028c1c8e1c107056b4a8b10 (previously verified)
- Actor ONNX SHA256: caa4645a6b3ff5e608b5705c520f5947eb954b4d8ec38acdc51cec50350e1f27
- Adaptation ONNX SHA256: 490c21e247bdf15858873211b5d8d833918cda4fb819cb9fb9fcf6a49976718d
- Branch: agent/codex/dev_tita_gluon

Restarted task-owned native MuJoCo launch with plot:=true, same Student YAML and local-only domain 96. Existing operator keyboard process preserved. Viewer resets to idle. Launch opened PlotJuggler and loaded ROS2 streaming plugin. MuJoCo log confirms scalar plot publication at 50 Hz under /cosim_ros2_jazzy/plot; ros2 topic echo received measured_vx=6.272858676936721e-09. Actual frequency not measured.

Existing plotjuggler_tita_validation.xml is explicitly a placeholder topic list, not a saved GUI layout. Operator should select ROS2 streaming, subscribe to plot topics, then drag series onto a plot. Recommended pairs: cmd_vx/measured_vx, cmd_yaw_rate/measured_yaw_rate, target/joint positions and target/measured wheel velocities; also pitch/roll.

Artifacts: student_0809_plot_viewer.log, student_0809_plot_sample.log, student_0809_plot_agent_check.log.

Only experiment records added; no code/config changes. No hardware commands. agent-check.sh PASS; final record diff reviewed and pre-existing modifications preserved. No new policy behavior evaluation performed.
