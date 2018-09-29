#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float64
from dynamixel_msgs.msg import MotorStateList
from dynamixel_gripper.msg import load_state

global load_left
global load_right
global load

load_left = 0
load_right = 0
load = 0

def callback(data):
    global load
    global load_left
    global load_right
    data = data.motor_states
    for motor in data:
        if(motor.id==1):
            load_left=motor.load
        if(motor.id==2):
            load_right=motor.load

    load = (load_left+load_right)/2

    rospy.loginfo("\nLeft load value: %f\nRight load value: %f\nAverage load value: %f\n-" % (load_left,load_right,load))

def getLoadValue():
    rospy.init_node('GripperLoadValue', anonymous=True)
    pub = rospy.Publisher('/gripper/load', load_state, queue_size=10)
    rospy.Subscriber('/motor_states/pan_tilt_port', MotorStateList, callback)
    rate = rospy.Rate(1) # 10hz

    loadState = load_state()

    while not rospy.is_shutdown():
        global load
        global load_left
        global load_right

        loadState.load_left = load_left
        loadState.load_right = load_right
        loadState.avg_load = load

        # rospy.loginfo(hello_str)
        pub.publish(loadState)
        rate.sleep()


if __name__ == '__main__':
    try:
        getLoadValue()
    except rospy.ROSInterruptException:
        pass
