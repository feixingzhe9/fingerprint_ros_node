#!/usr/bin/env python
# coding=utf-8

import os
import sys
#from termios import tcflush, TCIFLUSH
import time
import rospy
#from std_msgs.msg import String
from mrobot_srvs.srv import JString
#from mrobot_msgs.msg import fingerprint
from fp_proc import fp_proc

def main():
    rospy.spin()

if __name__ == '__main__':

    try:
        time.sleep(0.5)
        fp_proc.ros_start()
        main()
    except Exception:
        rospy.logerr(sys.exc_info())
        rospy.loginfo("lost connect")
        exit(1)

