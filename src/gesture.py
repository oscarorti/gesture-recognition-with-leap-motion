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


class Gesture(object):
    STATES = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def screentap_processing(self, gesture):
        screentap = ScreenTapGesture(gesture)
        hand_type = self.__get_screentap_hand(screentap)
        return gesture.id, self.STATES[gesture.state], hand_type

    def keytap_processing(self, gesture):
        keytap = KeyTapGesture(gesture)
        hand_type = self.__get_keytap_hand(keytap)
        return gesture.id, self.STATES[gesture.state], hand_type

    def swipe_processing(self, gesture):
        swipe = SwipeGesture(gesture)
        hand_type = self.__get_swipe_hand(swipe)
        swipe_direction = self.get_swipe_direction(swipe)
        return gesture.id, self.STATES[gesture.state], hand_type, swipe_direction

    def circle_processing(self, controller, gesture):
        circle = CircleGesture(gesture)
        hand_type = self.__get_circle_hand(circle)
        clockwiseness = self.__get_circle_direction(circle)
        # Calculate the angle swept since the last frame
        swept_angle = 0
        previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
        swept_angle = (circle.progress - previous_update.progress) * 2 * Leap.PI
        return gesture.id, self.STATES[gesture.state], circle.radius, hand_type, clockwiseness

    def __get_circle_direction(self, circle):
        if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2:
            clockwiseness = "clockwise"
        else:
            clockwiseness = "counterclockwise"

        return clockwiseness

    def __get_screentap_hand(self, screentap):
        handType = "Left hand" if screentap.hands[0].is_left else "Right hand"
        return handType

    def __get_keytap_hand(self, keytap):
        handType = "Left hand" if keytap.hands[0].is_left else "Right hand"
        return handType

    def __get_swipe_hand(self, swipe):
        handType = "Left hand" if swipe.hands[0].is_left else "Right hand"
        return handType

    def get_swipe_direction(self, swipe):
        if swipe.direction[0] > 0 and math.fabs(swipe.direction[0]) > math.fabs(swipe.direction[1]):
            swipe_direction = "right"
        elif swipe.direction[0] < 0 and math.fabs(swipe.direction[0]) > math.fabs(swipe.direction[1]):
            swipe_direction = "left"
        elif swipe.direction[1] > 0 and math.fabs(swipe.direction[0]) < math.fabs(swipe.direction[1]):
            swipe_direction = "up"
        elif swipe.direction[1] < 0 and math.fabs(swipe.direction[0]) < math.fabs(swipe.direction[1]):
            swipe_direction = "down"
        return swipe_direction

    def __get_circle_hand(self, circle):
        handType = "Left hand" if circle.hands[0].is_left else "Right hand"
        return handType

    def __state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
