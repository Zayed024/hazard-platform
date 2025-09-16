# backend/app/ai/image_analyzer.py

import cv2
import numpy as np

def analyze_report_image(image_bytes: bytes) -> float:
    """
    Analyzes an image for blurriness to contribute to a trust score.
    A higher score indicates a clearer image.
    Returns a score between 0.0 (very blurry) and 1.0 (very clear).
    """
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        # Convert the byte array to an OpenCV image
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            return 0.0

        # Calculate the Laplacian variance
        laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
        
        # Normalize the score. Thresholds can be tuned.
        # A variance > 100 is generally considered not blurry.
        # We will cap the score at a variance of 500 for normalization.
        score = min(laplacian_var / 500.0, 1.0)
        
        return score
    except Exception:
        return 0.2 # Default low score if image processing fails