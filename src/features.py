import numpy as np
import cv2

class FeatureExtractor:
    @staticmethod
    def extract_features(preprocessed_image):
        """
        Extract relevant features from preprocessed ECG image
        Args:
            preprocessed_image (np.array): Binary preprocessed image
        Returns:
            np.array: Feature vector
        """
        features = []
        
        # Basic statistical features
        features.extend([
            np.mean(preprocessed_image),
            np.std(preprocessed_image),
            np.percentile(preprocessed_image, 25),
            np.percentile(preprocessed_image, 75)
        ])
        
        # Contour-based features
        contours, _ = cv2.findContours(
            preprocessed_image,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            features.extend([
                cv2.contourArea(largest_contour),
                cv2.arcLength(largest_contour, True)
            ])
        else:
            features.extend([0, 0])
            
        # Signal frequency features
        freq_transform = np.fft.fft2(preprocessed_image)
        features.extend([
            np.abs(freq_transform).mean(),
            np.abs(freq_transform).std(),
            np.abs(freq_transform).max()
        ])
        
        return np.array(features)
