#!/usr/bin/env python
#type:ignore
import sys
import cv2
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String
from sensor_msgs.msg import Image
import rospy
import numpy as np
import time
import message_filters
import os 

class image_convert:
    def __init__(self):
        self.image_depth=message_filters.Subscriber("/camera/depth/image_raw",Image)
        self.image_rgb=message_filters.Subscriber("/camera/rgb/image_raw",Image)
        self.bridge=CvBridge()
        self.time_sychronization=message_filters.ApproximateTimeSynchronizer([self.image_depth,self.image_rgb],queue_size=10,slop=0.01,allow_headerless=True)

    def callback(self,image_depth,image_rgb):
        cv_image_rgb=self.bridge.imgmsg_to_cv2(image_rgb)
        cv_image_rgb=cv2.cvtColor(cv_image_rgb, cv2.COLOR_BGR2RGB)
        cv_image_depth=self.bridge.imgmsg_to_cv2(image_depth,"16UC1")
        max_meter=3
        cv_image_depth=np.array(cv_image_depth/max_meter,dtype=np.uint8)
        cv2.imwrite("/home/kentuen/fallen_configurations_data/data_raw/%f_depth.png"%time.time(),cv_image_depth)
        cv2.imwrite("/home/kentuen/fallen_configurations_data/data_raw/%f_rgb.png"%time.time(),cv_image_rgb)
        cv2.waitKey(3)
    
    def image_capture(self):
        print ('image capture starts...')
        self.time_sychronization.registerCallback(self.callback)



def main(args):
    direcorty="/home/kentuen/fallen_configurations_data/data_raw/"
    if not os.path.exists(direcorty):
        os.mkdir(direcorty)
    rospy.init_node("cv_image_convertor",anonymous=True)
    convertor=image_convert()
    convertor.image_capture()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print ("Shut Down...")

if __name__=="__main__":
    main(sys.argv)