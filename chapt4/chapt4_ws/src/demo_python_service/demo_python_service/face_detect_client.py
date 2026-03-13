import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory # 获取功能包share的绝对路径
from cv_bridge import CvBridge
import time

class FaceDetectClientNode(Node):
    def __init__(self):
        super().__init__("face_detect_node")
        self.bridge = CvBridge()
        self.image_path = get_package_share_directory('demo_python_service') + '/resource/ros2_test_image2.png'
        self.client = self.create_client(FaceDetector, 'face_detect')
        self.get_logger().info(f"face_clent_node加载")
        self.image = cv2.imread(self.image_path)
    
    def send_request(self):
        # 判断服务端是否在线
        while self.client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info("服务器不在线")
        # 构造request
        request = FaceDetector.Request()
        request.image = self.bridge.cv2_to_imgmsg(self.image)
        # 发送请求并等待处理
        future = self.client.call_async(request=request)
        # while not future.done():
        #     time.sleep(1.0)  # 1. 休眠当前线程，等待服务端处理，但会导致无法接受服务端返回
        #     # 2. 如果在循环中不编写代码，理论上可以接受服务端的返回，但是会占用大量cpu资源
        rclpy.spin_until_future_complete(self, future)  # 使用专门的多线程处理
        response = future.result()
        self.get_logger().info(f"接受到响应，共有{response.number}人，耗时({response.use_time}.")
        self.show_response(response)

        
    def show_response(self, response):
        for i in range(response.number):
            top = response.top[i]
            right = response.right[i]
            bottom = response.bottom[i]
            left = response.left[i]

            cv2.rectangle(self.image, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.imshow("test_image_detect", self.image)
        cv2.waitKey()




def main():
    rclpy.init()
    node = FaceDetectClientNode()
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()