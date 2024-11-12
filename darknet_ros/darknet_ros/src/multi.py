#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from subprocess import Popen, PIPE

class ObjectDetectionNode:
    def __init__(self):
        rospy.init_node('object_detection_node', anonymous=True)

        # Initialize subscribers for camera images
        self.subscribers = [
            rospy.Subscriber('/tb3_0/camera/rgb/image_raw', Image, self.image_callback, callback_args='/tb3_0'),
            rospy.Subscriber('/tb3_1/camera/rgb/image_raw', Image, self.image_callback, callback_args='/tb3_1'),
            rospy.Subscriber('/tb3_2/camera/rgb/image_raw', Image, self.image_callback, callback_args='/tb3_2')
        ]

        # Initialize CvBridge for image conversion
        self.bridge = CvBridge()

    def image_callback(self, image_data, robot_id):
        # Convert ROS Image message to OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(image_data, desired_encoding='bgr8')

        # Save the image to a temporary file (you can modify this based on your actual implementation)
        temp_image_path = f'/tmp/{robot_id}_image.jpg'
        cv2.imwrite(temp_image_path, cv_image)

        # Run darknet_ros node on the temporary image
        self.run_darknet_ros(temp_image_path)

        rospy.loginfo(f'Detection performed for {robot_id}')

    def run_darknet_ros(self, image_path):
        # Launch darknet_ros node with the image
        darknet_process = Popen(['roslaunch', 'darknet_ros', 'darknet_ros.launch', 'image_path:=' + image_path],
                                stdout=PIPE, stderr=PIPE)
        darknet_process.wait()
        rospy.loginfo(f'darknet_ros process completed with return code {darknet_process.returncode}')

    def run(self):
        # Spin the node to keep it alive
        rospy.spin()

if __name__ == '__main__':
    object_detection_node = ObjectDetectionNode()
    object_detection_node.run()
