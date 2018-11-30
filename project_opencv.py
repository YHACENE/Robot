#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
#import gst
#import pygst
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0') 
from gi.repository import GObject, Gst, GstRtspServer
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy
import time

class MyFactory(GstRtspServer.RTSPMediaFactory):
	def __init__(self):
		GstRtspServer.RTSPMediaFactory.__init__(self)

	def do_create_element(self, url):
		spec =  """ appsrc ! queue ! h264parse ! videoconvert ! rtph264pay config-interfal=1 pt=96"""
		return Gst.parse_launch(spec)

class GstServer():
	def __init__(self):
		self.server = GstRtspServer.RTSPServer()
		self.server.set_service("3002")
		f = MyFactory()
		f.set_shared(True)
		m = self.server.get_mount_points()
		m.add_factory("/capture", f)
		self.server.attach(None)

class VideoCamera():
	def __init__(self, interval = 0.1):
		self.camera = PiCamera()
		self.rawCapture = None
		self.classifier = None
		self.interval = interval

	def prep_cam(self, dimL, diml, rate):
		self.camera.resolution  = (dimL, diml)
		self.camera.framerate = rate
		self.rawCapture = PiRGBArray(self.camera, size=(dimL, diml))
		self.classifier = cv2.CascadeClassifier("/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml") 
		time.sleep(0.1)

	def get_faces(self, frame):
		minisize = (frame.shape[1]/4, frame.shape[0]/4)
		miniframe = cv2.resize(frame, minisize)
		faces = self.classifier.detectMultiScale(miniframe)
		return faces

	def camera_show(self):
		#fourcc = cv2.VideoWriter_fourcc(*'MPG4')
		#fourcc = cv2.cv.CV_FOURCC(*'MJPG')
		#out = cv2.VideoWriter('test.avi', fourcc, 20.0, (640, 480))
		#out = cv2.VideoWriter('appsrc ! queue ! h264parse ! videoconvert ! rtph264pay config-interfal=1 pt=96 ! gdppay ! tcpserversink host=192.168.10.12 port= 5000', fourcc, 20.0,(640, 480))

		for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
			time.sleep(self.interval)
			image = frame.array
			faces = self.get_faces(image)
			for f in faces:
				x, y, w, h = [v*4 for v in f]
				cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0))

			#cv2.imshow("Image", image)
			#out.write(image)
			key = cv2.waitKey(1) & 0xFF
			self.rawCapture.truncate(0)
			if key == ord('q'):
				break
		#out.release()
		#cv2.destroyAllWindows()

if __name__=="__main__":
	PC = VideoCamera()
	PC.prep_cam(640, 480, 25) #1280, 720
	PC.camera_show()
	loop = GObject.MainLoop()
	GObject.threads_init()
	Gst.init(None)
	s = GstServer()
	loop.run()
