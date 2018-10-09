#!/usr/bin/env python
# coding=utf-8

import ctypes
import os
import sys
import rospy
import time

def main():
    rate = rospy.Rate(10)
    time.sleep(1)
    dev_so = ctypes.CDLL('libFPDev_WL.so')
    alg_so = ctypes.CDLL('libFPAlg_WL.so')
    dev_info = (ctypes.c_char * (64 + 1))()
    err_msgs = (ctypes.c_char * (64 + 1))()
    sMB = (ctypes.c_char * (512 + 1))()
    sTZ = (ctypes.c_char * (512 + 1))()

    data_len = ctypes.c_int(1)

    term = -1
    port = 0
    ret = -1 
    print "get dev version ... "
    ret = dev_so.FPIGetVersion(term, port, 3000, dev_info, err_msgs)
    if ret < 0:
        rospy.logerr("ERROR: FPIGetVersion error ! !")
    else:
        rospy.loginfo("dev_info:  %s", dev_info.value)
    while 1:
        #sys.system('clear') 
        print "start to pick fingerprint model ..."
        ret = dev_so.FPIGetTemplate(term, port, 10000, sMB, ctypes.byref(data_len), err_msgs)
        print ' ---------- pick fingerprint model --------------'
        if ret < 0:
            rospy.logerr("ERROR: FPIGetTemplate error ! !")
            rospy.logerr("\n采集指纹模板失败--[%d] [%s]", ret, err_msgs.value)
        else:
            rospy.loginfo("FPIGetTemplate excute OK")
            rospy.loginfo("\n采集指纹模板成功\n")
            rospy.loginfo("data len:  %d", data_len.value)
            #for i in range(0, len(sMB)):
            rospy.loginfo("template info:  %s", sMB.value)



        print "start to pick fingerprint feature ..."
        ret = dev_so.FPIGetFeature(term, port, 15000, sTZ, ctypes.byref(data_len), err_msgs)
        print ' ---------- pick fingerprint feature --------------'

        if ret < 0:
            rospy.logerr("ERROR: FPIGetFeature error ! !")
            rospy.logerr("\n采集指纹特征失败--[%d] [%s]", ret, err_msgs.value)
        else:
            rospy.loginfo("FPIGetFeature excute OK")
            rospy.loginfo("data len:  %d", data_len.value)
            rospy.loginfo("feature info: %s", sTZ.value)

            
            
        print "start to match ..."
        ret = alg_so.FPIFpMatch(sMB, sTZ, 3)
        print ' ---------- end match --------------'
        
        if ret < 0:
            rospy.logerr("ERROR: FPIGetFeature error ! !")
            rospy.logerr("\n指纹比对失败--[%d] [%s]", ret, err_msgs.value)
            rospy.loginfo("FPIGetFeature excute OK")
        else:
            rospy.loginfo("FPIFpMatch excute OK")
            rospy.loginfo("\n指纹比对成功")

        time.sleep(1)

    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.init_node('fingerprint', anonymous=True)
        main()
    except Exception:
        rospy.logerr(sys.exc_info())
        rospy.loginfo("lost connect")
        exit(1)

