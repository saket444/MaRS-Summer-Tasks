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
---
---

# Task 2: Circular Patrol & Action Management

A ROS2 project that drives a turtlesim turtle in a precise circle using a custom Action Server and Client. The turtle streams live distance feedback, completes a full 360° loop, and aborts if it approaches a wall.

---
## Build

```bash
cd ~/ros2_ws
colcon build --packages-select turtle_interfaces my_turtle_pkg
source install/setup.bash
```

## Run

Open 3 terminals and run `source ~/ros2_ws/install/setup.bash` in each.

```bash
# Terminal 1
ros2 run turtlesim turtlesim_node

# Terminal 2
ros2 run my_turtle_pkg circle_patrol_server

# Terminal 3
ros2 run my_turtle_pkg circle_patrol_client
```

## Change the Radius

In `circle_patrol_client.py`, edit:
```bash
client.send_goal(2.0)  # set your desired radius here
```
Then rebuild: `colcon build --packages-select my_turtle_pkg`

> Keep radius between `1.0` – `2.0` to avoid wall collisions.

## Expected Output

| Scenario | Result |
|---|---|
| Full 360° loop completed | ✅ `Circle complete! Total distance: X m` |
| Turtle approaches wall | ❌ `Mission Aborted: Boundary Collision Imminent!` |

---
