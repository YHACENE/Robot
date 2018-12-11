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

from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
"""
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", re)
"""
class MyFactory(GstRtspServer.RTSPMediaFactory):
	def __init__(self, **properties):
		super(MyFactory, self).__init__(**properties)
		self.cam = VideoStream(usePiCamera=True).start() #PiCamera()
		self.classifer = cv2.CascadeClassifier("/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml")
		self.cam.resolution  = (1920, 1088)
		self.data = pickle.load(open("encodungs.pickle", "rb").read())
		self.cam.framerate = 25.0
		self.number_frame = 0
		self.duration = 1 / 25.0 * Gst.SECOND
		self.rawcap = PiRGBArray(self.cam, size=(1920, 1088))
		self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width=1920,height=1088,framerate=25/1 ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency threads=8 ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96'
		time.sleep(2.0)
		self.fps = FPS().start()
	def get_faces(self, frame):
		minisize = (frame.shape[1]/4, frame.shape[0]/4)
		miniframe = cv2.resize(frame, minisize)
		faces = self.classifier.detectMultiScale(miniframe)
		return faces

	def on_need_data(self, src, lenght):
		ret, frame = self.cam.read()
		frame = imutils.resize(frame, width=500)
		if ret:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			#data = frame.array
			faces = detector.detectMultiScale(gray, scaleFactor=1.1,
				minNeighbors=5, minSize=(30, 30),
				flags=cv2.CASCADE_SCALE_IMAGE)

			boxes = [(y, x + w, y + h, x) for (x, y, w, h) in faces]
			encodings = face_recognition.face_encodings(rgb, boxes)
			names = []

			for encodings in encodings:
				matches = face_recognition.compare_faces(self.data["encodings"], encodings)
				name = "Unknown"

				if True in matches:
					matchedIndexs = [i for (i, b) in enumerate(matches) if b]
					counts = {}

					for i in matchedIndexs:
						name = self.data["name"][i]
						counts[name] = counts.get(name, 0) +1

					name = max(counts, key=counts.get)
				names.append(name)
			for ((top, right, bottom, left), name) in zoip(boxes, names):
				cv2.rectangle(frame, (left, top), (right, bottom),
					(0, 255, 0), 2)
				y = top - 15 if top - 15 > 15 else top + 15
				cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
					0.75, (0, 255, 0), 2)

			buf = Gst.Buffer.new_allocate(None, len(frame), None)
			buf.fill(0, frame)
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
