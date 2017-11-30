"""
Main script to execute the gesture recognition software.
"""

# Import native python libraries
import inspect
import os
import sys
from listener import MyListener
import cameras

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


def run():
    # Create a sample listener and controller
    listener = MyListener()
    controller = Leap.Controller()
    controller.set_policy_flags(Leap.Controller.POLICY_IMAGES)
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    # 1D plot
    # plotter = Plotter(listener)

    try:
        cameras.run(controller)
    except KeyboardInterrupt:
        sys.exit(0)
    while True:
        pass


if __name__ == "__main__":
    run()
