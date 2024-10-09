import numpy as np
import cv2

def iris_normalization(image, pupil, iris):
    # Assuming the input image is grayscale, there's no need to specify a channel when accessing pixel values
    normalized_iris = np.zeros((64, 512), dtype=np.uint8)  # Adjusted size for grayscale image as set in Ma's article

    # Getting the new range for radius
    r_min = pupil[2]
    r_max = iris[2]
    
    for i in range(512):  # Loop over width
        theta = 2 * np.pi * i / 512  # calculate theta in current direction
        for j in range(64):  # Loop over height
            r_rel = j / 63  # Normalized position between 0 and 1
            r = r_rel * (r_max - r_min) + r_min # actual radical coordinate
            x = pupil[0] + r * np.cos(theta) # Unwrapping in pseudopolar coordinate
            y = pupil[1] + r * np.sin(theta)
            
            # Check if the computed coordinates are within image boundaries
            if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:  # Ensure it doesn't go out of bounds
                normalized_iris[j, i] = image[int(y), int(x)]  
    return normalized_iris