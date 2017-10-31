
import sys
import os
import inspect

# Setup environment variables
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))

# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

# Mac
# arch_dir = os.path.abspath(os.path.join(src_dir, '../lib')

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

# Import external libraries
import Leap
from Leap import CircleGesture
from Leap import KeyTapGesture
from Leap import ScreenTapGesture
from Leap import SwipeGesture
from collections import deque
import _vmath
import math


class MyListener(Leap.Listener):
    FINGERS = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    FINGER_BONES = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    STATES = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    # TODO: Find optimal thresholds for the following variables
    MIN_TIME_BETWEEN_GESTURES = 12
    MIN_MOVEMENT_VELOCITY = 5
    MAX_MOVEMENT_VELOCITY = 50

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

        if controller.is_gesture_enabled(Leap.Gesture.TYPE_CIRCLE) or \
           controller.is_gesture_enabled(Leap.Gesture.TYPE_KEY_TAP) or \
           controller.is_gesture_enabled(Leap.Gesture.TYPE_SCREEN_TAP) or \
           controller.is_gesture_enabled(Leap.Gesture.TYPE_SWIPE):




            # Custom values
            circle_min_radius = 50.0  # unit: mm
            circle_min_arc = 1.5 * math.pi	  # unit: radians
            swipe_min_length = 150.0  # unit: mm
            swipe_min_velocity = 1000  # unit: mm/s
            keytap_min_down_velocity = 50.0  # unit: mm/s
            keytap_history_seconds = .1  # unit: s
            keytap_min_distance = 3.0  # unit: mm
            screentap_min_forward_velocity = 50.0  # unit: mm/s
            screentap_history_seconds = .1  # unit: s
            screentap_min_distance = 5.0  # unit: mm

            # Default values
            # circle_min_radius = 5.0  # unit: mm
            # circle_min_arc = 1.5 * math.pi	  # unit: radiansc
            # swipe_min_length = 150.0  # unit: mm
            # swipe_min_velocity = 1000  # unit: mm/s
            # keytap_min_down_velocity = 50.0  # unit: mm/s
            # keytap_history_seconds = .1  # unit: s
            # keytap_min_distance = 3.0  # unit: mm
            # screentap_min_forward_velocity = 50.0  # unit: mm/s
            # screentap_history_seconds = .1  # unit: s
            # screentap_min_distance = 5.0  # unit: mm

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



    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        if not controller.is_connected:
            print ("Disconnected")

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # Get hands
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"

                # Calculate the angle swept since the last frame
                swept_angle = 0

                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

               # print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
               #         gesture.id, self.STATES[gesture.state],
               #         circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

                    # TODO: Check gesture status and print only start-end gesture
                    if gesture.state is not Leap.Gesture.STATE_UPDATE:
                        print "  Circle id: %d, %s, radius: %f, hand: %s, %s" % (gesture.id, self.STATES[gesture.state],
                                                                        circle.radius, handType, clockwiseness)

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                swipeDir = swipe.direction

                if (swipeDir[0] > 0 and math.fabs(swipeDir[0]) > math.fabs(swipeDir[1])):
                    dir = "right"
                elif (swipeDir[0] < 0 and math.fabs(swipeDir[0]) > math.fabs(swipeDir[1])):
                    dir = "left"
                elif (swipeDir[1] > 0 and math.fabs(swipeDir[0]) < math.fabs(swipeDir[1])):
                    dir = "up"
                elif (swipeDir[1] < 0 and math.fabs(swipeDir[0]) < math.fabs(swipeDir[1])):
                    dir = "down"

                # TODO: Check gesture status and print only start-end gesture
                if gesture.state is not Leap.Gesture.STATE_UPDATE:

                    #print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                    #        gesture.id, self.STATES[gesture.state],
                    #        swipe.position, swipe.direction, swipe.speed)
                    print "  Swipe id: %d, state: %s, hand: %s, direction: %s" % (
                        gesture.id, self.STATES[gesture.state], handType, dir)

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)

                #print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                #    gesture.id, self.STATES[gesture.state],
                #    keytap.position, keytap.direction)

                print "  Key Tap id: %d, %s, hand: %s" % (
                    gesture.id, self.STATES[gesture.state], handType)

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screentap = ScreenTapGesture(gesture)

                #print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
                #    gesture.id, self.STATES[gesture.state],
                #    screentap.position, screentap.direction)

                print "  Screen Tap id: %d, %s, hand: %s" % (
                    gesture.id, self.STATES[gesture.state], handType)


        """
        The following code is used for the plot function
        """
        # TODO: Understand how plotter goes

        self.confidence = frame.hands[0].confidence
        angle = 4 * [None]

        if self.confidence < 0.1:
            self.avg_a = None
            return

        hd = frame.hands[0].direction
        self.hand_angle = _vmath.angle_between((-1, 0, 0), (hd.x, hd.y, hd.z))

        for i, a in enumerate(self.angle_data):
            d = frame.hands[0].fingers[i + 1].bone(2).direction
            angle[i] = math.pi / 2 - _vmath.angle_between((0, 1, 0), (d.x, d.y, d.z))
            a.appendleft(angle[i])

        # find the finger pointing most downwards
        # and also the "second most downwards" finger.
        # if the difference between them is large enough we conclude
        # that one finger points downwards while the others don't.
        down_fingers = []
        down_fingers.append({'angle': 0.0, 'finger_index': 0})
        down_fingers.append({'angle': 0.0, 'finger_index': 0})

        for i in range(3):
            if angle[i] > down_fingers[0]['angle']:
                down_fingers[1] = down_fingers[0]
                down_fingers[0] = {'angle': angle[i], 'finger_index': i}
            elif angle[i] > down_fingers[1]['angle']:
                down_fingers[1] = {'angle': angle[i], 'finger_index': i}

        angle_diff = down_fingers[0]['angle'] - down_fingers[1]['angle']
        if down_fingers[0]['finger_index'] != -1 and angle_diff > 0.5:
            if self.finger_down != down_fingers[0]['finger_index']:
                self.finger_down = self.new_finger_down = down_fingers[0]['finger_index']
        elif self.finger_down != 3:
            # Hack, 3 means .. no finger down.
            self.finger_down = self.new_finger_down = 3

        # We calculate average without the finger pointing downwards the most ...
        fingers_for_average = range(4)
        fingers_for_average.remove(down_fingers[0]['finger_index'])
        angle_sum = 0
        for i in fingers_for_average:
            angle_sum += angle[i]
        self.avg_a = angle_sum / 3.0
