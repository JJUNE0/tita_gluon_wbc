#!/usr/bin/env python3
import argparse


def names(model, obj_type, count, mujoco):
    out = []
    for i in range(count):
        out.append(mujoco.mj_id2name(model, obj_type, i) or f"<unnamed:{i}>")
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("xml")
    args = parser.parse_args()

    import mujoco

    model = mujoco.MjModel.from_xml_path(args.xml)
    print(f"nq: {model.nq}")
    print(f"nv: {model.nv}")
    print(f"nu: {model.nu}")
    print("body names:")
    for i, name in enumerate(names(model, mujoco.mjtObj.mjOBJ_BODY, model.nbody, mujoco)):
        print(f"  {i}: {name}")
    print("joint names:")
    for i, name in enumerate(names(model, mujoco.mjtObj.mjOBJ_JOINT, model.njnt, mujoco)):
        print(
            f"  {i}: {name} qpos={model.jnt_qposadr[i]} qvel={model.jnt_dofadr[i]} "
            f"type={model.jnt_type[i]}"
        )
    print("actuator names:")
    for i, name in enumerate(names(model, mujoco.mjtObj.mjOBJ_ACTUATOR, model.nu, mujoco)):
        print(
            f"  {i}: {name} "
            f"trntype={int(model.actuator_trntype[i])} "
            f"dyntype={int(model.actuator_dyntype[i])} "
            f"gaintype={int(model.actuator_gaintype[i])} "
            f"biastype={int(model.actuator_biastype[i])} "
            f"ctrllimited={bool(model.actuator_ctrllimited[i])} "
            f"ctrlrange={model.actuator_ctrlrange[i].tolist()} "
            f"forcelimited={bool(model.actuator_forcelimited[i])} "
            f"forcerange={model.actuator_forcerange[i].tolist()} "
            f"gear={model.actuator_gear[i].tolist()}"
        )
    print("sensor names:")
    for i, name in enumerate(names(model, mujoco.mjtObj.mjOBJ_SENSOR, model.nsensor, mujoco)):
        print(
            f"  {i}: {name} type={model.sensor_type[i]} dim={model.sensor_dim[i]} "
            f"adr={model.sensor_adr[i]}"
        )


if __name__ == "__main__":
    main()
