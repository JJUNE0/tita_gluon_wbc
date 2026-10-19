#!/usr/bin/env python3
"""Bounded, subscribe-only metadata probe for TITA sensor topics."""

import json
import math
import struct
import sys
import time
from collections import defaultdict

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import CameraInfo, Image, Imu, JointState, PointCloud2, Range
from tf2_msgs.msg import TFMessage


TOPICS = {
    "left_image": ("/tita4252763/perception/camera/image/left", Image),
    "right_image": ("/tita4252763/perception/camera/image/right", Image),
    "left_info": ("/tita4252763/perception/camera/info/left", CameraInfo),
    "right_info": ("/tita4252763/perception/camera/info/right", CameraInfo),
    "face_tof": ("/tita4252763/perception/devices/face_point", PointCloud2),
    "neck_tof": ("/tita4252763/perception/devices/neck_point", PointCloud2),
    "ultrawave": ("/tita4252763/perception/devices/ultrawave", Range),
    "body_imu": ("/tita4252763/imu_sensor_broadcaster/imu", Imu),
    "chassis_odom": ("/tita4252763/chassis/odometry", Odometry),
    "tower_odom": ("/tita4252763/tower/odometry", Odometry),
    "mapping_odom": ("/tower/mapping/odometry", Odometry),
    "joint_states": ("/tita4252763/joint_states", JointState),
    "camera_cloud": ("/tita4252763/perception/camera/point_cloud", PointCloud2),
    "tower_cloud": ("/tita4252763/tower/map_point", PointCloud2),
    "colored_cloud": ("/tower/mapping/cloud_colored", PointCloud2),
}


def stamp_seconds(message):
    stamp = getattr(getattr(message, "header", None), "stamp", None)
    return None if stamp is None else stamp.sec + stamp.nanosec * 1e-9


def finite(values):
    return all(math.isfinite(float(value)) for value in values)


def point_cloud_summary(message):
    fields = {field.name: field for field in message.fields}
    result = {
        "width": message.width,
        "height": message.height,
        "point_count": message.width * message.height,
        "fields": sorted(fields),
        "point_step": message.point_step,
        "row_step": message.row_step,
        "is_dense": message.is_dense,
        "data_bytes": len(message.data),
    }
    if not all(axis in fields for axis in ("x", "y", "z")) or message.point_step <= 0:
        return result
    endian = ">" if message.is_bigendian else "<"
    datatype_formats = {7: "f", 8: "d"}
    axes = []
    for axis in ("x", "y", "z"):
        field = fields[axis]
        fmt = datatype_formats.get(field.datatype)
        if fmt is None:
            return result
        axes.append((field.offset, endian + fmt))
    count = message.width * message.height
    stride = max(1, count // 5000)
    valid = invalid = 0
    distances = []
    data = bytes(message.data)
    for index in range(0, count, stride):
        row, col = divmod(index, message.width)
        base = row * message.row_step + col * message.point_step
        try:
            xyz = [struct.unpack_from(fmt, data, base + offset)[0] for offset, fmt in axes]
        except (struct.error, IndexError):
            invalid += 1
            continue
        if finite(xyz):
            valid += 1
            distances.append(math.sqrt(sum(value * value for value in xyz)))
        else:
            invalid += 1
    sampled = valid + invalid
    result.update(
        {
            "sampled_points": sampled,
            "valid_ratio": valid / sampled if sampled else None,
            "nan_inf_ratio": invalid / sampled if sampled else None,
            "distance_min_m": min(distances) if distances else None,
            "distance_max_m": max(distances) if distances else None,
        }
    )
    return result


def message_summary(message):
    result = {
        "frame_id": getattr(getattr(message, "header", None), "frame_id", ""),
        "stamp": stamp_seconds(message),
    }
    if isinstance(message, Image):
        result.update(
            width=message.width,
            height=message.height,
            encoding=message.encoding,
            step=message.step,
            data_bytes=len(message.data),
        )
    elif isinstance(message, CameraInfo):
        result.update(
            width=message.width,
            height=message.height,
            distortion_model=message.distortion_model,
            d=list(message.d),
            k=list(message.k),
            r=list(message.r),
            p=list(message.p),
            calibration_nonzero=any(value != 0.0 for value in (*message.d, *message.k, *message.r, *message.p)),
        )
    elif isinstance(message, PointCloud2):
        result.update(point_cloud_summary(message))
    elif isinstance(message, Range):
        result.update(
            radiation_type=message.radiation_type,
            field_of_view=message.field_of_view,
            min_range=message.min_range,
            max_range=message.max_range,
            range=message.range,
            finite=math.isfinite(message.range),
        )
    elif isinstance(message, Imu):
        result.update(
            orientation=[message.orientation.x, message.orientation.y, message.orientation.z, message.orientation.w],
            angular_velocity=[message.angular_velocity.x, message.angular_velocity.y, message.angular_velocity.z],
            linear_acceleration=[message.linear_acceleration.x, message.linear_acceleration.y, message.linear_acceleration.z],
            orientation_covariance=list(message.orientation_covariance),
            angular_velocity_covariance=list(message.angular_velocity_covariance),
            linear_acceleration_covariance=list(message.linear_acceleration_covariance),
        )
    elif isinstance(message, Odometry):
        result.update(
            child_frame_id=message.child_frame_id,
            position=[message.pose.pose.position.x, message.pose.pose.position.y, message.pose.pose.position.z],
            orientation=[
                message.pose.pose.orientation.x,
                message.pose.pose.orientation.y,
                message.pose.pose.orientation.z,
                message.pose.pose.orientation.w,
            ],
            linear_velocity=[message.twist.twist.linear.x, message.twist.twist.linear.y, message.twist.twist.linear.z],
            angular_velocity=[message.twist.twist.angular.x, message.twist.twist.angular.y, message.twist.twist.angular.z],
            pose_covariance=list(message.pose.covariance),
            twist_covariance=list(message.twist.covariance),
        )
    elif isinstance(message, JointState):
        result.update(
            names=list(message.name),
            name_count=len(message.name),
            position_count=len(message.position),
            velocity_count=len(message.velocity),
            effort_count=len(message.effort),
            finite=finite((*message.position, *message.velocity, *message.effort)),
        )
    return result


class ReadOnlyProbe(Node):
    def __init__(self):
        super().__init__("tita_sensor_readonly_probe")
        self.arrivals = defaultdict(list)
        self.stamps = defaultdict(list)
        self.latest = {}
        self.transforms = {}
        self.sensor_subscriptions = []
        for key, (topic, message_type) in TOPICS.items():
            self.sensor_subscriptions.append(
                self.create_subscription(
                    message_type,
                    topic,
                    lambda message, name=key: self.on_message(name, message),
                    qos_profile_sensor_data,
                )
            )
        for topic, static in (("/tf", False), ("/tf_static", True)):
            self.sensor_subscriptions.append(
                self.create_subscription(
                    TFMessage,
                    topic,
                    lambda message, is_static=static: self.on_tf(message, is_static),
                    qos_profile_sensor_data,
                )
            )

    def on_message(self, key, message):
        now = time.monotonic()
        self.arrivals[key].append(now)
        stamp = stamp_seconds(message)
        if stamp is not None:
            self.stamps[key].append(stamp)
        if key not in self.latest or isinstance(message, (PointCloud2, CameraInfo)):
            self.latest[key] = message_summary(message)

    def on_tf(self, message, static):
        for transform in message.transforms:
            translation = transform.transform.translation
            rotation = transform.transform.rotation
            self.transforms[f"{transform.header.frame_id}->{transform.child_frame_id}"] = {
                "translation": [translation.x, translation.y, translation.z],
                "rotation_xyzw": [rotation.x, rotation.y, rotation.z, rotation.w],
                "static": static,
                "stamp": stamp_seconds(transform),
            }

    def report(self):
        topics = {}
        for key, (topic, message_type) in TOPICS.items():
            arrivals = self.arrivals[key]
            duration = arrivals[-1] - arrivals[0] if len(arrivals) > 1 else 0.0
            topics[key] = {
                "topic": topic,
                "type": message_type.__module__.replace(".", "/") + "/" + message_type.__name__,
                "count": len(arrivals),
                "rate_hz": (len(arrivals) - 1) / duration if duration > 0.0 else None,
                "latest": self.latest.get(key),
            }
        left = self.stamps["left_image"]
        right = self.stamps["right_image"]
        skews = [min(abs(stamp - other) for other in right) for stamp in left] if left and right else []
        return {
            "duration_s": 12,
            "topics": topics,
            "stereo_sync": {
                "left_samples": len(left),
                "right_samples": len(right),
                "pair_samples": len(skews),
                "mean_abs_skew_s": sum(skews) / len(skews) if skews else None,
                "median_abs_skew_s": sorted(skews)[len(skews) // 2] if skews else None,
                "max_abs_skew_s": max(skews) if skews else None,
            },
            "transforms": self.transforms,
        }


def main():
    rclpy.init()
    node = ReadOnlyProbe()
    deadline = time.monotonic() + 12.0
    try:
        while time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=0.1)
        print(json.dumps(node.report(), indent=2, sort_keys=True))
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    sys.exit(main())
