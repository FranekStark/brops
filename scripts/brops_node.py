#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import CameraInfo
from camera_info_manager import CameraInfoManager
from brops import brops

class brops_node:
    def run(self):
        while not rospy.is_shutdown():
            image_cv = self.brops.read_image()
            if image_cv is not None:
                image_raw_msg = self.bridge.cv2_to_imgmsg(image_cv, encoding="bgr8")
                image_com_msg = self.bridge.cv2_to_compressed_imgmsg(image_cv)
                camera_info_msg = self.camera_info_manager_.getCameraInfo()

                now = rospy.Time.now()


                image_raw_msg.header.stamp = now
                image_raw_msg.header.frame_id = "camera"


                image_com_msg.header.stamp = now
                image_com_msg.header.frame_id = "camera"
                image_com_msg.format = "jpeg"

                camera_info_msg.header.stamp = now

         

                self.pub_img_raw_.publish(image_raw_msg)
                self.pub_img_com_.publish(image_com_msg)
                self.pub_cam_inf_.publish(camera_info_msg)



            


    def steering_callback(self, msg):
        self.brops.send_command(100 * msg.linear.x, 100 * msg.angular.z)

    def __init__(self):
        rospy.init_node("brops_node")
        self.brops = brops('10.42.42.217')
        self.pub_cam_inf_ = rospy.Publisher('~camera_info', CameraInfo, queue_size=5)
        self.pub_img_raw_ = rospy.Publisher('~image_raw', Image, queue_size=5)
        self.pub_img_com_ = rospy.Publisher('~image_compressed', CompressedImage, queue_size=5)
        self.camera_info_manager_ = CameraInfoManager('cam', 'package://brops/calibrations/cam.yaml', 'cam')
        self.camera_info_manager_.loadCameraInfo()
        self.sub_twist_ = rospy.Subscriber('~twist', Twist, self.steering_callback)
        self.bridge = CvBridge()
       
      
    
    
        
        



if __name__ == '__main__':
    try:
        node = brops_node()
        node.run()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass