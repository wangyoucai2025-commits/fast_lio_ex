#!/usr/bin/env python3
"""Republish the RTK /gps_data message as sensor_msgs/Imu for FAST-LIO.

FAST-LIO reads angular_velocity (rad/s) and linear_acceleration. The bag
message carries those in twist.angular and acc. Acceleration may be in g;
FAST-LIO normalizes it. Angular rate must be rad/s.
"""

import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from rosidl_runtime_py.utilities import get_message
from sensor_msgs.msg import Imu


class GpsToImu(Node):
    def __init__(self):
        super().__init__('gps_to_imu')
        self.declare_parameter('gps_topic', '/gps_data')
        self.declare_parameter('imu_topic', '/gps_imu')
        self.declare_parameter('gps_type', 'common_msgs/msg/GpsInfo')
        self.declare_parameter('angular_in_degrees', False)

        gps_type = self.get_parameter('gps_type').get_parameter_value().string_value
        if not gps_type:
            raise RuntimeError(
                'Set gps_type to the Type column from "ros2 bag info". '
                'This bag uses common_msgs/msg/GpsInfo, not the bag directory name.')

        gps_topic = self.get_parameter('gps_topic').get_parameter_value().string_value
        imu_topic = self.get_parameter('imu_topic').get_parameter_value().string_value
        self._deg = self.get_parameter('angular_in_degrees').get_parameter_value().bool_value
        self._scale = math.pi / 180.0 if self._deg else 1.0
        self._logged = False

        msg_cls = get_message(gps_type)
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=200)
        self._pub = self.create_publisher(Imu, imu_topic, qos)
        self.create_subscription(msg_cls, gps_topic, self._on_gps, qos)
        self.get_logger().info(
            'Converting %s [%s] -> %s (angular %s)' % (
                gps_topic, gps_type, imu_topic,
                'deg/s' if self._deg else 'rad/s'))

    def _on_gps(self, msg):
        out = Imu()
        out.header = msg.header
        ang = msg.twist.angular
        acc = msg.acc
        out.angular_velocity.x = ang.x * self._scale
        out.angular_velocity.y = ang.y * self._scale
        out.angular_velocity.z = ang.z * self._scale
        out.linear_acceleration.x = acc.x
        out.linear_acceleration.y = acc.y
        out.linear_acceleration.z = acc.z
        out.orientation_covariance[0] = -1.0
        self._pub.publish(out)
        if not self._logged:
            self._logged = True
            self.get_logger().info(
                'first sample gyro [%.5f %.5f %.5f] acc [%.4f %.4f %.4f]' % (
                    out.angular_velocity.x, out.angular_velocity.y, out.angular_velocity.z,
                    acc.x, acc.y, acc.z))


def main():
    rclpy.init()
    node = GpsToImu()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
