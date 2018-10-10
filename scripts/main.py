#!/usr/bin/env python
# coding=utf-8

import ctypes
import os
import sys
import rospy
import time


test_flag = False

def main():
    rate = rospy.Rate(10)
    time.sleep(1)
    #dev_so = ctypes.CDLL('libFPDev_WL.so')
    dev_so = ctypes.CDLL('libFPDevUSB_WL.so')
    #alg_so = ctypes.CDLL('libFPAlg_WL.so')
    #alg_so = ctypes.CDLL('libFPDevUSB_WL.so')

    dev_info = (ctypes.c_char * (64 + 1))()
    lib_info = (ctypes.c_char * (64 + 1))()
    err_msgs = (ctypes.c_char * (64 + 1))()
    sMB = (ctypes.c_char * (512 + 1))()
    sTZ = (ctypes.c_char * (512 + 1))()

    data_len = ctypes.c_int(1)

    term = -1
    port = 0
    ret = -1 

    os.system("clear")

    print "start to get dev version ... "
    #ret = dev_so.FPIGetVersion(term, port, 3000, dev_info, err_msgs)
    ret = dev_so.FPIGetVersion(dev_info, err_msgs)
    print ' ---------- end of getting dev version --------------'

    if ret < 0:
        rospy.logerr("ERROR: FPIGetVersion error ! !")
    else:
        rospy.loginfo("dev_info:  %s", dev_info.value)

    print "start to get lib info ... "
    ret = dev_so.FPIGetInfo(lib_info, err_msgs)
    print ' ---------- end of getting lib info --------------'

    if ret < 0:
        rospy.logerr("ERROR: FPIGetInfo error ! !")
    else:
        rospy.loginfo("dev_info:  %s", lib_info.value)


    #sys.system('clear')
    raw_input("press enter to continue . . .")
    while 1:
        os.system("clear")
        print   "\t\t==================================================\n"  \
                "\t\ttest function      \n" \
                "\t\t===================================================\n" \
                "\t\t\t1-- get template (press 3 times) and save template \n"\
                "\t\t\t2--pick fingerprint feature and match \n" \
                "\t\t\t4--finger check(check the finger is pressed or not)\n" \
                "\t\t\t0--quit        \n"

        state = input("\n input option (integer) \n  ")
        if state is not None:
            if isinstance(state, int):
                pass
            else:
                rospy.logerr("please input integer value !");
                continue
        else:
            rospy.logerr("input value is None !");


        if state == 1:

            print "start to pick fingerprint model ..."
            data_len.value = 0
            #ret = dev_so.FPIGetTemplate(term, port, 15000, sMB, ctypes.byref(data_len), err_msgs)
            ret = dev_so.FPIGetTemplate(15000, sMB, ctypes.byref(data_len), err_msgs)
            print ' ---------- pick fingerprint model --------------'
            if ret < 0:
                rospy.logerr("ERROR: FPIGetTemplate error ! !")
                rospy.logerr("\n采集指纹模板失败--[%d] [%s]", ret, err_msgs.value)
            elif ret == 0:
                rospy.loginfo("FPIGetTemplate excute OK")
                rospy.loginfo("\n采集指纹模板成功\n")
                rospy.loginfo("data len:  %d", data_len.value)
                rospy.loginfo("template info:  %s", sMB.value)

            print 'ret value: ', ret

        elif state == 2:

            print "start to pick fingerprint feature ..."
            data_len.value = 0
            #ret = dev_so.FPIGetFeature(term, port, 5000, sTZ, ctypes.byref(data_len), err_msgs)
            ret = dev_so.FPIGetFeature(5000, sTZ, ctypes.byref(data_len), err_msgs)
            print ' ---------- pick fingerprint feature --------------'

            if ret < 0:
                rospy.logerr("ERROR: FPIGetFeature error ! !")
                rospy.logerr("\n采集指纹特征失败--[%d] [%s]", ret, err_msgs.value)
            else:
                rospy.loginfo("FPIGetFeature excute OK")
                rospy.loginfo("data len:  %d", data_len.value)
                rospy.loginfo("feature info: %s", sTZ.value)

            print "\n           start to match ..."
            ret = dev_so.FPIFpMatch(sMB, sTZ, 3)
            print ' ---------- end match --------------\n'
            
            if ret < 0:
                rospy.logerr("ERROR: FPIFpMatch error ! !")
                rospy.logerr("\n指纹比对失败--[%d] [%s]", ret, err_msgs.value)
            else:
                rospy.loginfo("FPIFpMatch excute OK")
                rospy.loginfo("\n指纹比对成功")

        elif state == 3:
            pass

        elif state == 4:

            print "\n start to check finger . . "
            ret = dev_so.FPICheckFinger(err_msgs)
            print ' ---------- end check finger --------------\n'
            if ret < 0:
                rospy.logerr("ERROR: FPICheckFinger error ! !")
                rospy.logerr("\nFPICheckFinger--[%d] [%s]", ret, err_msgs.value)
            else:
                rospy.loginfo("FPICheckFinger excute OK")
                if ret == 0:
                    print "finger is pressed "
                if ret == 1:
                    print "finger is not pressed "

        elif state == 0:
            #exit(1)
            return

        time.sleep(2)

    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.init_node('fingerprint', anonymous=True)
        main()
    except Exception:
        rospy.logerr(sys.exc_info())
        rospy.loginfo("lost connect")
        exit(1)

