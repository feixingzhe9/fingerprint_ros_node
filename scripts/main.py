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
    os.system("clear")
    print "start to get dev version ... "
    ret = dev_so.FPIGetVersion(term, port, 3000, dev_info, err_msgs)
    print ' ---------- end of getting dev version --------------'
    if ret < 0:
        rospy.logerr("ERROR: FPIGetVersion error ! !")
    else:
        rospy.loginfo("dev_info:  %s", dev_info.value)

    #sys.system('clear')
    input("press enter to continue . . .")
    while 1:
        os.system("clear")
        print   "\t\t==================================================\n"  \
                "\t\ttest function      \n" \
                "\t\t===================================================\n" \
                "\t\t\t1-- get template (press 3 times) and save template \n"\
                "\t\t\t2--pick fingerprint model\n" \
                "\t\t\t3--pick fingerprint feature  \n" \
                "\t\t\t4--fingerprint match\n" \
                "\t\t\t0--quit        \n"

        state = input("\n input option \n  ")

        if isinstance(state, int):
            pass
        else:
            rospy.logerr("please input integer value !");
            continue


        if state == 1:

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


        elif state == 2:

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

        elif state == 3:
            
            print "\nstart to match ..."
            ret = alg_so.FPIFpMatch(sMB, sTZ, 3)
            print ' ---------- end match --------------\n'
            
            if ret < 0:
                rospy.logerr("ERROR: FPIGetFeature error ! !")
                rospy.logerr("\n指纹比对失败--[%d] [%s]", ret, err_msgs.value)
                rospy.loginfo("FPIGetFeature excute OK")
            else:
                rospy.loginfo("FPIFpMatch excute OK")
                rospy.loginfo("\n指纹比对成功")

        elif state == 0:
            #exit(1)
            return

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

