# Import native python libraries
import sys
import os
import inspect
import math

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
from Leap import CircleGesture
from Leap import KeyTapGesture
from Leap import ScreenTapGesture
from Leap import SwipeGesture


def screentap_gesture_processing(self, gesture):
    screentap = ScreenTapGesture(gesture)
    handType = "Left hand" if screentap.hands[0].is_left else "Right hand"
    print "  Screen Tap id: %d, %s, hand: %s" % (
        gesture.id, self.STATES[gesture.state], handType)


def keytap_gesture_processing(self, gesture):
    keytap = KeyTapGesture(gesture)
    handType = "Left hand" if keytap.hands[0].is_left else "Right hand"
    print "  Key Tap id: %d, %s, hand: %s" % (
        gesture.id, self.STATES[gesture.state], handType)


def swipe_gesture_processing(self, gesture):
    swipe = SwipeGesture(gesture)
    handType = "Left hand" if swipe.hands[0].is_left else "Right hand"
    if swipe.direction[0] > 0 and math.fabs(swipe.direction[0]) > math.fabs(swipe.direction[1]):
        swipe_direction = "right"
    elif swipe.direction[0] < 0 and math.fabs(swipe.direction[0]) > math.fabs(swipe.direction[1]):
        swipe_direction = "left"
    elif swipe.direction[1] > 0 and math.fabs(swipe.direction[0]) < math.fabs(swipe.direction[1]):
        swipe_direction = "up"
    elif swipe.direction[1] < 0 and math.fabs(swipe.direction[0]) < math.fabs(swipe.direction[1]):
        swipe_direction = "down"
    if gesture.state is not Leap.Gesture.STATE_UPDATE:
        print "  Swipe id: %d, state: %s, hand: %s, direction: %s" % (
            gesture.id, self.STATES[gesture.state], handType, swipe_direction)


def circle_gesture_processing(self, controller, gesture):
    circle = CircleGesture(gesture)
    handType = "Left hand" if circle.hands[0].is_left else "Right hand"
    # Determine clock direction using the angle between the pointable and the circle normal
    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2:
        clockwiseness = "clockwise"
    else:
        clockwiseness = "counterclockwise"

    # Calculate the angle swept since the last frame
    swept_angle = 0
    if circle.state != Leap.Gesture.STATE_UPDATE:
        previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
        swept_angle = (circle.progress - previous_update.progress) * 2 * Leap.PI

        # TODO: Check gesture status and print only start-end gesture
        if gesture.state is not Leap.Gesture.STATE_UPDATE:
            print "  Circle id: %d, %s, radius: %f, hand: %s, %s" % (gesture.id, self.STATES[gesture.state],
                                                                     circle.radius, handType, clockwiseness)
