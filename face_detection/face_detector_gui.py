import numpy as np
import dlib
import cv2

face_detected = False


def run():
    # Initialize dlib's face detector and then create the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("face_detection/shape_predictor_68_face_landmarks.dat")

    cap = cv2.VideoCapture(1)

    # For the resize image:
    cf = 4

    global face_detected
    while True:
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

        face_detected = False
        for (i, rect) in enumerate(rects):
            face_detected = True
            # determine the facial landmarks for the face region by entering the B&W image and the detection of a face
            shape = predictor(gray, rect)
            # convert the facial landmark (x, y)-coordinates to a NumPy array
            shape = __shape_to_coords(shape)

            # convert dlib's rectangle to a OpenCV-style bounding box
            (x, y, w, h) = __to_help_opencv(rect)
            # draw the face bounding box
            # parameters: image, one vertex, opposite vertex, color, thickness
            cv2.rectangle(image, (cf * x, cf * y), (cf * x + cf * w, cf * y + cf * h), (0, 255, 0), 2)

            # show the face number
            cv2.putText(image, "Face #{}".format(i + 1), (cf * x - 10, cf * y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)

            # loop over the (x, y)-coordinates for the facial landmarks and draw a point on the image
            for (x, y) in shape:
                cv2.circle(image, (cf * x, cf * y), 2, (0, 0, 255), -1)

        cv2.putText(image, "FaceDetection Camera", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
        # Display the resulting frame and press q to exit
        cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def __to_help_opencv(rect):
    # take a bounding predicted by dlib and convert it
    # to the format (x, y, w, h) as we would normally do
    # with OpenCV
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y

    # return a tuple of (x, y, w, h)
    return x, y, w, h


def __shape_to_coords(shape, dtype="int"):
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
    run()
