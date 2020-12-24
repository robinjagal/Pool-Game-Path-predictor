import math
from sympy import Point, Line, Circle, intersection, Ray, pi
from cv2 import cv2 as cv
from sympy import plot_implicit, cos, sin, symbols, Eq, And
from sympy import symbols
from sympy.plotting import plot
import matplotlib.pyplot as plt
import numpy as np
import ball_detection as detection

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
        enlarged_ball = Circle(Point(coord[0], coord[1]), coord[2]+radius)

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


def 


def main():

    image_address = 'pool_Images/2.png'
    ball_coord, cue_coord, stick_coord = detection.detect_coordinates(image_address)
    #print(cue_coord, ball_coord, stick_coord)
    if len(cue_coord) == 0 or len(stick_coord) == 0:
        print("No point detected")
        return

    cue_point = Point(cue_coord[0], cue_coord[1])
    stick_point = Point(stick_coord[0], stick_coord[1])
    path_of_white_ball(cue_point, stick_coord, cue_coord[2])
    #path_of_white_ball(p1, p2, RADIUS)
    future_point, collision_ball_info  = during_collision(cue_point, cue_coord[2],stick_point,ball_coord)
    if future_point == cue_point:
        print("No collision")
        return 
    else:
        frame = cv.imread(image_address, 1)
        cv.circle(frame, (int(collision_ball_info[0]), int(collision_ball_info[1])), 2*int(collision_ball_info[2]), (0, 255, 255), 2)
        cv.circle(frame, (int(future_point.x), int(future_point.y)), int(cue_coord[2]), (255, 255, 255), -1)
        temp_point = Point(collision_ball_info[0],collision_ball_info[1])
        colored_future_point = intersection(Ray(future_point,temp_point),Circle(temp_point,collision_ball_info[2]*5)) 
        cv.line(frame, (cue_point.x, cue_point.y), (future_point.x, future_point.y), (255, 255, 255), thickness=2)
        cv.line(frame, ((int)(collision_ball_info[0]), (int)(collision_ball_info[1])), ((int)(colored_future_point[0].x), (int)(colored_future_point[0].y)), (0, 255, 0), thickness=2)
        while 1:
            cv.namedWindow('Image',cv.WND_PROP_FULLSCREEN)
            cv.imshow('Image', frame)
            if cv.waitKey(1) & 0xFF == 27:
                break
        cv.destroyAllWindows()


if __name__ == '__main__':
    main()
    #main()



