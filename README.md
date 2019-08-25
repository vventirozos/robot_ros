# gopigo3 based project with:
##### RPLidar A1
##### Coral USB accelerator
##### Raspberry pi v2 camera
##### Pan and tilt servos 
##### Speaker-mic (soon..)
##
##
Initial commit contains a modified gopigo3 ROS "driver" with different servo interface, some extra publishers,
and different transformations that can be used easily for slam, see : https://github.com/iot-magi/gopigo3_navigation
Also contains a ROS node for coral edge TPU usb accelerator, modified from : https://github.com/jveitchmichaelis/edgetpu_ros
By default it will subscribe to a raspicam compressed image topic taking advantage of the hardware acceleration.
This node will publish messages of type: Detection2DArray in /edgetpu/detections. There are some variations of the script like
using raw / compressed image messages, publishing with / without including image data.
(I will probably will change this to dynamic parameters at some point..)
Last, it includes a very basic person tracker that uses servos and the TPU to detect persons and keep them at the center
of the frame.
##

Setting everything up is not very straight forward. TPU only supports python3 so you will need openCV bridge
compiled for python3 aswell.

Tested on:
* Raspberry Pi 4
* Raspbian Buster
* Python 3
* ROS Melodic
