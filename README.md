# Summer Tasks

## Task 1 — ROS 2 Publisher & Subscriber

A ROS 2 workspace with publisher/subscriber nodes in both C++ and Python.

---


### Build

```bash
source /opt/ros/humble/setup.bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

---

### Run

**C++**
```bash
ros2 run cpp_pubsub cpp_publisher
ros2 run cpp_pubsub cpp_subscriber
```

**Python**
```bash
ros2 run py_pubsub py_publisher
ros2 run py_pubsub py_subscriber
```

---

### CLI Commands

```bash
ros2 topic list
ros2 topic echo /cpp_topic
ros2 topic hz /cpp_topic
ros2 node list
ros2 node info /cpp_publisher
rqt_graph
```

---

### What I Learned
- ROS 2 workspace and package structure
- Publisher/subscriber pattern using topics
- Difference between `ament_cmake` (C++) and `ament_python` (Python) packages
- ROS 2 CLI tools for inspecting nodes and topics
