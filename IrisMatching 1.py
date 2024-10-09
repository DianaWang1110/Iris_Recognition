import cv2
import os 
import scipy
from tqdm import trange
import numpy as np
from sklearn.neighbors._nearest_centroid import NearestCentroid
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

def fishers_linear_discriminant(X, y): # to create a function that performs Fisher's Linear Discriminant to our data
    LDADimention = 107 # define the number of dimensions we want to reduce our data to, which is 107 less than the number of data points
    clf = LDA(n_components = LDADimention) # create a Linear Discriminant Analysis object, based on the number of dimensions we want to reduce our data to, 107 dimensions
    clf.fit(X,y) # fit the data X to the Linear Discriminant Analysis object y, which will help us identify the best projection vector
    return clf


def nearest_center_classifier(training_data, training_labels, test_data,distance_type="cosine"): # to create a function that performs nearest center classifier to our data
    """
    Nearest center classifier.

    Parameters:
    training_data -- training data reduced to lower dimensions.
    training_labels -- corresponding labels for the training data.
    test_data -- test data reduced to lower dimensions.

    Returns:
    predictions -- predicted labels for the test data.
    """
    classes = np.unique(training_labels) # define the unique classes of the training data
    centroids = np.array([np.mean(training_data[training_labels == c], axis=0) for c in classes]) # calculate the mean vectir of each class in the reduced training data
    predictions = [] # create an empty list to store the predicted labels for the test data

    if distance_type == "cosine": # we calculate the cosine similarity between the test data and the mean vector of each class, the centroid 
        for sample in test_data:
            cosine_similarities = [np.dot(sample, centroid) / (np.linalg.norm(sample) * np.linalg.norm(centroid)) for centroid in centroids] 
            predictions.append(classes[np.argmax(cosine_similarities)]) # we append the class with the highest cosine similarity to the test data to the list 

    elif distance_type == "l2": # we calculate the L2 distance between the test data and the mean vector of each class, the centroid
        for sample in test_data:
            l2_distances = [np.linalg.norm(sample - centroid) for centroid in centroids]
            predictions.append(classes[np.argmin(l2_distances)]) # we append the class with the lowest L2 distance to the test data to the list

    elif distance_type == "l1": # we calculate the L1 distance between the test data and the mean vector of each class, the centroid
        for sample in test_data:
            l1_distances = [np.linalg.norm(sample - centroid, ord=1) for centroid in centroids]
            predictions.append(classes[np.argmin(l1_distances)]) # we append the class with the lowest L1 distance to the test data to the list

    return predictions

