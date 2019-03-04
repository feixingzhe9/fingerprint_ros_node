#!/usr/bin/env python
# coding=utf-8

import ctypes
import os
import sys
from termios import tcflush, TCIFLUSH
import time
import rospy
import thread
from fp_db import fp_db
from std_msgs.msg import String
from mrobot_msgs.msg import fingerprint

dev_so = ctypes.CDLL('libFpDriverUSB_WL.so')

img_1 = (ctypes.c_char * (40537))()
img_2 = (ctypes.c_char * (40537))()
img_3 = (ctypes.c_char * (40537))()
tz_1 = (ctypes.c_char * (512 + 1))()
tz_2 = (ctypes.c_char * (512 + 1))()
tz_3 = (ctypes.c_char * (512 + 1))()

fp_id_pub = None

fp_template_for_test = None

def pub_fp_id(result, rfid):
    global fp_id_pub
    msg = fingerprint()
    msg.result = result
    msg.rfid = rfid
    fp_id_pub.publish(msg)


def fingerprint_proc():
    global dev_so
    global img_1
    global img_2
    global img_3
    global tz_1
    global tz_2
    global tz_3
    time.sleep(1)

    fp_db.create_table()
    print fp_db.cursor
    print fp_db.connect

    dev_info = (ctypes.c_char * (64 + 1))()
    lib_info = (ctypes.c_char * (64 + 1))()
    err_msgs = (ctypes.c_char * (64 + 1))()
    sMB = (ctypes.c_char * (512 + 1))()
    sTZ = (ctypes.c_char * (512 + 1))()
    tmp_buf = (ctypes.c_char * (512 + 1))()

    data_len = ctypes.c_int(1)
    img_data_len = ctypes.c_int(1)

    term = -1
    port = 0
    ret = -1 

    os.system("clear")

    ret = dev_so.FPIDeviceInit()
    if ret < 0:
        rospy.logerr("ERROR: FPIDeviceInit error ! !")
    else:
        rospy.loginfo("FPIDeviceInit OK")

    print "start to get dev version ... "
    ret = dev_so.FPIGetVersion(dev_info, err_msgs)
    print ' ---------- end of getting dev version --------------'

    if ret < 0:
        rospy.logerr("ERROR: FPIGetVersion error ! !")
    else:
        rospy.loginfo("dev_info:  %s", dev_info.value)


    while 1:
        print "请按下指纹 ..."
        data_len.value = 0
        while dev_so.FPICheckFinger(err_msgs) == 1:
            pass

        pub_fp_id(1, "0000")
        for i in range(0, len(sTZ)):
            sTZ[i] = 'A'
        ret = dev_so.FPIFeature(5000, sTZ, ctypes.byref(data_len))

        if ret < 0:
            rospy.logerr("ERROR: FPIGetFeature error ! !")
            rospy.logerr("\n采集指纹特征失败--[%d] [%s]", ret, err_msgs.value)
        else:
            rospy.loginfo("FPIGetFeature excute OK")

        match_ok_flag = False
        rospy.loginfo("开始匹配 ...")
        if dev_so.FPIFpMatch(fp_template_for_test, sTZ, 3) == 0:
            rospy.loginfo("指纹比对成功")
            #pub_fp_id(0, rfid)
            match_ok_flag = True

        if match_ok_flag is not True:
            rospy.logerr("ERROR: FPIFpMatch error ! !")
            rospy.logerr("指纹比对失败--[%d] [%s]", ret, err_msgs.value)
            rospy.logerr("指纹比对失败")
            #pub_fp_id(-1, "0000")

        #time.sleep(2)

def main():
    rospy.spin()

if __name__ == '__main__':

    #global fp_template_for_test
    try:
        rospy.init_node('fingerprint', anonymous=True)
        fp_id_pub = rospy.Publisher('fp_id', fingerprint, queue_size=10)
        #rospy.get_param("/fingerprint_template_for_test")
        fp_template_for_test = rospy.get_param("/fingerprint_template_for_test")
        print "fp_template len: ",  len(fp_template_for_test)
        print "fp_template: ",  fp_template_for_test
        thread.start_new_thread(fingerprint_proc, ())
        time.sleep(0.5)
        main()
    except Exception:
        rospy.logerr(sys.exc_info())
        rospy.loginfo("lost connect")
        exit(1)

