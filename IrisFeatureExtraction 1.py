import numpy as np
import scipy.signal as signal

class GaborFeatureExtractor:
    def __init__(self, kernel_size=9, block_size=8):
        self.KERNEL_SIZE = kernel_size # we define the size of the Gabor kernels to be 9
        self.BLOCK_SIZE = block_size # we defined the size the block when computing the feature vector to be 8

    def get_region_of_interest(self, image):
        return image[0:48, :] # extract the region of interest from the first 48 rows of the image
    
    def calculate_gabor_filter2(self, sigma_x, sigma_y): # to create the Gabor filter
        def g2(x, y, sigma_x, sigma_y): # one of the Gaussian functions in the Gabor filter
            def m2(x, y, sigma_y): # the other Gaussian function in the Gabor filter
                minus_sigma_y = 1 / sigma_y # defines the frequency of the sinusoidal component of the Gabor filter, which is 1/sigma_y
                return np.cos(2 * np.pi * minus_sigma_y *(x*np.cos(np.pi/4)+y*np.sin(np.pi/4))) # creates the sinusoidal component of the Gabor filter
            return (1 / (2 * np.pi * sigma_x * sigma_y) * np.exp(-(x**2 / sigma_x**2 + y**2 / sigma_y**2) / 2) * m2(x, y, sigma_y)) # the gabor function that multiplies Gaussian envelope and sinusoidal component, created by m2
        
        kernel = np.zeros((self.KERNEL_SIZE, self.KERNEL_SIZE)) # creates a 9*9 matrix of zeros, our kernel
        
        for row in range(self.KERNEL_SIZE): # loop over each row and column of the kernel
            for col in range(self.KERNEL_SIZE):
                kernel[row, col] = g2((col - 4), (row - 4), sigma_x, sigma_y) # assign the value of the Gabor filter to each element of our defined kernel
        return kernel

    def calculate_gabor_filter(self, sigma_x, sigma_y): # to create the Gabor filter, but with a different sinusoidal component g1,m1
        def g1(x, y, sigma_x, sigma_y): # one of the Gaussian functions in the Gabor filter
            def m1(x, y, sigma_y): # the other Gaussian function in the Gabor filter, different from m2, that calculates the distance from the center of the kernel
                minus_sigma_y = 1 / sigma_y # defines the frequency of the sinusoidal component of the Gabor filter, which is 1/sigma_y
                return np.cos(2 * np.pi * minus_sigma_y * np.sqrt(x**2 + y**2)) # creates another sinusoidal component of the Gabor filter that calculates the distance from the center of the kernel
            return (1 / (2 * np.pi * sigma_x * sigma_y) * np.exp(-(x**2 / sigma_x**2 + y**2 / sigma_y**2) / 2) * m1(x, y, sigma_y)) # the gabor function that multiplies Gaussian envelope and sinusoidal component, created by m2        
        
        kernel = np.zeros((self.KERNEL_SIZE, self.KERNEL_SIZE)) # creates a 9*9 matrix of zeros, our kernel
        
        for row in range(self.KERNEL_SIZE): # loop over each row and column of the kernel
            for col in range(self.KERNEL_SIZE):
                kernel[row, col] = g1((col - 4), (row - 4), sigma_x, sigma_y) # assign the value of the Gabor filter to each element of our defined kernel
        return kernel

    def filter_image(self, image, sigma_x, sigma_y): # to create a function that filters the image with the Gabor filter
        image = self.get_region_of_interest(image) # extract the region of interest from the first 48 rows of the image
        this_kernel = self.calculate_gabor_filter(sigma_x, sigma_y) # create the Gabor filter
        new_image = signal.convolve2d(image, this_kernel, mode='same') # convolve the image with the Gabor filter, we set the mode to 'same' so as to keep the size of the output image the same as the input image
        return new_image
    
    def filter_image2(self, image, sigma_x, sigma_y): # to create a function that filters the image with the Gabor filter, but with a different sinusoidal component g1,m1
        image = self.get_region_of_interest(image) # extract the region of interest from the first 48 rows of the image
        this_kernel = self.calculate_gabor_filter2(sigma_x, sigma_y) # create the Gabor filter, with function g2,m2
        new_image = signal.convolve2d(image, this_kernel, mode='same') # convolve the image with the new Gabor filter, we set the mode to 'same' so as to keep the size of the output image the same as the input image
        return new_image


    def get_feature_vector(self, f1, f2): # to create a function that calculates the feature vector from two filtered images f1 and f2
        n_rows = int(f1.shape[0] / self.BLOCK_SIZE) # define the number of rows and columns for 8*8 blocks in the image
        n_cols = int(f1.shape[1] / self.BLOCK_SIZE)
        vec = np.zeros(n_rows * n_cols * 2 * 2) # create a vector of zeros with the size of number of blocks
        for i in range(2): # loop over each filtered image
            image = [f1, f2][i] # define our current image
            for row in range(n_rows): # loop over each block
                for col in range(n_cols): 
                    mean_value = np.mean(np.abs(image[row * self.BLOCK_SIZE: (row + 1) * self.BLOCK_SIZE, col * self.BLOCK_SIZE: (col + 1) * self.BLOCK_SIZE])) # calculate the mean value of the block
                    sd_value = np.sum(abs(image[row * self.BLOCK_SIZE: (row + 1) * self.BLOCK_SIZE, col * self.BLOCK_SIZE: (col + 1) * self.BLOCK_SIZE] - mean_value)) / (self.BLOCK_SIZE * self.BLOCK_SIZE) # calculate the standard deviation of the block from the mean value
                    vec[i * (n_rows * n_cols * 2) + 2 * (row * n_cols) + 2 * col] = mean_value # assign the mean value to the current vector
                    vec[i * (n_rows * n_cols * 2) + 2 * (row * n_cols) + 2 * col + 1] = sd_value # assign the standard deviation to the current vector
        return vec


