# fast_lio_ex

根据FAST_LIO：
https://github.com/hku-mars/FAST_LIO/
的ROS2分支改造

1、适配ROS2 Foxy

laserMapping.cpp：

void map_save_callback(std_srvs::srv::Trigger::Request::ConstSharedPtr req, std_srvs::srv::Trigger::Response::SharedPtr res)

改为

void map_save_callback(std_srvs::srv::Trigger::Request::SharedPtr req, std_srvs::srv::Trigger::Response::SharedPtr res)

2、加入对速腾RSM1雷达的支持

3、加入来自惯导的gnss、imu数据的支持

4、启动

ros2 run fast_lio gps_to_imu.py --ros-args -p gps_type:=common_msgs/msg/GpsInfo

ros2 launch fast_lio mapping.launch.py

ros2 bag play <ros bag数据包名>


![RSM1 建图效果](doc/rsm1_map.jpg)

![建图效果 1](doc/img_1.jpg)

![建图效果 2](doc/img_2.jpg)

![建图效果 3](doc/img_3.jpg)

![建图效果 4](doc/img_4.jpg)

![建图效果 5](doc/img_5.jpg)

![建图效果 6](doc/img_6.jpg)

![建图效果 7](doc/img_7.jpg)

![建图效果 8](doc/img_8.jpg)

![建图效果 9](doc/img_9.jpg)

