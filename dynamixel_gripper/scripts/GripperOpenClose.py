#!/usr/bin/env python
# license removed for brevity

# This scripts runs a node that opens and closes the dyanmixel gripper via ros topics

import rospy
from std_msgs.msg import Float64, Int32
from dynamixel_msgs.msg import MotorStateList
from dynamixel_gripper.msg  import grip_state

# define open & close angles
global LGrip_open_angle
global LGrip_close_angle
global RGrip_open_angle
global RGrip_close_angle

RGrip_open_angle = 3.15
RGrip_close_angle = 2.75
LGrip_close_angle = 2.50
LGrip_open_angle = 2.10

# initialise parameters
# 0 - open, 1 - close
global gripper_state
global feedback_load
global feedback_load_max
global present_angle
gripper_state= 0
feedback_load = 0
feedback_load_max = 0.2
present_angle = [0,0]

def callback(data):
    global gripper_state
    gripper_state = int(data.data)
    rospy.loginfo("Grip mode switched to %s" % gripper_state)

def callback_load(data):
    global feedback_load
    global present_angle
    feedback_load = 0
    data = data.motor_states
    if(len(data)==1): rospy.loginfo("Only 1 motor detected!")
    for i in range(len(data)):
        feedback_load = max(data[i].load,feedback_load)
        present_angle[i] = data[i].position


def open_and_close():
    rospy.init_node('GripperOpenClose', anonymous=True)
    pub = rospy.Publisher('/LGrip_controller/command', Float64, queue_size=10)
    pub2 = rospy.Publisher('/RGrip_controller/command', Float64, queue_size=10)
    pub_state = rospy.Publisher('/gripper/state', grip_state, queue_size=10)
    rospy.Subscriber('/gripper/command', Int32, callback)
    rospy.Subscriber('/motor_states/pan_tilt_port', MotorStateList, callback_load)
    rate = rospy.Rate(1) # 10hz

    msg = grip_state()

    while not rospy.is_shutdown():

        rospy.loginfo("Gripper Load: %f, Gripper State %d" % (feedback_load,gripper_state))

        # open state
        if(gripper_state == 0):
            #set left & right grippers to open up
            pub.publish(LGrip_open_angle)
            pub2.publish(RGrip_open_angle)

        # closed state
        elif(gripper_state == 1):

            # check that a good grip is made and does not go over limit to prevent overload
            if(abs(feedback_load)<=feedback_load_max):
                pub.publish(LGrip_close_angle)
                pub2.publish(RGrip_close_angle)

            # else freeze movement of motors
            else:
                pub.publish(present_angle[0])
                pub2.publish(present_angle[1])
                rospy.loginfo("Load detected, motor angles locked.")

        else:
            rospy.loginfo("Invalid gripper state (%s) given. Please provide 0 or 1 only." % gripper_state)

        msg.gripper_state = gripper_state
        msg.left_pos = present_angle[0]
        msg.right_pos = present_angle[1]
        msg.avg_load = feedback_load
        pub_state.publish(msg)

        rate.sleep()


if __name__ == '__main__':
    try:
        print "GripperOpenClose node has started."
        open_and_close()
    except rospy.ROSInterruptException:
        pass
