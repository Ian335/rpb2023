from std_msgs.msg import String
import rospy
import subprocess
import time

def talker():
# TODO: publish 10 string data, topic name is chatter
    pub = rospy.Publisher('chatter', String, queue_size=20)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    time.sleep(5)
    i=0
    j=10
    
    while(1):
        hello_str = "hello world %s" % rospy.get_time()
        pub.publish(hello_str)   
        
        i +=1
    
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
