import cv2
import rospy
import numpy as np

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        self.bridge = CvBridge()

    def callback(self, data):
        try:
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')

            msg = Header()
            msg = data.header
            msg.frame_id = '0'  # default: STOP
           
            color_dict = dict()
            color_dict.clear()
           
            x = image.shape[0]
            y = image.shape[1]
            start = 0.1
            end = 0.9

            max = 0
            res = (0,0,0)
			
            for i in range(round(x*start),round(x*end)):
                for j in range(round(y*start),round(y*end)):
                   
                    
                    num = 30
                    b = image[i][j][0]//num*num
                    g = image[i][j][1]//num*num
                    r = image[i][j][2]//num*num
               
                    
                    if (b,g,r) in color_dict:
                        color_dict[(b,g,r)]+=1
                        if(color_dict[(b,g,r)]>max):
                            max = color_dict[(b,g,r)]
                            res = (b,g,r)
                    else:
                        color_dict[(b,g,r)]=1
           
            
           
            color_names={
                (255,255,255):'White',
                (0,0,0):'Black',
                (0,0,255):'Red',
                (0,255,0):'Green',
                (255,0,0):'Blue',
                (0,255,255):'Yellow',
                (255,0,255):'Pink',
                (255,128,0):'SkyBlue'
            }
           

            min_dist = 100000000
            min_color = 'Black'
           
            for key in color_names:
                dist = (res[0]-key[0])**2+(res[1]-key[1])**2+(res[2]-key[2])**2
                if dist < min_dist:
                    min_dist = dist
                    min_color = color_names[key]
            if min_color=='Red':
                msg.frame_id = '-1'
            elif min_color=='Blue' or min_color=='SkyBlue':
                msg.frame_id = '+1'
           
            self.color_pub.publish(msg)
            cv2.imshow('Image', image)
            cv2.waitKey(1)

        except CvBridgeError as e:
            print(e)


    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    detector = DetermineColor()
    rospy.init_node('CompressedImages1', anonymous=False)
    rospy.spin()

