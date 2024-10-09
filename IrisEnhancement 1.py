import numpy as np
import cv2

class Enhancement:
    def __init__(self):
        pass
    def estimate_background(self, image):
        nrow = int(image.shape[0] / 16) # define the number of rows and columns for 16*16 blocks in the image
        ncol = int(image.shape[1] / 16)
        new_image = np.repeat(np.NaN, repeats=nrow * ncol) # make a new image with NaN values
        new_image = new_image.reshape(nrow, ncol) # make this image into a matrix with nrow rows and ncol columns
        for row in range(nrow): # loop over each block
            for col in range(ncol):
                allrows = np.arange(row * 16, (row + 1) * 16) # create a block of 16*16 pixels
                allcols = np.arange(col * 16, (col + 1) * 16)
                value = np.mean(image[row * 16: (row + 1) * 16, col * 16: (col + 1) * 16]) # calculate the mean of the block
                new_image[row, col] = value # assign the mean value to the new image
        res = cv2.resize(new_image, None, fx=16, fy=16, interpolation=cv2.INTER_CUBIC) # fulfill the new image 
        return res

    def subtract_background(self, image):
        return image - self.estimate_background(image)

    def enhance_image(self, image): # histogram equalization to be applied in each loop
        image = np.array(image, dtype=np.uint8)
        image = cv2.equalizeHist(image)
        return image

    def enhance_image_by_parts(self, image):
        nrow = int(image.shape[0] / 32) # define the number of rows and columns for 32*32 blocks in the image
        ncol = int(image.shape[1] / 32)
        for row in range(nrow): # Loop over each block of the image to do histogram equalization
            for col in range(ncol):
                enhanced = self.enhance_image(image[row * 32: (row + 1) * 32, col * 32: (col + 1) * 32]) # define the start and end of the block
                image[row * 32: (row + 1) * 32, col * 32: (col + 1) * 32] = enhanced # Replace the original block with the enhanced block
        return image

    def perform_all_enhancements(self, image):
        # image = self.subtract_background(image)
        image = self.enhance_image_by_parts(image)
        return image
