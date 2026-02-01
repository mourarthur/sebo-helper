import cv2
import numpy as np
import pytest
from app.services.image_utils import detect_rotation, rotate_image, deskew

def create_test_image(angle, size=(200, 200)):
    # Create a white image
    img = np.ones((size[1], size[0], 3), dtype=np.uint8) * 255
    # Draw a black rectangle (simulating a text block)
    rect_center = (size[0] // 2, size[1] // 2)
    rect_size = (100, 30)
    
    # Create the rotated rectangle
    rect = (rect_center, rect_size, angle)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    
    cv2.drawContours(img, [box], 0, (0, 0, 0), -1)
    return img

def test_detect_rotation_zero():
    img = create_test_image(0)
    angle = detect_rotation(img)
    # Allow small margin
    assert abs(angle) < 1.0

def test_detect_rotation_positive():
    # 20 degrees
    img = create_test_image(20)
    angle = detect_rotation(img)
    # minAreaRect angle can be tricky depending on width/height
    # We expect something around 20 or related
    assert 15 < abs(angle) < 25

def test_detect_rotation_negative():
    # -30 degrees
    img = create_test_image(-30)
    angle = detect_rotation(img)
    assert 25 < abs(angle) < 35

def test_rotate_image():
    img = create_test_image(0)
    # Rotating 45 degrees should change the image
    rotated = rotate_image(img, 45)
    assert not np.array_equal(img, rotated)
