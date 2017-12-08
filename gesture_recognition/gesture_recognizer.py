"""
Main script to execute the gesture recognition software.
"""

# Import native python libraries
import inspect
import os
import sys
from listener import MyListener
from face_detection import face_detector_gui
import time

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


def run_step():

    face = face_detector_gui.FDetector()
    face.run()
    print face.face_detected
    if face.face_detected:
        # Create a sample listener and controller
        listener = MyListener()
        controller = Leap.Controller()
        controller.set_policy_flags(Leap.Controller.POLICY_IMAGES)
        # Have the sample listener receive events from the controller
        controller.add_listener(listener)

        t_end = time.time() + 20
        while time.time() < t_end:
            pass
    return


if __name__ == "__main__":
    while True:
        run_step()
