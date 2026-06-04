#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include <chrono>

using namespace std::chrono_literals;

class CppPublisher : public rclcpp::Node {
public:
  CppPublisher() : Node("cpp_publisher"), count_(0) {
    publisher_ = create_publisher<std_msgs::msg::String>("cpp_topic", 10);
    timer_ = create_wall_timer(500ms, [this]() { timer_callback(); });
  }
private:
  void timer_callback() {
    auto msg = std_msgs::msg::String();
    msg.data = "Hello from C++: " + std::to_string(count_++);
    RCLCPP_INFO(get_logger(), "Publishing: '%s'", msg.data.c_str());
    publisher_->publish(msg);
  }
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  size_t count_;
};

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<CppPublisher>());
  rclcpp::shutdown();
  return 0;
}
