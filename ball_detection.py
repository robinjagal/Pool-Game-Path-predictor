from cv2 import cv2 as cv
import numpy as np
import math


def nothing(x):
    pass


def detect_coordinates(image_address):
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


def main():
    image_address = 'pool_table_edited.png'
    coordinates = detect_coordinates(image_address)
    print(coordinates)


if __name__ == '__main__':
    main()