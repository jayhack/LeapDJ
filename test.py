#!/usr/local/bin/python
from NIPy.devices.DeviceReceiver import *
from NIPy.motion_sequence.MotionSequence import *
from NIPy.recording.Recorder import Recorder
from NIPy.file_storage.StorageDelegate import *
from NIPy.visualization.Visualizer import Visualizer
from NIPy.motion_sequence_editing.MotionSequenceEditor import MotionSequenceEditor
from NIPy.classification.GestureMonitor import GestureMonitor
from LeapDJ import LeapDJ

# Function: record
# ----------------
# creates a recording and returns it as a motion_sequence
def record (leap_receiver):

	print_notification ('Hit <enter> to start recording, <enter> again to stop')
	recorder = Recorder (leap_receiver)
	raw_input ()
	print "==========[ START RECORDING ]=========="
	recorder.start ()
	raw_input ()
	print "==========[ RECORDING COMPLETE ]=========="
	recorder.stop ()
	return recorder.get_motion_sequence ()

if __name__ == "__main__":

	# dj = LeapDJ ()
	# dj.get_gesture_recordings ()
	# r = dj.storage_delegate.get_recording ('1388393878.68.dataframe') #real recording
	# r = dj.storage_delegate.get_recording ('1388396063.37.dataframe') #real recording, up right
	# r = dj.storage_delegate.get_recording ('1388397101.56.dataframe') #real recording, left, right, up
	# dj.visualizer.plot_motion_sequence (r)
	# r = dj.storage_delegate.get_recording ('1388373754.69.dataframe') #right
	# dj.gesture_detector.detect (r)
	# r = dj.record ()
	# dj.storage_delegate.save_recording (r)

	try:

		#===[ Setup receiver, start its thread ]===
		# leap_receiver = DeviceReceiver ('leap')
		# leap_receiver.start ()
		storage_delegate = StorageDelegate ('data')

		#===[ Setup Motion Sequence ]===
		ms = storage_delegate.get_recording ('1388393878.68.dataframe') #real recording
		# ms = storage_delegate.get_recording ('1388396063.37.dataframe') #real recording, up right
		# ms = storage_delegate.get_recording ('1388397101.56.dataframe') #real recording, left, right, up		
		# ms = RealTimeMotionSequence (leap_receiver)

		#===[ Setup GestureMonitors, start their threads ]===
		up_monitor = GestureMonitor (storage_delegate.get_gesture_recordings('UP'), ms, 'UP')
		right_monitor = GestureMonitor (storage_delegate.get_gesture_recordings('RIGHT'), ms, 'RIGHT')
		left_monitor = GestureMonitor (storage_delegate.get_gesture_recordings('LEFT'), ms, 'LEFT')
		up_monitor.start ()
		right_monitor.start ()
		left_monitor.start ()


		for frame in ms.stream_frames ():
			print '.'

		up_monitor.stop()
		right_monitor.stop ()
		left_monitor.stop ()

	except (KeyboardInterrupt, SystemExit):
	    leap_receiver.stop ()
	    up_monitor.stop ()
	    right_monitor.stop ()













