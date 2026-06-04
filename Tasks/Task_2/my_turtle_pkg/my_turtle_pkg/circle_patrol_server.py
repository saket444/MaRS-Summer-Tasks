import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.action.server import ServerGoalHandle
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtle_interfaces.action import ExecuteCircle
import math
import time

class CirclePatrolServer(Node):
    def __init__(self):
        super().__init__('circle_patrol_server')

        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.pose = None
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

        self._action_server = ActionServer(
            self,
            ExecuteCircle,
            'execute_circle',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        self.get_logger().info("Circle Patrol Action Server is ready.")

    def pose_callback(self, msg):
        self.pose = msg

    def goal_callback(self, goal_request):
        self.get_logger().info(f"Received goal: radius = {goal_request.radius}")
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info("Cancel request received.")
        return CancelResponse.ACCEPT

    def is_near_wall(self, x, y, margin=0.5):
        return x < margin or x > 11.0 - margin or y < margin or y > 11.0 - margin

    async def execute_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info("Executing circular patrol...")

        radius = goal_handle.request.radius
        v = 1.5
        w = v / radius

        # Wait until we have a pose
        while self.pose is None:
            self.get_logger().info("Waiting for turtle pose...")
            time.sleep(0.1)

        x_start = self.pose.x
        y_start = self.pose.y
        self.get_logger().info(f"Start position: ({x_start:.2f}, {y_start:.2f})")

        feedback_msg = ExecuteCircle.Feedback()
        result = ExecuteCircle.Result()

        distance_traveled = 0.0
        prev_x = self.pose.x
        prev_y = self.pose.y

        loop_started = False

        twist = Twist()
        twist.linear.x = v
        twist.angular.z = w

        while rclpy.ok():
            # Publish movement command
            self.cmd_pub.publish(twist)

            # Let ROS2 process callbacks (updates pose)
            rclpy.spin_once(self, timeout_sec=0.1)

            # Check for cancellation
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.stop_turtle()
                result.success = False
                result.final_report = "Goal cancelled by client."
                return result

            current_x = self.pose.x
            current_y = self.pose.y

            # Wall Crash Detection
            if self.is_near_wall(current_x, current_y):
                self.stop_turtle()
                goal_handle.abort()
                result.success = False
                result.final_report = "Mission Aborted: Boundary Collision Imminent!"
                self.get_logger().error(result.final_report)
                return result

            # Arc-length feedback
            delta = math.sqrt((current_x - prev_x)**2 + (current_y - prev_y)**2)
            distance_traveled += delta
            prev_x = current_x
            prev_y = current_y

            feedback_msg.distance_traveled = distance_traveled
            feedback_msg.current_status = f"Moving in circle, distance: {distance_traveled:.2f} m"
            goal_handle.publish_feedback(feedback_msg)

            # Check if turtle left the start zone
            dist_from_start = math.sqrt((current_x - x_start)**2 + (current_y - y_start)**2)
            if not loop_started and dist_from_start > 0.5:
                loop_started = True

            # Check if turtle returned to start
            if loop_started and dist_from_start < 0.2:
                self.stop_turtle()
                goal_handle.succeed()
                result.success = True
                result.final_report = f"Circle complete! Total distance: {distance_traveled:.2f} m"
                self.get_logger().info(result.final_report)
                return result

        self.stop_turtle()
        return result

    def stop_turtle(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.cmd_pub.publish(twist)
        self.get_logger().info("Turtle stopped.")


def main(args=None):
    rclpy.init(args=args)
    server = CirclePatrolServer()
    rclpy.spin(server)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
