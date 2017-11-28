from threading import Thread

from face_recognition import face_detect_best
from gesture_recognition import launch_app


def launch_face_detection():
    print("initializing face detection")
    face_detect_best.start()


def launch_gesture_recognition():
    print('initializing gesture recognition')
    launch_app.main()


if __name__ == '__main__':
    face_detection_thread = Thread(target=launch_face_detection)
    gesture_recogntion_thread = Thread(target=launch_gesture_recognition)
    face_detection_thread.start()

    while True:
        if face_detect_best.face_detected:
            gesture_recogntion_thread.start()
