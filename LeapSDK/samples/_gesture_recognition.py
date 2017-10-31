################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import inspect
# Import native python libraries
import os
import sys

# Import project modules

# Setup environment variables
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))

# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

# Mac
# arch_dir = os.path.abspath(os.path.join(src_dir, '../lib')

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

sys.path.insert(0, "../lib")

# Import external libraries
import Leap
from _plotter import Plotter
import _classListener


def main():
    # Create a sample listener and controller
    listener = _classListener.MyListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    plotter = Plotter(listener)

    while True:
        pass


if __name__ == "__main__":
    main()
