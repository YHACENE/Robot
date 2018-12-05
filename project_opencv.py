#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys

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
	def __init__(self, **properties):
		super(MyFactory, self).__init__(**properties)
		self.cap = PiCamera()
		self.classifer = cv2.CascadeClassifier("/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml")
		self.camera.resolution  = (640, 480)
		self.camera.framerate = 30
		self.number_frame = 0
		self.duration = 1 / 30 * Gst.SECOND
		self.rawcap = PiRGBArray(self.camera, size=(640, 480))
		self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width=640,height=480,framerate=30/1 ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency threads=8 ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96'
	def get_faces(self, frame):
		minisize = (frame.shape[1]/4, frame.shape[0]/4)
		miniframe = cv2.resize(frame, minisize)
		faces = self.classifier.detectMultiScale(miniframe)
		return faces

	def on_need_data(self, src, lenght):
		ret, frame = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
		if ret:
			data = frame.array
			faces = self.get_faces(data)
			for f in faces:
				x, y, w, h = [v*4 for v in f]
				cv2.rectangle(data, (x,y), (x+w, y+h), (255,0,0))

			buf = Gst.Buffer.new_allocate(None, len(data), None)
			buf.fill(0, data)
			buf.duration = self.duration
			timestamp = self.number_frames * self.duration
			buf.pts = buf.dts = int(timestamp)
			buf.offset = timestamp
			self.number_frames += 1
			retval = src.emit('push-buffer', buf)
			print('pushed buffer, frame {}, duration {} ns, durations {} s'.format(self.number_frames,
																				   self.duration,
																				   self.duration / Gst.SECOND))
			if retval != Gst.FlowReturn.OK:
				print(retval)

			#cv2.imshow("Image", image)
			key = cv2.waitKey(1) & 0xFF
			self.rawCapture.truncate(0)
			if key == ord('q'):
				break
	def do_create_element(self, url):
		return Gst.parse_launch(self.launch_string)

	def do_configure(self, rtsp_media):
		self.number_frame = 0
		appsrc = rtsp_media.get_element().get_child_by_name('source')
		appsrc.connect("need-data", self.on_need_data)

class GstServer(GstRtspServer.RTSPServer):
	def __init__(self, **properties):
		#super(GstServer, self).__init__(**properties)
		self.server = GstRtspServer.RTSPServer()
		self.server.set_service("3002")
		self.factory = MyFactory()
		self.factory.set_shared(True)
		self.server.get_mount_points().add_factory("/capture", self.factory)
		self.server.attach(None)

def run():
	GObject.threads_init()
    Gst.init(None)

    server = GstServer()

    loop = GObject.MainLoop()
    loop.run()

"""
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
"""
if __name__=="__main__":
	run()
	"""
	PC = VideoCamera()
	PC.prep_cam(640, 480, 25) #1280, 720
	PC.camera_show()
	loop = GObject.MainLoop()
	GObject.threads_init()
	Gst.init(None)
	s = GstServer()
	loop.run()
	"""
