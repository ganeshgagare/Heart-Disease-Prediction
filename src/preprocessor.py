import cv2
import numpy as np
from PIL import Image

class ECGPreprocessor:
    @staticmethod
    def preprocess_image(image):
        """
        Preprocess ECG image for feature extraction
        Args:
            image (PIL.Image): Input ECG image
        Returns:
            np.array: Preprocessed image
        """
        # Convert PIL Image to numpy array
        img_array = np.array(image)
        
        # Convert to grayscale
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
            
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Noise removal
        kernel = np.ones((3,3), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        return cleaned
