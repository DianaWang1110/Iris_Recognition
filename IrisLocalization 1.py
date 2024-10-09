import cv2
import numpy as np
import os
def detect_pupil_iris_new(image,iris_constant):
    # if len(image.shape) == 3:
    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blurred = cv2.medianBlur(image, 5) # blur image to remove noise
    circles = cv2.HoughCircles(image_blurred, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=1, minRadius=20, maxRadius=60) # detect pupils using Hough Transform

    if circles is not None:
        circles = np.uint16(np.around(circles)) # convert the (x, y) coordinates and radius of the pupil to integers
        pupil = circles[0][0]

        # Add a constant radius to the pupil radius
        # Add iris_constant to the pupil's radius to estimate the iris's size,
        # which is the size of the circle that surrounds the pupil
        iris = pupil.copy()
        iris[2] = iris[2] + iris_constant
        # draw circle
        # cv2.circle(image, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
        return (image,pupil,iris)

    return None

# param1: This is the higher threshold for the internal Canny edge detector. Increasing this value reduces false circle detection but may miss real circles. Decreasing it may increase circle detection but also false positives.
# param2: This is the accumulator threshold for the circle centers at the detection stage. Lowering this value increases the likelihood of detecting circles but also false circles. Increasing it may result in missing real circles.
