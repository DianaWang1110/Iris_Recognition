
# Iris Recognition System

This repository contains the implementation of an Iris Recognition System developed as part of a project at Columbia University. The system uses a multi-stage pipeline to accurately process and identify iris patterns in eye images.

## Project Overview

The system processes high-resolution images in the following stages:

1. **Iris Localization**: Detects the iris and pupil boundaries using the Hough Transform and gradient methods.
2. **Iris Normalization**: Converts the localized iris region into a consistent polar representation.
3. **Feature Extraction**: Extracts textural features from the iris using Gabor filters and wavelet transforms.
4. **Template Matching**: Matches the extracted features against a pre-enrolled database using the Hamming distance.

## Key Components

### 1. Iris Localization
- Detects the iris using `HoughCircles` and gradient-based techniques.
- The function applies `medianBlur` to reduce noise and Hough Transform to detect circles representing the pupil and iris.

### 2. Iris Normalization
- Unwraps the Cartesian coordinates of the iris into a polar system for consistent size and shape representation.
- Converts each pixel in the iris region into pseudo-polar coordinates using predefined equations.

### 3. Feature Extraction
- Utilizes Gabor filters to capture the unique textural information of the iris.
- Divides the iris image into blocks and applies dual Gabor filters, extracting statistical measures like mean and standard deviation from the filtered blocks.

### 4. Template Matching
- Uses dimensional reduction (Fisher’s Linear Discriminant) to optimize the feature space.
- Classifies iris templates by comparing them to the closest class mean using a nearest centroid approach with distance metrics such as cosine similarity, L1, and L2 norms.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/IrisRecognitionSystem.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Iris Localization**: Run the iris localization script to detect and localize the iris within an eye image.
   ```bash
   python IrisLocalization.py
   ```

2. **Iris Normalization**: Normalize the localized iris to a polar coordinate system.
   ```bash
   python IrisNormalization.py
   ```

3. **Feature Extraction**: Extract the features from the normalized iris using Gabor filters.
   ```bash
   python IrisFeatureExtraction.py
   ```

4. **Iris Matching**: Perform template matching by comparing extracted features with pre-enrolled templates.
   ```bash
   python IrisMatching.py
   ```
