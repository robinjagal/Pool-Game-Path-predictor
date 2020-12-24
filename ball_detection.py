from cv2 import cv2 as cv
import numpy as np
import math
import argparse
import math
from sympy import Point, Line, Circle, intersection, Ray, pi
from cv2 import cv2 as cv
from sympy import plot_implicit, cos, sin, symbols, Eq, And
from sympy import symbols
from sympy.plotting import plot
import matplotlib.pyplot as plt
from numba import jit, cuda

def nothing(x):
    pass
cv.namedWindow('Image',cv.WINDOW_NORMAL)
cv.resizeWindow('Image',600,600)

def during_collision(cue_point,radius, stick_point, ball_coord):
    future_point = cue_point
    collision_ball_info = cue_point
    min_distance = 1e9
    
    temp_ray = Ray(cue_point,stick_point)
    temp_Line = Line(cue_point,stick_point)
    temp_circle = Circle(cue_point,radius)
    temp_collision_points = intersection(temp_Line,temp_circle)

    if temp_ray.contains(temp_collision_points[0]):
        white_ray = Ray(cue_point,temp_collision_points[1])
    else:
        white_ray = Ray(cue_point,temp_collision_points[0])    

    for coord in ball_coord:
        enlarged_ball = Circle(Point(coord[0], coord[1]), coord[2]+radius+5)

        intersect_point = intersection(white_ray,enlarged_ball)
        
        if len(intersect_point) == 2 and cue_point.distance(intersect_point[0]) >= cue_point.distance(intersect_point[1]):
            temp_point = intersect_point[1]
        elif len(intersect_point) == 2 or len(intersect_point) == 1:
            temp_point = intersect_point[0]
        else:
            continue
        
        dist = cue_point.distance(temp_point)
        if min_distance > dist:
                min_distance = dist
                future_point = temp_point
                collision_ball_info = coord
    
    return future_point, collision_ball_info

prev_stick_point = Point(0,0)
prev_cue_point = Point(0,0)

def predict_path(circle_coordinates,cue_ball_coordinate,cue_stick_coordinate,frame):
    global prev_stick_point, prev_cue_point

    if len(cue_ball_coordinate) < 3 or len(cue_stick_coordinate) < 2:
        print("No point detected")
        cv.imshow('Image',frame)
        return

    cue_point = Point(cue_ball_coordinate[0], cue_ball_coordinate[1])
    stick_point = Point(cue_stick_coordinate[0], cue_stick_coordinate[1])

    if prev_stick_point == stick_point and cue_point == prev_cue_point:
        flag = 1
    else:
        future_point, collision_ball_info  = during_collision(cue_point, cue_ball_coordinate[2],stick_point,circle_coordinates)
        prev_stick_point = stick_point
        prev_cue_point = cue_point 
        flag = 0
    
    if flag==1 or future_point == cue_point:
        pass
    else:
        print("Collision")
        cv.circle(frame, (int(collision_ball_info[0]), int(collision_ball_info[1])), 2*int(collision_ball_info[2]), (0, 255, 255), 2)
        cv.circle(frame, (int(future_point.x), int(future_point.y)), int(cue_ball_coordinate[2]), (255, 255, 255), -1)
        temp_point = Point(collision_ball_info[0],collision_ball_info[1])
        colored_future_point = intersection(Ray(future_point,temp_point),Circle(temp_point,collision_ball_info[2]*5)) 
        cv.line(frame, (cue_point.x, cue_point.y), (future_point.x, future_point.y), (255, 255, 255), thickness=2)
        cv.line(frame, ((int)(collision_ball_info[0]), (int)(collision_ball_info[1])), ((int)(colored_future_point[0].x), (int)(colored_future_point[0].y)), (0, 255, 0), thickness=2)
    
    cv.circle(frame, (int(cue_stick_coordinate[0]), int(cue_stick_coordinate[1])), 3, (123, 55, 55), 4)
    cv.circle(frame, (int(cue_ball_coordinate[0]), int(cue_ball_coordinate[1])),int(cue_ball_coordinate[2])*2, (100, 100, 100), 2)
    cv.circle(frame, (int(cue_ball_coordinate[0]), int(cue_ball_coordinate[1])), 1, (255, 100, 100), 2)
    for coordinate in circle_coordinates:
        cv.circle(frame, (int(coordinate[0]), int(coordinate[1])), 1, (0, 255, 0), 2)
        cv.circle(frame, (int(coordinate[0]), int(coordinate[1])), 2*int(coordinate[2]), (0, 255, 255), 2)
    cv.imshow('Image',frame)



image_array = []
def detect_coordinates(image_address):
         
     cv.namedWindow('Trackbar',cv.WINDOW_NORMAL)
     cv.createTrackbar('lh', 'Trackbar', 65, 255, nothing)
     cv.createTrackbar('ls', 'Trackbar', 0, 255, nothing)
     cv.createTrackbar('lv', 'Trackbar', 0, 255, nothing)
     cv.createTrackbar('uh', 'Trackbar', 84, 255, nothing)
     cv.createTrackbar('us', 'Trackbar', 255, 255, nothing)
     cv.createTrackbar('uv', 'Trackbar', 255, 255, nothing)
     cv.createTrackbar('min_rad', 'Trackbar', 20, 100, nothing)
     cv.createTrackbar('max_rad', 'Trackbar', 27, 100, nothing)
     
     circle_coordinates = []
     cue_ball_coordinate = []
     cue_stick_coordinate = []
     cap = cv.VideoCapture(image_address)
     while(cap.isOpened()):
         circle_coordinates.clear()
         cue_ball_coordinate.clear()
         ret , frame = cap.read()
         if not ret:
             break
         
         hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
         hsv_cue = hsv.copy()
         lh = cv.getTrackbarPos('lh', 'Trackbar')
         ls = cv.getTrackbarPos('ls', 'Trackbar')
         lv = cv.getTrackbarPos('lv', 'Trackbar')
         uh = cv.getTrackbarPos('uh', 'Trackbar')
         us = cv.getTrackbarPos('us', 'Trackbar')
         uv = cv.getTrackbarPos('uv', 'Trackbar')
         
         min_rad = cv.getTrackbarPos('min_rad', 'Trackbar')
         max_rad = cv.getTrackbarPos('max_rad', 'Trackbar')
         lower_green = np.array([lh, ls, lv])
         upper_green = np.array([uh, us, uv])
         lower_white = np.array([0, 0, 168])
         upper_white = np.array([172, 111, 255])
         lower_pink = np.array([125,100,141])
         upper_pink = np.array([166,123,219])
         mask_white = cv.inRange(hsv_cue, lower_white, upper_white)
         mask = cv.inRange(hsv, lower_green, upper_green)
         #mask_table = mask.copy()
         mask = cv.bitwise_not(mask, mask=None)
         mask_stick = cv.inRange(hsv,lower_pink,upper_pink)
         contours, _ = cv.findContours(
             mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
         contours_white_ball, _ = cv.findContours(
             mask_white, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
         contours_stick, _ = cv.findContours(mask_stick,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
         #contours_table, _ = cv.findContours(mask_table,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
         #c = max(contours_table, key = cv.contourArea)
         #x,y,w,h = cv.boundingRect(c)

         #draw the biggest contour (c) in green
         #cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
         if len(contours_stick) != 0:
            c = max(contours_stick,key = cv.contourArea)
            M_stick = cv.moments(c)
            if M_stick['m00'] != 0:
                cX_stick = M_stick['m10']/M_stick['m00']
                cY_stick = M_stick['m01']/M_stick['m00']
                #cv.circle(frame, (int(cX_stick), int(cY_stick)), 3, (123, 55, 55), 4)  
                cue_stick_coordinate = [cX_stick,cY_stick]

         for contour in contours_white_ball:
             approx_white = cv.approxPolyDP(
                 contour, 0.01*cv.arcLength(contour, True), True)
             x_white = approx_white.ravel()[0]
             y_white = approx_white.ravel()[1]
             M = cv.moments(contour)
             if M['m00'] == 0:
                 continue
             cX_white = M['m10']/M['m00']
             cY_white = M['m01']/M['m00']
             
             if len(approx_white) > 8  and len(approx_white) < 23:
                 #k = cv.isContourConvex(approx_white)
                 area = cv.contourArea(contour)
                 perimeter = cv.arcLength(contour,True)
                 circularity = 4 * math.pi * (area/(perimeter*perimeter))
                 if circularity < 0.5:
                     continue
                 radius_white = math.sqrt((cX_white-x_white)**2 + (cY_white-y_white)**2)
                 if radius_white < min_rad or radius_white > max_rad:
                     continue
                 #cv.circle(frame, (int(cX_white), int(cY_white)),
                           #int(radius_white)*2, (100, 100, 100), 2)
                 #cv.circle(frame, (int(cX_white), int(cY_white)), 1, (255, 100, 100), 2)
                 cue_ball_coordinate = [cX_white, cY_white, radius_white]

         for contour in contours:
             if len(cue_ball_coordinate) != 0:
                 cX_white = cue_ball_coordinate[0]
                 cY_white = cue_ball_coordinate[1]
             approx = cv.approxPolyDP(
             contour, 0.01*cv.arcLength(contour, True), True)
             x = approx.ravel()[0]
             y = approx.ravel()[1]
             M = cv.moments(contour)
             if M['m00'] == 0:
                 continue
             cX = M['m10']/M['m00']
             cY = M['m01']/M['m00']
             
             if len(approx) > 8 and len(approx) < 23:
                 area = cv.contourArea(contour)
                 perimeter = cv.arcLength(contour,True)
                 circularity = 4 * math.pi * (area/(perimeter*perimeter))
                 if circularity < 0.5:
                     continue
                 if len(cue_ball_coordinate) != 0:
                     distance = math.sqrt((cX-cX_white)**2 + (cY-cY_white)**2)
                     if distance < min_rad:
                         continue
                 radius = math.sqrt((cX-x)**2 + (cY-y)**2)
                 if radius < min_rad or radius > max_rad:
                     continue
                 #cv.circle(frame, (int(cX), int(cY)), 1, (0, 255, 0), 2)
                 #cv.circle(frame, (int(cX), int(cY)), 2*int(radius), (0, 255, 255), 2)
                 circle_coordinates.append([cX, cY, radius])

         #cv.imshow('Image', frame)
         height,width,_ = frame.shape
         size = (width,height)
         image_array.append(frame)
         predict_path(circle_coordinates,cue_ball_coordinate,cue_stick_coordinate,frame)
         if cv.waitKey(1) & 0xFF == 27:
             break
     cap.release()
     cv.destroyAllWindows()
     out = cv.VideoWriter('outpy.avi',cv.VideoWriter_fourcc('M','J','P','G'), 10, size)
     for img in image_array:
         out.write(img)
     


def main():
    image_address = 'poolvideo1.mp4'
    detect_coordinates(image_address)
    #print(ref_point)


if __name__ == '__main__':
    main()

def detect_coordinates2(image_address):
     cv.namedWindow('Trackbar',cv.WINDOW_NORMAL)
     cv.createTrackbar('lh', 'Trackbar', 36, 255, nothing)
     cv.createTrackbar('ls', 'Trackbar', 0, 255, nothing)
     cv.createTrackbar('lv', 'Trackbar', 0, 255, nothing)
     cv.createTrackbar('uh', 'Trackbar', 86, 86, nothing)
     cv.createTrackbar('us', 'Trackbar', 255, 255, nothing)
     cv.createTrackbar('uv', 'Trackbar', 255, 255, nothing)
     cv.createTrackbar('min_rad', 'Trackbar', 5, 50, nothing)
     cv.createTrackbar('max_rad', 'Trackbar', 10, 50, nothing)
     #cv.createTrackbar('lh_s', 'Trackbar', 0, 255, nothing)
     #cv.createTrackbar('ls_s', 'Trackbar', 0, 255, nothing)
     #cv.createTrackbar('lv_s', 'Trackbar', 0, 255, nothing)
     #cv.createTrackbar('uh_s', 'Trackbar', 0, 255, nothing)
     #cv.createTrackbar('us_s', 'Trackbar', 0, 255, nothing)
     #cv.createTrackbar('uv_s', 'Trackbar', 0, 255, nothing)
     
     circle_coordinates = []
     cue_ball_coordinate = []
     cue_stick_coordinate = []

     while(True):
         circle_coordinates.clear()
         cue_ball_coordinate.clear()
         frame = cv.imread(image_address, 1)
         frame_copy = frame.copy()
         frame_copy = cv.medianBlur(frame_copy,3)
         hsv = cv.cvtColor(frame_copy, cv.COLOR_BGR2HSV)
         hsv_cue = hsv.copy()
         lh = cv.getTrackbarPos('lh', 'Trackbar')
         ls = cv.getTrackbarPos('ls', 'Trackbar')
         lv = cv.getTrackbarPos('lv', 'Trackbar')
         uh = cv.getTrackbarPos('uh', 'Trackbar')
         us = cv.getTrackbarPos('us', 'Trackbar')
         uv = cv.getTrackbarPos('uv', 'Trackbar')
         #lh_s = cv.getTrackbarPos('lh_s', 'Trackbar')
         #ls_s = cv.getTrackbarPos('ls_s', 'Trackbar')
         #lv_s = cv.getTrackbarPos('lv_s', 'Trackbar')
         #uh_s = cv.getTrackbarPos('uh_s', 'Trackbar')
         #us_s = cv.getTrackbarPos('us_s', 'Trackbar')
         #uv_s = cv.getTrackbarPos('uv_s', 'Trackbar')
         min_rad = cv.getTrackbarPos('min_rad', 'Trackbar')
         max_rad = cv.getTrackbarPos('max_rad', 'Trackbar')
         lower_green = np.array([lh, ls, lv])
         upper_green = np.array([uh, us, uv])
         lower_white = np.array([0, 0, 168])
         upper_white = np.array([172, 111, 255])
         lower_pink = np.array([125,100,186])
         upper_pink = np.array([166,123,219])
         mask_white = cv.inRange(hsv_cue, lower_white, upper_white)
         mask = cv.inRange(hsv, lower_green, upper_green)
         mask = cv.bitwise_not(mask, mask=None)
         mask_stick = cv.inRange(hsv,lower_pink,upper_pink)
         contours, _ = cv.findContours(
             mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
         contours_white_ball, _ = cv.findContours(
             mask_white, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
         contours_stick, _ = cv.findContours(mask_stick,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)

         for contour in contours_stick:
             #approx_stick = cv.approxPolyDP(
                #contour,0.01*cv.arcLength(contour,True),True)
             M_stick = cv.moments(contour)
             if M_stick['m00'] == 0:
                 continue
             cX_stick = M_stick['m10']/M_stick['m00']
             cY_stick = M_stick['m01']/M_stick['m00']
             cv.circle(frame, (int(cX_stick), int(cY_stick)), 1, (123, 55, 55), 2)
             cue_stick_coordinate = [cX_stick,cY_stick]

         for contour in contours_white_ball:
             approx_white = cv.approxPolyDP(
                 contour, 0.01*cv.arcLength(contour, True), True)
             x_white = approx_white.ravel()[0]
             y_white = approx_white.ravel()[1]
             M = cv.moments(contour)
             if M['m00'] == 0:
                 continue
             cX_white = M['m10']/M['m00']
             cY_white = M['m01']/M['m00']
             

             #if len(approx_white) == 4:
              #   _, _, w, h = cv.boundingRect(approx_white)
               #  aspectRatio = float(w)/h
                # if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                 #    cv.circle(frame, (int(cX_white), int(cY_white)), 1, (255, 0, 255), 2)
          
             if len(approx_white) > 10:
                 k = cv.isContourConvex(approx_white)
                 if k == 0:
                     continue
                 radius_white = math.sqrt((cX_white-x_white)**2 + (cY_white-y_white)**2)
                 if radius_white < min_rad or radius_white > max_rad:
                     continue
                 cv.circle(frame, (int(cX_white), int(cY_white)),
                           int(radius_white)*2, (100, 100, 100), 2)
                 cv.circle(frame, (int(cX_white), int(cY_white)), 1, (255, 100, 100), 2)
                 cue_ball_coordinate = [cX_white, cY_white, radius_white]

         for contour in contours:
             if len(cue_ball_coordinate) != 0:
                 cX_white = cue_ball_coordinate[0]
                 cY_white = cue_ball_coordinate[1]
             approx = cv.approxPolyDP(
             contour, 0.01*cv.arcLength(contour, True), True)
             x = approx.ravel()[0]
             y = approx.ravel()[1]
             M = cv.moments(contour)
             if M['m00'] == 0:
                 continue
             cX = M['m10']/M['m00']
             cY = M['m01']/M['m00']
             
             if len(approx) > 10:
                 if len(cue_ball_coordinate) != 0:
                     distance = math.sqrt((cX-cX_white)**2 + (cY-cY_white)**2)
                     if distance < min_rad:
                         continue
                 radius = math.sqrt((cX-x)**2 + (cY-y)**2)
                 if radius < min_rad or radius > max_rad:
                     continue
                 cv.circle(frame, (int(cX), int(cY)), 1, (0, 255, 0), 2)
                 cv.circle(frame, (int(cX), int(cY)), 2*int(radius), (0, 255, 255), 2)
                 circle_coordinates.append([cX, cY, radius])

         cv.imshow('Image', frame)
         cv.imshow('Imag2',mask)
         if cv.waitKey(1) & 0xFF == 27:
             break
     cv.destroyAllWindows()
     return circle_coordinates, cue_ball_coordinate, cue_stick_coordinate

