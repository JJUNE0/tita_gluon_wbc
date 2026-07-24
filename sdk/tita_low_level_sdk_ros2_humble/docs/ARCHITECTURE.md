# Architecture

## Ownership boundary

The stack is a replacement, not an additional policy node attached to vendor balance control.

```text
before takeover: vendor stack owns motion/CAN
after takeover:  one direct HardwareBridge and one Stage1Controller own motion/CAN
```

The supervisor verifies service shutdown, named process disappearance, old controller-manager
absence, and SocketCAN release before it invokes the unchanged official `start.bash`.

## Production command path

```text
Stage1Controller
-> position / velocity / effort / kp / kd command interfaces
-> patched upstream HardwareBridge::write()
-> effort_ff + kp*(q_target-q) + kd*(dq_target-dq)
-> per-joint torque clamp
-> upstream TITA motor API
-> CAN
-> motion board
```

There is no Python motor writer and no custom raw-SocketCAN motor writer.

## Direct sensor path

After vendor shutdown, the controller consumes only HardwareBridge state:

- eight joint positions, velocities, and efforts
- IMU quaternion, angular velocity, and linear acceleration
- motor feedback freshness and status availability
- hardware read/write result and consecutive failure count
- controller/writer sequence correlation

The separate TITA motor-status vector may be unavailable in Direct mode. An all-zero unavailable
vector is diagnostic only; finite, fresh eight-joint feedback and the motor timeout watchdog
remain mandatory. A partial status vector fails closed.

## TransformUp envelopes

`TRANSFORM_UP` uses the exact pinned official fold target, including L3/R3 `-2.7 rad`, inside a
transition-only envelope. `STANDING_SETTLE` and every RL state use the conservative operational
envelope with L3/R3 lower bound `-2.670354 rad`. The exception cannot leak into normal operation.

## RL path

The same controller retains all command interfaces:

```text
standing hold
-> real observation/history
-> ONNX inference at 50 Hz
-> native action adapter
-> bounded 20 ms stand-to-policy blend
-> 500 Hz final command/write path
```

The observation joint fields are interleaved. This policy's action head is already native
left-then-right and must not receive the observation reindex.

## SAFE_HOLD

SAFE_HOLD rejects new policy output, ramps wheel velocity to zero, holds a validated leg pose with
bounded gains, keeps the hardware writer and logger alive, and requests an operator-supported
full-power recovery. It is not an emergency stop.

