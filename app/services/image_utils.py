import cv2
import numpy as np

def detect_rotation(img) -> float:
    """
    Detects the rotation angle of a text block in an image.
    Returns the angle to rotate the image by to make it horizontal.
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return 0.0

    main_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(main_contour)
    (center, size, angle) = rect

    # Normalization for deskewing
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        
    return angle

def rotate_image(img, angle: float):
    """
    Rotates the image by the given angle.
    """
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # Using white border for text images
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    return rotated

def deskew(img):
    """
    Detects rotation and rotates the image to correct it.
    """
    angle = detect_rotation(img)
    if abs(angle) < 0.1:
        return img
    return rotate_image(img, angle)