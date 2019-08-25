#!/usr/bin/python3
## init
import rospy
from vision_msgs.msg import Detection2DArray, Detection2D, BoundingBox2D, ObjectHypothesisWithPose
from std_msgs.msg import Float64, Int16, ColorRGBA

##			NOTES
##			w center = 160
##			h center = 120
##			_bbox_ limits = 100 - 300 (pes)
##			sto 300 prepei na paei deksia
##
##          _servo_ limits handled by the driver
##			0 = terma deksia
##			180 = terma aristera

rospy.init_node('faceDetection', anonymous=True)

# Variables

led_left = rospy.Publisher('/led/eye/left', ColorRGBA, queue_size=1)
led_right = rospy.Publisher('/led/eye/right', ColorRGBA, queue_size=1)
pub_w = rospy.Publisher('/servo/position/1', Float64, queue_size=1)
pub_h = rospy.Publisher('/servo/position/2', Float64, queue_size=1)
servo_w_pos = rospy.wait_for_message("/servo/last_position/1", Int16)
servo_h_pos = rospy.wait_for_message("/servo/last_position/2", Int16)
servo_w = int(servo_w_pos.data)
servo_h = int(servo_h_pos.data)
center_w = 160
center_h = 120
rospy.sleep(1.5)

# Initialiation
led_left.publish(255.0, 0.0, 0.0, 0.0)
led_right.publish(255.0, 0.0, 0.0, 0.0)
pub_w.publish(90)
pub_h.publish(90)

## actual work
  
def facedetection_cb(data):
  w = int(data.detections[0].results[0].pose.pose.position.x)
  h = int(data.detections[0].results[0].pose.pose.position.y)
  obj_id = int(data.detections[0].results[0].id)
  global servo_w
  global center_w
  global servo_h
  global center_h
  global pub_w
  global pub_h

  if obj_id == 0:
    if ((w - center_w) > 15):
      servo_w -= 1
      pub_w.publish(servo_w)
    if ((w - center_w)) < -15:
      servo_w += 1
      pub_w.publish(servo_w)
    if ((h - center_h) > 15):
      servo_h += 1
      pub_h.publish(servo_h)
    if ((h - center_h)) < -15:
      servo_h -= 1
      pub_h.publish(servo_h)
    else:
      pass

def facedetection():
  print("Starting..")
  while not rospy.is_shutdown():
    tpusub = rospy.Subscriber('/edgetpu/detections', Detection2DArray, facedetection_cb, queue_size=1)
    rospy.spin()


def shutdown_hook():
  global pub_w
  global pub_h
  global led_left
  global led_right
#  rospy.sleep(5)
  led_left.publish(0)
  led_right.publish(0)
  pub_w.publish(90)
  pub_h.publish(90)
  rospy.sleep(1)
  print ("shutdown time!")  


if __name__ == '__main__':
  facedetection()
#  rospy.on_shutdown(shutdown_hook)