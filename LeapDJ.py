#!/usr/bin/python
# ------------------------------------------------------------ #
# File: LeapDJ
# ------------
# Implementation of gesture recognition on the leap
# for a max patch that uses gestures to control a 'DJ' kit.
# intended as a demonstration of capabilities of NIPy
# ------------------------------------------------------------ #
import os
from NIPy.devices.DeviceReceiver import DeviceReceiver
from NIPy.motion_sequence.MotionSequence import *
from NIPy.recording.Recorder import Recorder
from NIPy.file_storage.StorageDelegate import StorageDelegate
from NIPy.visualization.Visualizer import Visualizer
from NIPy.motion_sequence_editing.MotionSequenceEditor import MotionSequenceEditor
from NIPy.gesture_detection.GestureDetector import GestureDetector


class LeapDJ:

    #==========[ MEMBER OBJECTS ]==========
    storage_delegate = None
    leap_receiver = None
    visualizer = None
    gesture_detector = None

    #==========[ DATA ]==========
    gesture_recordings = {}                 # dict gestures: activity_name -> panel of dataframes



    ########################################################################################################################
    ##############################[ --- Initialization/Constructor --- ]####################################################
    ########################################################################################################################

    # Function: print_welcome
    # -----------------------
    # prints a welcome message
    def print_welcome (self):
        print "######################################################################"
        print "#########[ --- LeapDJ: Natural Interaction DJ Controller --- ]########"
        print "###############[ -   by Jay Hack, Winter 2013/14      - ]#############"
        print "######################################################################"
        print "\n"


	# Function: Constructor
	# ---------------------
	# initializes PyMotion instance:
    #   - receiver
    #   - storage_delegate
    def __init__ (self, classifier_name='HmmScore'):

        self.print_welcome ()

        #===[ NIPy setup ]===
        print_status ("Initialization", "Storage Delegate")
        self.storage_delegate = StorageDelegate (os.path.join (os.getcwd(), 'data'))
        print_status ("Initialization", "Leap Receiver")
        self.leap_receiver = DeviceReceiver ('leap')
        print_status ("Initialization", "Visualizer")
        self.visualizer = Visualizer ()
        print_status ("initialization", "Editor")
        self.editor = MotionSequenceEditor ()
        print_status ("Initialization", "Detector")
        self.get_gesture_recordings ()
        self.gesture_detector = GestureDetector (self.gesture_recordings)




    ########################################################################################################################
    ##############################[ --- Recording --- ]#####################################################################
    ########################################################################################################################

    # Function: record
    # ----------------
    # creates a recording and returns it as a motion_sequence
    def record (self):

        print_notification ('<enter> to start recording, <enter> again to stop')
        recorder = Recorder (self.leap_receiver)
        raw_input ()
        print "==========[ START RECORDING ]=========="
        recorder.start ()
        raw_input ()
        print "==========[ RECORDING COMPLETE ]=========="
        recorder.stop ()
        return recorder.get_motion_sequence ()


    # Function: get_gesture_recordings
    # --------------------------------
    # given gesture name/number of desired recording and
    # returns them
    def make_gesture_recordings (self, gesture_name, num_recordings=10): 

        print_header ("Recording gesture: " + gesture_name + " (" + str(num_recordings) + ")")
        for i in range(num_recordings):
            print_header ("Raw Recording:")
            recording = self.record ()
            print_header ("Accept/Reject Recording (y/n):")
            self.visualizer.plot_motion_sequence (recording)
            response = raw_input (">>> (y/n)")
            if response == 'y':
                print_header ("Trim Recording")
                self.editor.trim (recording)
                self.storage_delegate.save_gesture_recording (recording, gesture_name)


    # Function: get_gesture_recordings
    # --------------------------------
    # fills self.gesture_recordings w/ a dict mapping gesture_name -> list of recordings
    def get_gesture_recordings (self):

        gestures = self.storage_delegate.get_existing_gestures ()
        for gesture in gestures:
            rs = self.storage_delegate.get_gesture_recordings (gesture)
            self.gesture_recordings[gesture] = rs






    ########################################################################################################################
    ##############################[ --- Detection --- ]#####################################################################
    ########################################################################################################################

    # Function: get_frame_source
    # --------------------------
    # given a recording name, returns the frame source
    def get_frame_source (self, recording_name):

        if not recording_name:
            return self.receiver

        else:
            recording = self.storage_delegate.get_recording (recording_name)
            return PlayBack (recording)


    # Function: detect_gestures
    # -------------------------
    # call this function after initialization to detect gestures
    # if recording_name is none, it gets them real-time, otherwise
    # it gets them from playback
    def detect_gestures (self, recording_name=None):

        self.detector.detect_gestures (self.get_frame_source (recording_name), self.classifier)



    ########################################################################################################################
    ##############################[ --- User Interface --- ]################################################################
    ########################################################################################################################

    # Function: get_mode
    # ------------------
    # prompts user for their desired mode, returns it
    def get_mode (self):

        print_header ("Enter Mode:")
        print " - R: Record new data"
        print " - A: Analyze existing data"
        response = raw_input ("---> ").lower()
        return response


    # Function: get_gesture_name
    # ----------------------------
    # prints out existing gesture names, prompts user for the one they want
    def get_gesture_name (self):

        gestures = self.storage_delegate.get_existing_gestures ()

        ### Step 1: interface ###
        print_header ("enter gesture index (999 for new gesture): ")
        for index, a in enumerate(gestures):
            print "[", index, "] ", a

        ### Step 2: get the name, sanitize it ###
        gesture_index = raw_input ("---> ")
        if not gesture_index.isdigit ():
            print_notification ("Error: enter a real index (a digit)")
            return self.get_gesture_name ()
        else:
            gesture_index = int(gesture_index)
            if not (gesture_index == 999 or gesture_index in range (len(gestures))):
                print_notification ("Error: enter a real index (one in the correct range)")
                return self.get_gesture_name ()

        ### Step 3: interpret it ###
        if gesture_index == 999:
            print_header ("Enter new activity name")
            gesture_name = raw_input ("---> ")
            return gesture_name
        else:
            return gestures[gesture_index]


    # Function: interface_main
    # ------------------------
    # main function for all interface
    def interface_main (self):

        #==========[ Get Mode ]==========
        mode = self.get_mode ()

        #==========[ Recording Mode ]==========
        if mode == 'r':

            gesture_name = self.get_gesture_name ()
            self.make_gesture_recordings (gesture_name)

        #==========[ Detection Mode ]==========
        elif mode == 'd':

            self.detect_gestures ()

        #==========[ Analyze Mode ]==========
        elif mode == 'a':
            print_error ("Analyze Mode: not yet implemented")
        
        #==========[ Unrecognized Mode ]==========
        else:
            print_notification("Error: did not recognize that option")
            self.interface_main ()


    # Function: run_ui
    # ----------------
    # runs the program w/ a ui for recording, analyzing
    def run_ui (self):

        while (True):
            self.interface_main ()






if __name__ == "__main__":

    dj = LeapDJ ()
    dj.detect_gestures ()









