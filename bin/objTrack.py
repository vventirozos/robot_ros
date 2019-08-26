#!/usr/bin/python3
import rospy
from vision_msgs.msg import Detection2DArray, Detection2D, BoundingBox2D, ObjectHypothesisWithPose
from std_msgs.msg import Float64, Int16, ColorRGBA

rospy.init_node('objDetection', anonymous=True)

class obj_detection:
  
  def __init__(self):
    self.tpusub = rospy.Subscriber('/edgetpu/detections', Detection2DArray, self.objdetection_cb, queue_size=1)
    self.pub_w = rospy.Publisher('/servo/position/1', Float64, queue_size=1)
    self.pub_h = rospy.Publisher('/servo/position/2', Float64, queue_size=1)
    self.servo_w_center = 90
    self.servo_h_center = 90
    self.servo_w = self.servo_w_center
    self.servo_h = self.servo_h_center
    self.center_w = 160
    self.center_h = 120

# callback 
  def objdetection_cb(self, data):
    self.obj_id = int(data.detections[0].results[0].id)
    if self.obj_id == 0:
      self.w = int(data.detections[0].results[0].pose.pose.position.x)
      self.h = int(data.detections[0].results[0].pose.pose.position.y)
      self.objtrack(self.w,self.h)
    else:
      print("no person found")

# servo tracking function
  def objtrack(self, w, h):
    if ((self.w - self.center_w) > 15):
      self.servo_w -= 1
      self.pub_w.publish(self.servo_w)
    if ((self.w - self.center_w)) < -15:
      self.servo_w += 1
      self.pub_w.publish(self.servo_w)
    if ((self.h - self.center_h) > 15):
      self.servo_h += 1
      self.pub_h.publish(self.servo_h)
    if ((self.h - self.center_h)) < -15:
      self.servo_h -= 1
      self.pub_h.publish(self.servo_h)

# robot initialization,should add more like leds and such..
  def init_robot (self):
    print("Resetting Servos..")
    rospy.sleep(1)
    self.pub_w.publish(self.servo_w_center)
    self.pub_h.publish(self.servo_h_center)

# TPU subscription
  def objdetection(self):
    self.tpusub

################## ############### #################

od = obj_detection()
od.init_robot()
print ("Starting..")

while not rospy.is_shutdown():
  od.objdetection()

#print (od.obj_id)