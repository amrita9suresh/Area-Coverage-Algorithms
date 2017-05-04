#!/usr/bin/python
# -*- coding:utf8 -*-

import rospy, os, sys, curses, time, cv2, tf
import roslib; 
import actionlib
import std_msgs
import numpy as np
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Pose, PoseStamped, PoseWithCovariance, PoseWithCovarianceStamped, Transform
from sensor_msgs.msg import LaserScan, Imu
from move_base_msgs.msg import *


side = 5
sweep_width = 1

def spiral_coverage() :
	
	global side, sweep_width
	l = side
	
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	client.wait_for_server()
	rospy.loginfo('got server')
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = "odom"
	goal.target_pose.header.stamp = rospy.Time.now()
	goal.target_pose.pose.position.x = 0.0
	goal.target_pose.pose.position.y = 0.0
	goal.target_pose.pose.position.z = 0.0
	goal.target_pose.pose.orientation.x = 0.0
	goal.target_pose.pose.orientation.y = 0.0
	goal.target_pose.pose.orientation.z = 0.0
	goal.target_pose.pose.orientation.w = 0.0

	m = 0
	first = 0

	while l >= 0 :
		
		goal.target_pose.pose.position.x = m
		if first == 0 :		
			goal.target_pose.pose.position.y = 0
			first = 1
		else :
			goal.target_pose.pose.position.y = m - 1.5 * sweep_width
		goal.target_pose.pose.orientation.w = 1.57
		client.send_goal(goal)
		rospy.loginfo('sent goal')
		rospy.loginfo(goal)
		client.wait_for_result()
	
		goal.target_pose.pose.orientation.w = 0
		goal.target_pose.pose.position.x = m
		goal.target_pose.pose.position.y = l
		client.send_goal(goal)
		rospy.loginfo('sent goal')
		rospy.loginfo(goal)
		client.wait_for_result()

		goal.target_pose.pose.position.x = l
		goal.target_pose.pose.position.y = l
		client.send_goal(goal)
		rospy.loginfo('sent goal')
		rospy.loginfo(goal)
		client.wait_for_result()

		goal.target_pose.pose.position.x = l
		goal.target_pose.pose.position.y = m
		client.send_goal(goal)
		rospy.loginfo('sent goal')
		rospy.loginfo(goal)
		client.wait_for_result()
	
		m += 1.5 * sweep_width
		l -= (1.5 * sweep_width)		
	

if __name__ == '__main__':
	
	rospy.init_node('spiral')
	spiral_coverage()
	rospy.spin()

