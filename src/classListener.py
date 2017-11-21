"""
Leap motion listener where gestures are defined and configured.
"""

# Import native python libraries
import sys
import os
import inspect
from collections import deque
import math

# Import src dependences
import gestures_processing

# Setup environment variables
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../LeapSDK/lib/x64' if sys.maxsize > 2**32 else '../LeapSDK/lib/x86'
# Mac
# arch_dir = os.path.abspath(os.path.join(src_dir, '../LeapSDK/lib')
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path.insert(0, "../LeapSDK/lib")

# Import LeapSDK
import Leap


class MyListener(Leap.Listener):
    FINGERS = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    FINGER_BONES = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    STATES = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def __init__(self):
        """
        The following code is for plotting purposes
        """

        super(self.__class__, self).__init__()
        self.angle_data = []
        self.hand_angle = None
        # four fingers to keep track of
        for i in range(4):
            self.angle_data.append(deque([0] * 1000, 1000))
        self.confidence = 0
        self.avg_a = 0
        self.new_finger_down = 3
        self.finger_down = None

    def get_angle_data(self):
        return self.angle_data

    def pop_new_finger_down_if_any(self):
        finger = self.new_finger_down
        self.new_finger_down = None
        return finger

    def get_hand_direction(self):
        return self.hand_direction

    def get_confidence(self):
        return self.confidence

    # hand angle in relation to the eh, "left" vector, (-1, 0, 0).
    def get_hand_angle(self):
        return self.hand_angle

    def get_average_angle(self):
        return self.avg_a

    def get_angle_data(self):
        return self.angle_data

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        if controller.is_connected:
            print ("Connected")
        else:
            print ("ERROR")
            quit()

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

        if controller.is_gesture_enabled(Leap.Gesture.TYPE_CIRCLE) and \
           controller.is_gesture_enabled(Leap.Gesture.TYPE_KEY_TAP) and \
           controller.is_gesture_enabled(Leap.Gesture.TYPE_SCREEN_TAP) and \
           controller.is_gesture_enabled(Leap.Gesture.TYPE_SWIPE):

            # Custom values
            circle_min_radius = 30.0  # unit: mm
            circle_min_arc = 1.5 * math.pi	  # unit: radians
            swipe_min_length = 150.0  # unit: mm
            swipe_min_velocity = 1000.0  # unit: mm/s
            keytap_min_down_velocity = 1000.0  # unit: mm/s
            keytap_history_seconds = .001  # unit: s
            keytap_min_distance = 50.0  # unit: mm
            screentap_min_forward_velocity = 50.0  # unit: mm/s
            screentap_history_seconds = .001  # unit: s
            screentap_min_distance = 5.0  # unit: mm

            controller.config.set("Gesture.Circle.MinRadius", circle_min_radius)
            controller.config.set("Gesture.Circle.MinArc", circle_min_arc)
            controller.config.set("Gesture.Swipe.MinLength", swipe_min_length)
            controller.config.set("Gesture.Swipe.MinVelocity", swipe_min_velocity)
            controller.config.set("Gesture.KeyTap.MinDownVelocity", keytap_min_down_velocity)
            controller.config.set("Gesture.KeyTap.HistorySeconds", keytap_history_seconds)
            controller.config.set("Gesture.KeyTap.MinDistance", keytap_min_distance)
            controller.config.set("Gesture.ScreenTap.MinForwardVelocity", screentap_min_forward_velocity)
            controller.config.set("Gesture.ScreenTap.HistorySeconds", screentap_history_seconds)
            controller.config.set("Gesture.ScreenTap.MinDistance", screentap_min_distance)
            controller.config.save()

            print("Geastures enabled")
        else:
            print('Device error, gestures can not be enabled, exit code: 4686446')
            quit()

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        if not controller.is_connected:
            print ("Disconnected")

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                gestures_processing.circle_gesture_processing(self, controller, gesture)
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                gestures_processing.swipe_gesture_processing(self, gesture)
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                gestures_processing.keytap_gesture_processing(self, gesture)
            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                gestures_processing.screentap_gesture_processing(self, gesture)
