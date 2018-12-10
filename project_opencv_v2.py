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
		self.cam = PiCamera()
		self.classifer = cv2.CascadeClassifier("/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml")
		self.cam.resolution  = (1920, 1088)
		self.cam.framerate = 25.0
		self.number_frame = 0
		self.duration = 1 / 25.0 * Gst.SECOND
		self.rawcap = PiRGBArray(self.cam, size=(1920, 1088))
		self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width=1920,height=1088,framerate=25/1 ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency threads=8 ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96'
	def get_faces(self, frame):
		minisize = (frame.shape[1]/4, frame.shape[0]/4)
		miniframe = cv2.resize(frame, minisize)
		faces = self.classifier.detectMultiScale(miniframe)
		return faces

	def on_need_data(self, src, lenght):
		ret, frame = self.cam.capture_continuous(self.rawcap, format="bgr", use_video_port=True)
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
			#key = cv2.waitKey(1) & 0xFF
			self.rawcap.truncate(0)
                        #if key == ord('q'):  break
	
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

if __name__=="__main__":
	run()
