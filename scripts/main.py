#!/usr/bin/env python
# coding=utf-8

import ctypes
import os
import sys
from termios import tcflush, TCIFLUSH
import time
import rospy
import thread
import json
from fp_db import fp_db
from std_msgs.msg import String
from mrobot_msgs.msg import fingerprint
from mrobot_srvs.srv import JString

dev_so = ctypes.CDLL('libFpDriverUSB_WL.so')

img_3 = (ctypes.c_char * (40537))()
tz_3 = (ctypes.c_char * (512 + 1))()


def pub_fp_info(fp_info):
    report_fp_info_pub.publish(json.dumps(fp_info))


def set_fp_templates(req):
    fp_info = json.loads(req.request)
    print fp_info
#    JStringResponse.success = True
#    JStringResponse.response = "OK"
    for fp in fp_info:
        print 'get fingprint feature: len  ', len(fp), 'data: ', fp
        fp_db.insert_fp_feature(name = 'hello', rfid = '0001', password = '0001', worker_id = 1, door_id = 0, id_type = 1, feature = fp)

    return [True, "OK"]


def fp_init(cnt):
    global dev_so

    for i in range(0, cnt):
        if dev_so.FPIDeviceInit() < 0:
            time.sleep(1)
            rospy.logerr("ERROR: FPIDeviceInit error, restart to init . . . ")
        else:
            rospy.loginfo("FPIDeviceInit OK")
            return 0

    rospy.logerr("ERROR: FPIDeviceInit error ! !")
    return -1

def fingerprint_proc():
    global dev_so
    global img_3
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

    if fp_init(3) < 0:
        return
    print "start to get dev version ... "
    ret = dev_so.FPIGetVersion(dev_info, err_msgs)
    print ' ---------- end of getting dev version --------------'

    if ret < 0:
        rospy.logerr("ERROR: FPIGetVersion error ! !")
    else:
        rospy.loginfo("dev_info:  %s", dev_info.value)

    fp_info_cmd = None
    while 1:
        print "请按下指纹 ..."
        data_len.value = 0
        while dev_so.FPICheckFinger(err_msgs) == 1:
            pass

        for i in range(0, len(sTZ)):
            sTZ[i] = 'A'
        ret = dev_so.FPIFeature(5000, sTZ, ctypes.byref(data_len))

        if ret < 0:
            rospy.logerr("ERROR: FPIGetFeature error ! !")
            rospy.logerr("\n采集指纹特征失败--[%d] [%s]", ret, err_msgs.value)
        else:
            rospy.loginfo("FPIGetFeature excute OK")
        features = fp_db.get_feature_rfid_name()
        match_ok_flag = False
        rospy.loginfo("开始匹配 ...")
        for i in range(0, len(features)):
            sMB.value = features[i][3]
            if dev_so.FPIFpMatch(sMB, sTZ, 3) == 0:
                rospy.loginfo("指纹比对成功")
                name = features[i][1]
                rfid = features[i][2]
                match_ok_flag = True
                fp_info_cmd = {'template': sTZ.value, 'matched_template': sMB.value}
                pub_fp_info(fp_info_cmd)
                break

        if match_ok_flag is not True:
            rospy.logerr("ERROR: FPIFpMatch error ! !")
            rospy.logerr("指纹比对失败--[%d] [%s]", ret, err_msgs.value)
            rospy.logerr("指纹比对失败")

            fp_info_cmd = {'template': sTZ.value, 'matched_template': ''}
            pub_fp_info(fp_info_cmd)

        print "请抬起指纹 ..."
        while dev_so.FPICheckFinger(err_msgs) == 0:
            pass
        time.sleep(0.2)

def main():
    rospy.spin()

if __name__ == '__main__':

    try:
        rospy.init_node('fingerprint', anonymous=True)
        report_fp_info_pub = rospy.Publisher('/fingerprint/template_matched_info', String, queue_size=10)
        rospy.Service('/fingerprint/set_templates', JString, set_fp_templates)
        thread.start_new_thread(fingerprint_proc, ())
        time.sleep(0.5)
        main()
    except Exception:
        rospy.logerr(sys.exc_info())
        rospy.loginfo("lost connect")
        exit(1)

