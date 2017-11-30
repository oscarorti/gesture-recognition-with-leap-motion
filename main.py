from threading import Thread

from face_detection import face_detector_gui
from gesture_recognition import gesture_recognizer


def launch_face_detection():
    print("FACE DETECTION ENABLED \n")
    face_detector_gui.run()


def launch_gesture_recognition():
    print("GESTURE RECOGNITION ENABLED \n")
    gesture_recognizer.run()


if __name__ == '__main__':
    face_detection_thread = Thread(target=launch_face_detection)
    gesture_recogntion_thread = Thread(target=launch_gesture_recognition)
    face_detection_thread.start()

    while True:
        if face_detector_gui.face_detected and not gesture_recogntion_thread.isAlive():
            gesture_recogntion_thread.start()
