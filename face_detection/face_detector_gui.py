import numpy as np
import dlib
import cv2


class FDetector:
    def __init__(self):
        self.face_detected = False

    def run(self):
        # Initialize dlib's face detector and then create the facial landmark predictor
        detector = dlib.get_frontal_face_detector()
        cap = cv2.VideoCapture(1)
        # For the resize image:
        cf = 4
        self.face_detected = False

        for it in range(1, 64, 1):
            # Capture frame-by-frame. The ret parameter is useful
            # when reading a file that can have an end. Now we read
            # from the webcam, so we don't have this problem
            ret, image = cap.read()

            # resize to be able to run in real-time
            imagemod = cv2.resize(image, (0, 0), fx=1 / float(cf), fy=1 / float(cf))
            # RGB -> B&W
            gray = cv2.cvtColor(imagemod, cv2.COLOR_BGR2GRAY)

            # detector of the faces in the grayscale frame
            rects = detector(gray, 1)

            for (i, rect) in enumerate(rects):
                self.face_detected = True

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def __to_help_opencv(self, rect):
        # take a bounding predicted by dlib and convert it
        # to the format (x, y, w, h) as we would normally do
        # with OpenCV
        x = rect.left()
        y = rect.top()
        w = rect.right() - x
        h = rect.bottom() - y

        # return a tuple of (x, y, w, h)
        return x, y, w, h

    def __shape_to_coords(self, shape, dtype="int"):
        # initialize the list of (x, y)-coordinates
        coords = np.zeros((68, 2), dtype=dtype)

        # loop over the 68 facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        # it is like a vector of 68 positions with 2 coordinates for each position
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)

        # return the list of (x, y)-coordinates
        return coords


if __name__ == '__main__':
    detector = FDetector()
    print detector.face_detected
    detector.run()
    print detector.face_detected
