
def EVcheck(*args):
	'''
	HEADS UP THIS MIGHT BE SLOW SINCE IT'S ACCESSING LIST ENTRIES?
    '''
	'''
	EVcheck stands for existence value check since it checks if a key exists (so no keyerror) then gets the value
	
	I think this is faster since it's a bunch of if checks whereas the list comprehension makes a listvar THEN equivalenece
	
	other way:
    [shared_metadata_dict[key]
        for key in shared_metadata_dict.keys()
        if key == "kivy_run_state"
    ] == [False]
    '''
	# print("args", args,flush = True) #looks like this: ([<DictProxy object, typeid 'dict' at 0x1e27e2ce490>, 'kivy_run_state', False],)
	dictVAR = args[0][0] #should be a dict
	keynameVAR = args[0][1] #should be a string
	desiredVAL = args[0][2] #value u are checking for
	if keynameVAR in dictVAR.keys():
		if dictVAR[keynameVAR] == desiredVAL:
			return True
		else: 
			return False
	else:
		return False

#original FileVideoStream from imutils: https://github.com/PyImageSearch/imutils/blob/master/demos/read_frames_fast.py

# import the necessary packages
from threading import Thread
import sys
import cv2
import time

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
	from queue import Queue
# otherwise, import the Queue class for Python 2.7
else:
	from Queue import Queue

class FCVAFileVideoStream:
	def __init__(self, path, transform=None, queue_size=30):
		# initialize the file video stream along with the boolean
		# used to indicate if the thread should be stopped or not
		self.stream = cv2.VideoCapture(path)
		self.stopped = False
		self.transform = transform

		# initialize the queue used to store frames read from
		# the video file
		self.Q = Queue(maxsize=queue_size)
		# intialize thread
		self.thread = Thread(target=self.update, args=())
		self.thread.daemon = True

	def start(self):
		# start a thread to read frames from the file video stream
		self.thread.start()
		return self

	def update(self):
		# keep looping infinitely
		while True:
			# if the thread indicator variable is set, stop the
			# thread
			if self.stopped:
				break

			# otherwise, ensure the queue has room in it
			if not self.Q.full():
				# read the next frame from the file
				(grabbed, frame) = self.stream.read()

				# if the `grabbed` boolean is `False`, then we have
				# reached the end of the video file
				if not grabbed:
					self.stopped = True
					
				# if there are transforms to be done, might as well
				# do them on producer thread before handing back to
				# consumer thread. ie. Usually the producer is so far
				# ahead of consumer that we have time to spare.
				#
				# Python is not parallel but the transform operations
				# are usually OpenCV native so release the GIL.
				#
				# Really just trying to avoid spinning up additional
				# native threads and overheads of additional
				# producer/consumer queues since this one was generally
				# idle grabbing frames.
				if self.transform:
					frame = self.transform(frame)

				# add the frame to the queue
				self.Q.put(frame.tobytes())
			else:
				time.sleep(0.1)  # Rest for 10ms, we have a full queue

		self.stream.release()

	def read(self):
		# return next frame in the queue
		return self.Q.get()

	# Insufficient to have consumer use while(more()) which does
	# not take into account if the producer has reached end of
	# file stream.
	def running(self):
		return self.more() or not self.stopped

	def more(self):
		# return True if there are still frames in the queue. If stream is not stopped, try to wait a moment
		tries = 0
		while self.Q.qsize() == 0 and not self.stopped and tries < 5:
			time.sleep(0.1)
			tries += 1

		return self.Q.qsize() > 0

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
		# wait until stream resources are released (producer thread might be still grabbing frame)
		self.thread.join()
