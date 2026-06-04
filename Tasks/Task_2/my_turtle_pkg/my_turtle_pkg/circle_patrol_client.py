import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from turtle_interfaces.action import ExecuteCircle


class CirclePatrolClient(Node):
    def __init__(self):
        super().__init__('circle_patrol_client')
        self._client = ActionClient(self, ExecuteCircle, 'execute_circle')

    def send_goal(self, radius):
        self.get_logger().info("Waiting for action server...")
        self._client.wait_for_server()

        goal = ExecuteCircle.Goal()
        goal.radius = radius

        self.get_logger().info(f"Sending goal: radius = {radius}")
        future = self._client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )
        future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        fb = feedback_msg.feedback
        print(f"[FEEDBACK] Distance traveled: {fb.distance_traveled:.2f} m | "
              f"Status: {fb.current_status}")

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error("Goal rejected!")
            return
        self.get_logger().info("Goal accepted! Turtle is moving...")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result().result
        if result.success:
            self.get_logger().info(f"[SUCCESS] {result.final_report}")
        else:
            self.get_logger().error(f"[FAILED/ABORTED] {result.final_report}")
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    client = CirclePatrolClient()
    client.send_goal(3.0)   # ← Set your desired radius here
    rclpy.spin(client)


if __name__ == '__main__':
    main()
