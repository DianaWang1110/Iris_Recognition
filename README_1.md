# bl2940 yw3928 IrisRecognition System

# Overview

Boyan Luo(bl2940) Yixuan Wang(yw3928)

# Design Logic

The system is designed with a multi-stage pipeline that ensures the accurate capture, processing, and matching of iris patterns. The workflow is as follows:

1. **Iris Capture** : High-resolution images are captured under controlled illumination to minimize noise.
2. **Iris Localization** : Employing Hough Transform and gradient methods to locate the iris boundaries within the eye image.
3. **Iris Normalization** : Adjusting the localized iris region to a dimensionally consistent polar representation.
4. **Feature Extraction** : Utilizing Gabor filters and wavelet transforms to extract distinctive features from the normalized iris pattern.
5. **Template Matching** : Comparing the feature set against a pre-enrolled database using Hamming distance for identification.

# Logic of the Code

## IrisLocalization

The function, detect_pupil_and_iris, aims to take an image (bmp file) as input and detects the pupil and iris using HoughCircles. Firsty, we employ medianBlur to reduce small dots. Next by using HoughCircles, we first detect the pupil out: minDist = 100 as we want the minimum distance between the two circles to be big; param1 = 100 defines the threshold for edge detection and is suitable for our samples; param2 = 1 defines our tolerance for incorrectly-detected circles. minRadius and maxRadius for the detected circles is specified for their sizes. To create the circle of iris, we simply add an iris_constant to detected pupil, the coordinates we have already transformed into integers.


## IrisNormalization

Using input of the Cartesian coordinates of pupil and iris, our goal for iris_normalization would be to unwrap every single x,y coordinate in the Cartesian system into a new pseudopolar coordinate. We are designing a function to do the above pixel by pixel. Defined as in the article, the new size is set to be 64*512. We calculate the theta in current direction as theta = 2 * np.pi * X / N, where N = 512. Calculating the radius from the center of pupil to the boundary of iris, we get the coordinates of inner and outer circles in Cartesian coordinates based on the equations in the article. To ensure our x,y doesn't go out of index, we also define the limit of x and y based on our input image.


## IrisEnhancement

Although Ma's article suggests using subtract_background before enhance_image, we find that it would be helpful in improving accuracte ratio that we enhance the image without subtracting from background. We do this by designing the function perform_all_enhancements that takes an image and applying histogram equalization in a block-wise fashion. It divides the image into 32x32 pixel blocks. Then the function creates a copy of the original image and for each block, it extracts the block and converts it to 8-bit integer format if it isn't already, and then applies histogram equalization to that block. After this, we then replace this bloack back to the original input image. This eventually completes the purpose of features.py.


## IrisFeatureExtraction

In image processing, texture plays a pivotal role, and Gabor filters are renowned for their efficacy in this domain. We employ these filters in the GaborFeatureExtractor to capture textural information from images. The process involves isolating a region of interest, typically the upper segment of the image, and then convolving it with Gabor kernels. These kernels are engineered to highlight specific frequency and orientation details within the image, effectively capturing the essential textures.

The crux of our method lies in applying not one, but two distinct Gabor filters to the image. This dual-filter approach is designed to extract a broader range of textural features. Post filtering, we partition the image into manageable blocks and calculate statistical measures - mean and standard deviation. These measures, computed from the absolute responses of the filtered blocks, constitute the feature vector, a succinct yet descriptive representation of the image's texture. This vector becomes the cornerstone of subsequent image analysis tasks, facilitating a nuanced understanding of the image's textural landscape.


## IrisMatching

Our goal in this classification process is to intuitively group test data by proximity to the most representative point of each category—the centroid. We adopt a dimensional reduction strategy, using Fisher's Linear Discriminant, to optimize our data's feature space down to 107 dimensions. This facilitates a more focused analysis by reducing noise and computational complexity while preserving class-discriminatory information.

Once our feature space is optimized, we implement a nearest centroid classification mechanism. This involves mapping out the mean vectors, or centroids, of each class within the training dataset. Our test samples are then compared to these centroids using a chosen distance metric—cosine similarity, or L1, or L2 norms. The test samples are classified according to the closest centroid in this feature space.

In essence, we are simplifying the multidimensional data landscape into a more manageable form, and then classifying test samples based on the simplest of heuristics: which class mean they are closest to, in the reduced-dimension space. This blend of dimensionality reduction and proximity-based classification embodies a straightforward yet effective approach to pattern recognition.


## IrisPerformanceEvaluation



## IrisRecognition




# Limitations and Improvements

Current limitations of the UNI_UNI2_UNI3 Iris Recognition System include:

* **Sensitivity to Occlusion** : Partial eyelid or eyelash occlusion can affect accuracy. Future improvements could include deep learning models trained on occluded images to improve robustness.
* **Illumination Variance** : Performance can degrade under less controlled lighting conditions. Adaptive image pre-processing techniques could be integrated to mitigate this issue.

### Peer Evaluation

Every team member has contributed significantly to the project:

# Peer Evaluation
## Team member 1: Yixuan Wang yw3928 (Iris Localization, Iris Normalization, Image Enhancement)
I'm writing this evaluation to capture the teamwork and progress we made, as this is the first ever programming project that is of this complexity level of programming design. I would like to say thanks for our TA Qifan, Robert and me on the close collboration and communication we had during the project. 

Self-Reflection in Relation to Peer Performance
Learning from Peer
I've learned a lot from this project with Robert. I would like to learn from his methodical way of thinking about code – as part of a bigger picture rather than a pile of files. Never experienced in other programming courses, keeping a close eye on each output of every single bmp file taught me that in computer vision individuals differences plays a very important role in the final result.

Complementary Skills
I am in charge of the specifics of iris detection, normalization and enhancement. Turning complex equations into workable code is an interesting project to me,  which is very important in image preprocessing in our project. 

Team Dynamics
Collaboration and Communication
Our teamwork was very important when trying to enhance the accuracy rate. It took a lot of back-and-forth, sending code snippets, and brainstorming sessions that went on for days. I also gained a lesson in the power of two minds working towards a common goal.

Conclusion
Summary of Reflection
This peer evaluation has been a self-reflection for me. It's shown me how important it is to think ahead, design before jump right in coding. This is as significant as teamwork and mentorship, which gave me direction at each crossing road.

Final Thanks
I would like to also say thanks to our TA Qifan who gives us a lot of help when we face problems in localizing the iris. 

* **Team Member 2** : Took charge of **Iris Normalization** - implemented the process of transforming the iris region to a standardized format that facilitates further analysis.
