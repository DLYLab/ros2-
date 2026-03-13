import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory # 获取功能包share的绝对路径
from cv_bridge import CvBridge
import time

class FaceDetectNode(Node):
    def __init__(self, ):
        super().__init__("face_detect_node")
        self.service_ = self.create_service(FaceDetector, 'face_detect', self.detect_face_callback)
        self.bridge = CvBridge()
        self.model = 'hog'
        self.image_upper = 1
        self.image_path = get_package_share_directory('demo_python_service') + '/resource/ros2_test_image.png'
        self.get_logger().info(f"face_node加载")
    
    def detect_face_callback(self, request, response):
        if request.image.data:
            cv_image = self.bridge.imgmsg_to_cv2(request.image) # ros2图像格式转为opencv格式
        else:
            cv_image = cv2.imread(self.image_path)  # 默认cv图像
            self.get_logger().info(f"加载默认图像")
        
        start_time = time.time()
        self.get_logger().info(f"图像加载完成，开始检测")

        # 人脸检测
        face_location = face_recognition.face_locations(cv_image, self.image_upper, model=self.model) # 返回值是人脸的框的坐标的列表
        
        end_time = time.time()
        response.use_time = end_time - start_time
        response.number = len(face_location)

        for top,right,bottom,left in face_location:
            response.top.append(top)
            response.right.append(right)
            response.bottom.append(bottom)
            response.left.append(left)
        
        return response

def main():
    rclpy.init()
    node = FaceDetectNode()
    rclpy.spin(node)
    rclpy.shutdown()
