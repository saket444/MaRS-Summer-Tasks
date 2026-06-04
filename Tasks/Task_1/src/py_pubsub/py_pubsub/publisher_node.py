import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class PyPublisher(Node):
    def __init__(self):
        super().__init__('py_publisher')
        self.publisher_ = self.create_publisher(String, 'py_topic', 10)
        self.count = 0
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello from Python: {self.count}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = PyPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
