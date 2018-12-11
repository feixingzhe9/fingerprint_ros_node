#!/usr/bin/env python
# coding=utf-8

import rospy
import json
from mrobot_srvs.srv import JString

rospy.wait_for_service('/fingerprint/set_templates')

fp_info_1 = 'Z8yu+79HIL3qrhttc+zhP6jAITR0LEsWQcVwxtiHihSDq0ofX82eiWruW+3zrKE/qIBhdDRsC3YhAC3AGsPXEzNwAErnGOPEx474JTagKNgoBLbYXTQKCcCI6hMTYWaDq+0LZfNMIwRsj61gIHNtvOzjVQqXgX9kFl2+R3Zh7zu4kHFkJHwbRhGVIJaI19pE0/saD08XcC16/kv947yxL7iQcWQkfBtGEZUglojX2kTT+xoPTxdwLXr+S/3jvLEvuJBxZCR8G0YRlSCWiNfaRNP7Gg9PF3Atev5L/eO8sS+4kHFkJHwbRhGVIJaI19pE0/saD08XcC16/kv947yx4w=='
print len(fp_info_1)
fp_info = [fp_info_1, 'mpijjkiejlpp']
set_fp_info = rospy.ServiceProxy('/fingerprint/set_templates', JString)

fp = JString()
fp.request = json.dumps(fp_info)
return_vaule = set_fp_info(fp.request)
print return_vaule