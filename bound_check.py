#!/usr/bin/python
# -*- coding:utf8 -*-

import std_msgs
import rospy, os, sys
import numpy as np
from nav_msgs.msg import Odometry 
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import Twist, Pose, PoseStamped, PoseWithCovariance, PoseWithCovarianceStamped


def point_inside_polygon(x,y,poly):

	n = len(poly)
	inside =False

	p1x,p1y = poly[0]
	for i in range(n+1):
		p2x,p2y = poly[i % n]
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xinters:
						inside = not inside
		p1x,p1y = p2x,p2y

	return inside



def check(data) :
	
	coords = []
	coords.append((49.8999820279, 8.90002784158))
	coords.append((49.8999820159, 8.89997216536))
	coords.append((49.9000179875, 8.89997216569))
	coords.append((49.9000179783, 8.90002784162))

	rospy.set_param('in_or_out', point_inside_polygon(data.latitude, data.longitude, coords))
	


if __name__ == '__main__':

	rospy.init_node('bound_check')
	subgps = rospy.Subscriber("/navsat/fix", NavSatFix, check)
	

	rospy.spin()	
	
	
