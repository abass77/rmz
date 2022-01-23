#Module to flatten document on the screen

import numpy as np
import cv2

def order_points(points):
    
    #Initializing array for document vertices
    rectangle = np.zeros((4, 2), dtype = "float32")
    
    #Finding documnet vertices in order of (tl, tr, br, bl) where t = top, l = left and so on
    col_wise_sum = points.sum(axis = 1)
    rectangle[0] = points[np.argmin(col_wise_sum)]
    rectangle[2] = points[np.argmax(col_wise_sum)]
    
    col_wise_diff = np.diff(points, axis = 1)
    rectangle[1] = points[np.argmin(col_wise_diff)]
    rectangle[3] = points[np.argmax(col_wise_diff)]
    
    return rectangle

def doc_perspective_transform(image, points):
    
    doc_bounding_rect = order_points(points)
    (tl, tr, br, bl) = doc_bounding_rect
    
    #Computing top and bottom widths
    width_top = np.linalg.norm(tr - tl)
    width_bottom = np.linalg.norm(br - bl)
    max_width = int(max(width_top, width_bottom))
    
    #Computing left and right heights
    height_left = np.linalg.norm(tl - bl)
    height_right = np.linalg.norm(tr - br)
    max_height = int(max(height_left, height_right))
    
    #New coordinates for document
    new_coords = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
        ], dtype = "float32")
    
    #Applying transformation matrix to change document according to new coordinates
    transform_matrix = cv2.getPerspectiveTransform(doc_bounding_rect, new_coords)
    warped_image = cv2.warpPerspective(image, transform_matrix, (max_width, max_height))
    
    return warped_image
    