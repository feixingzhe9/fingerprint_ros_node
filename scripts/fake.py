#!/usr/bin/env python
# coding=utf-8

import rospy
import json
from mrobot_srvs.srv import JString

rospy.wait_for_service('/fingerprint/set_templates')

fp_info = ['asdfgasdfij','mpijjkiejlpp']
set_fp_info = rospy.ServiceProxy('/fingerprint/set_templates', JString)

fp = JString()
#print fp.request.request
fp.request = json.dumps(fp_info)
return_vaule = set_fp_info(fp.request)
print return_vaule