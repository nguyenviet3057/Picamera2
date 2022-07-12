from picamera2 import PiCamera2
from threading import Thread
import cv2
import time
import simplejpeg as sj

class PiVideoStream:
	def __init__(self, resolution=(800, 640), framerate=32, **kwargs):
		# initialize the camera
		self.camera = PiCamera2()

		# set camera parameters
		self.camera.resolution = resolution
		self.camera.framerate = framerate

		# set optional camera parameters (refer to PiCamera docs)
		for (arg, value) in kwargs.items():
			setattr(self.camera, arg, value)

		# initialize the stream
		self.stream = self.camera.capture_array(wait=False)

		# initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.frame = None
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		for f in self.stream:
			# grab the frame from the stream and clear the stream in
			# preparation for the next frame
			self.frame = f.array

			# if the thread indicator variable is set, stop the thread
			# and resource camera resources
			if self.stopped:
				self.stream.close()
				self.camera.close()
				return

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

frameCount = 0
print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream(resolution=(800,640)).start()
time.sleep(1.0)
timePoint = time.time()
while (time.time-timePoint<10):
    vs.read()
    #buffer = sj.encode_jpeg(vs.read(),25,'rgb','444',True)
    frameCount += 1
    
print("{:.2f}".format(frameCount/(time.time()-timePoint)))
print("{:.2f}".format(time.time()-timePoint))
vs.stop()