#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

sub_joy_ = None
pub_twist_ = None


def joy_stick_handler(msg):
    twist_msg = Twist()
    twist_msg.linear.x = msg.axes[5] - msg.axes[4]
    twist_msg.angular.z = msg.axes[0]
    pub_twist_.publish(twist_msg)


if __name__ == '__main__':
    try:
        rospy.init_node("brops_controller")
        sub_joy_ = rospy.Subscriber("joystick/joy", Joy, joy_stick_handler, queue_size=1)
        pub_twist_ = rospy.Publisher("brops_node/twist", Twist, queue_size=1)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
