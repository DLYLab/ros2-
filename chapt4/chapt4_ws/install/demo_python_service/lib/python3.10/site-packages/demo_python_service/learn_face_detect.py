import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory # 获取功能包share的绝对路径

def main():
    # 获取图片的真实路径
    test_image = get_package_share_directory('demo_python_service') + '/resource/ros2_test_image.png'
    print(f"图片路径：{test_image}")
    # 使用opencv来读取并显示图片
    image = cv2.imread(test_image)
    face_location = face_recognition.face_locations(image, 1, model='hog') # 返回值是人脸的框的坐标的列表
    # 绘制人脸框
    for top,right,bottom,left in face_location:
        cv2.rectangle(image,(left, top), (right, bottom), (255, 0, 0), 4)

    cv2.imshow("test_image", image)
    cv2.waitKey()