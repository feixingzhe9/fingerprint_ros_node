#!/usr/bin/env python
# coding=utf-8

import ctypes
import os
import sys
import time
import rospy
from fp_db import fp_db

test_flag = False

#dev_so = ctypes.CDLL('libFPDev_WL.so')
dev_so = ctypes.CDLL('libFpDriverUSB_WL.so')
#dev_so = ctypes.CDLL('libFPDevUSB_WL.so')
#alg_so = ctypes.CDLL('libFPAlg_WL.so')
#alg_so = ctypes.CDLL('libFPDevUSB_WL.so')

img_1 = (ctypes.c_char * (40537))()
img_2 = (ctypes.c_char * (40537))()
img_3 = (ctypes.c_char * (40537))()
tz_1 = (ctypes.c_char * (512 + 1))()
tz_2 = (ctypes.c_char * (512 + 1))()
tz_3 = (ctypes.c_char * (512 + 1))()

def test_fun():
    pass

def main():
    global dev_so
    global img_1
    global img_2
    global img_3
    global tz_1
    global tz_2
    global tz_3
    rate = rospy.Rate(10)
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
    #ret = dev_so.FPIGetVersion(term, port, 3000, dev_info, err_msgs)
    ret = dev_so.FPIGetVersion(dev_info, err_msgs)
    print ' ---------- end of getting dev version --------------'

    if ret < 0:
        rospy.logerr("ERROR: FPIGetVersion error ! !")
    else:
        rospy.loginfo("dev_info:  %s", dev_info.value)

    raw_input("\n \n 按下回车键以继续 . . .")
    #name = raw_input("\n \n press enter to continue . . .")

    while 1:
        os.system("clear")
        print "按下指纹以继续 . ."
        while dev_so.FPICheckFinger() is not 0: # 0: finger pressed, 1: finger not pressed
            #time.sleep(0.1)
            pass

        os.system("clear")
        print   "\t\t==================================================\n"  \
                "\t\t 测试模板      \n" \
                "\t\t===================================================\n" \
                "\t\t\t2-- 指纹识别 \n" \
                "\t\t\t4-- 检查手指是否按下\n" \
                "\t\t\t5-- 录入指纹 \n"\
                "\t\t\t0-- 退出        \n"

##                "\t\t\t1-- get template (press 3 times) and save template \n"\

        state = input("\n 请输入功能编号并回车(例如，输入5并回车,开始录入指纹): ")
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
            #ret = dev_so.FPIGetTemplate(15000, sMB, ctypes.byref(data_len), err_msgs)
            ret = dev_so.FPITemplate(15000, sMB, ctypes.byref(data_len))
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

            print "请按下指纹 ..."
            data_len.value = 0
            #ret = dev_so.FPIGetFeature(term, port, 5000, sTZ, ctypes.byref(data_len), err_msgs)
            #ret = dev_so.FPIGetFeature(5000, sTZ, ctypes.byref(data_len), err_msgs)
            ret = dev_so.FPIFeature(5000, sTZ, ctypes.byref(data_len))

            if ret < 0:
                rospy.logerr("ERROR: FPIGetFeature error ! !")
                rospy.logerr("\n采集指纹特征失败--[%d] [%s]", ret, err_msgs.value)
            else:
                rospy.loginfo("FPIGetFeature excute OK")
                #rospy.loginfo("data len:  %d", data_len.value)
                #rospy.loginfo("feature info: %s", sTZ.value)

            features = fp_db.get_feature_rfid_name()
            match_ok_flag = False
            rospy.loginfo("开始匹配 ...")
            for i in range(0, len(features)):
                sMB.value = features[i][2]
                if dev_so.FPIFpMatch(sMB, sTZ, 3) == 0:
                    rospy.loginfo("指纹比对成功")
                    print "该指纹匹配到的姓名: ", features[i][0]
                    print "该指纹匹配到的rfid: ", features[i][1]
                    match_ok_flag = True
                    break
            
            if match_ok_flag is not True:
                rospy.logerr("ERROR: FPIFpMatch error ! !")
                rospy.logerr("指纹比对失败--[%d] [%s]", ret, err_msgs.value)
                rospy.logerr("指纹比对失败")

        elif state == 4:

            print "\n 开始检测手指 . . "
            ret = dev_so.FPICheckFinger(err_msgs)
            if ret < 0:
                rospy.logerr("ERROR: FPICheckFinger error ! !")
                rospy.logerr("\nFPICheckFinger--[%d] [%s]", ret, err_msgs.value)
            else:
                rospy.loginfo("FPICheckFinger excute OK")
                if ret == 0:
                    print "手指已按下 "
                if ret == 1:
                    print "手指未按下 "


        elif state == 5:

            print "\n 1  start\n"
            ret = dev_so.FPIGetFeatureAndImage(5000, tz_1, ctypes.byref(data_len), img_1, ctypes.byref(img_data_len), err_msgs)
            if ret < 0:
                rospy.logerr("ERROR: FPIGetFeatureAndImage error ! !")
                rospy.logerr("\nFPIGetFeatureAndImage--[%d] [%s]", ret, err_msgs.value)
            else:
                rospy.loginfo("FPIGetFeatureAndImage excute OK")
                print 'img_1: ', tz_1.value
            print " 1 end \n"

            print "\n 2 start\n"
            ret = dev_so.FPIGetFeatureAndImage(5000, tz_2, ctypes.byref(data_len), img_2, ctypes.byref(img_data_len), err_msgs)
            if ret < 0:
                rospy.logerr("ERROR: FPIGetFeatureAndImage error ! !")
                rospy.logerr("\nFPIGetFeatureAndImage--[%d] [%s]", ret, err_msgs.value)
            else:
                rospy.loginfo("FPIGetFeatureAndImage excute OK")
                print 'img_2: ', tz_2.value
            print " 2 end \n"

            print "\n 3 start\n"
            ret = dev_so.FPIGetFeatureAndImage(5000, tz_3, ctypes.byref(data_len), img_3, ctypes.byref(img_data_len), err_msgs)
            if ret < 0:
                rospy.logerr("ERROR: FPIGetFeatureAndImage error ! !")
                rospy.logerr("\nFPIGetFeatureAndImage--[%d] [%s]", ret, err_msgs.value)
            else:
                rospy.loginfo("FPIGetFeatureAndImage excute OK")
                print 'img_3: ', tz_3.value
            print " 3 end \n"
            data_len.value = 0
            #ret = dev_so.FPIGetTemplateByTZ(img_1, img_2, img_3, sMB, ctypes.byref(data_len), err_msgs)
            ret = dev_so.FPIGetTemplateByTZ(tz_1, tz_2, tz_3, sMB, ctypes.byref(data_len))
            if ret < 0:
                rospy.logerr("ERROR: FPIGetTemplateByImg error ! !")
                rospy.logerr("\nFPIGetTemplateByImg--[%d] [%s]", ret, err_msgs.value)
            elif ret == 0:
                rospy.loginfo("FPIGetTemplateByImg excute OK")
                print 'get sMB :', sMB.value

            name = raw_input("\n请输入姓名:")
            rfid = raw_input("\n请输入RFID号:")
            worker_id = rfid
            rfid = str(rfid)
            password = rfid

            fp_db.insert_fp_feature(name, rfid, password, worker_id, door_id = 0, id_type = 1, feature = sMB.value)
            print "\n姓名 : ", name
            print "\nRFID : ", rfid
            print "\n录入成功\n"

        elif state == 0:
            #exit(1)
            return
        else:
            print "\n请输入正确的选项 ! \n"
            pass

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

