import math
from sympy import Point, Line, Circle, intersection, Ray, pi
from sympy import plot_implicit, cos, sin, symbols, Eq, And
from sympy import symbols
from sympy.plotting import plot
import matplotlib.pyplot as plt
import numpy as np
#import ball_detection as detection

pathBallW = []   # contains the rays which the cue ball will follow
pathBallN = []   # contains the lines which the normal ball will follow
RADIUS = 5


def path_of_white_ball_after_collision(m, c, r):
    pass
    

def plot_graph(point_inter, circle_centre, point_stick):
    white_ball_centre = Point(float(2 * point_inter.x - circle_centre.x), float(2 * point_inter.y - circle_centre.y))
    
    x = np.linspace(-30, 25, 10)

    circle1 = plt.Circle((circle_centre.x,circle_centre.y), RADIUS, color='r')
    circle2 = plt.Circle((point_stick.x, point_stick.y), RADIUS, color='black')
    circle3 = plt.Circle((white_ball_centre.x, white_ball_centre.y), RADIUS, color='grey')

    fig, ax = plt.subplots()
    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(circle3)
 
    x = np.linspace(-30, 25, 10)
    y = pathBallW[0].slope*x + (pathBallW[0].p1.y - pathBallW[0].slope*pathBallW[0].p1.x)
    plt.plot(x, y, 'b')
    y = pathBallW[2].slope*x + (pathBallW[2].p1.y - pathBallW[2].slope*pathBallW[2].p1.x)
    plt.plot(x, y, 'b')

    path_of_white_ball(circle_centre, point_inter, RADIUS)
    
    plt.axis("equal")
    plt.title('Graph')
    plt.xlabel('x', color='#1C2833')
    plt.ylabel('y', color='#1C2833')
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()


def path_of_white_ball(p1, p2, r):
    pathBallW[:] = []
    middle_ray = Ray(p1, p2).rotate(pi)
    cue_circle = Circle(p1, r)
    normal_line = middle_ray.perpendicular_line(p1)
    points = intersection(cue_circle, normal_line)
    pathBallW.append(middle_ray.parallel_line(points[0]))
    pathBallW.append(middle_ray)
    pathBallW.append(middle_ray.parallel_line(points[1]))

def plot_white_ball_path():
    x = np.linspace(-30, 25, 10)
    y = pathBallW[0].slope*x + (pathBallW[0].p1.y - pathBallW[0].slope*pathBallW[0].p1.x)
    plt.plot(x, y, 'b')
    y = pathBallW[2].slope*x + (pathBallW[2].p1.y - pathBallW[2].slope*pathBallW[2].p1.x)
    plt.plot(x, y, 'b')
    plt.axis("equal")
    plt.title('Graph')
    plt.xlabel('x', color='#1C2833')
    plt.ylabel('y', color='#1C2833')
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()
    

def find_collision_point(cue_point, ball_point, radius):
    point_collision = cue_point
    slope_line = pathBallW[1].slope
    white_ball_ray = pathBallW[1]
    white_ball_line = Line(cue_point, slope=slope_line)
    coeff = white_ball_line.coefficients
    ball_circle = Circle(ball_point, radius)
    point1 = cue_point
    point2 = intersection(white_ball_line.perpendicular_line(cue_point), Line(ball_point, slope=slope_line))[0]
    while 1:
        mid_point = Point((point1.x+point2.x)/2, (point1.y+point2.y)/2)
        mid_line = Line(mid_point, slope=slope_line)
        intersect_point = intersection(mid_line, ball_circle)
        if len(intersect_point) == 2 and cue_point.distance(intersect_point[0]) >= cue_point.distance(intersect_point[1]):
            point_collision = intersect_point[1]
        elif len(intersect_point) == 2 or len(intersect_point) == 1:
            point_collision = intersect_point[0]
        else:
            break

        point_extended = Point(float(2*point_collision.x - ball_point.x), float(2 * point_collision.y - ball_point.y))
        if white_ball_ray.contains(point_extended):
            break
        else:
            val_point_extended = coeff[0]*point_extended.x + coeff[1]*point_extended.y + coeff[2]
            val_mid_point = coeff[0]*mid_point.x + coeff[1]*mid_point.y + coeff[2]
            if (val_mid_point < 0 and val_point_extended < 0) or (val_mid_point > 0 and val_point_extended > 0):
                point1 = mid_point
            else:
                point2 = mid_point
        if point1 == point2:
            break
        print(point_collision)
    return point_collision


def ball_collide_first(cue_point, ball_coord):
    min_distance = 1e9
    first_ball = cue_point
    for coord in ball_coord:
        ball_circle = Circle(Point(coord[0], coord[1]), coord[2])
        if len(intersection(pathBallW[0], ball_circle)) >= 1 or len(intersection(pathBallW[2], ball_circle)) >= 1:
            d = cue_point.distance(ball_circle.center)
            if min_distance > d:
                min_distance = d
                first_ball = Point(coord[0], coord[1])
    return first_ball


def main():
    image_address = '3.png'
    ball_coord, cue_coord, stick_coord = detection.detect_coordinates(image_address)
    print(ball_coord, cue_coord, stick_coord)
    if len(cue_coord) == 0 or len(stick_coord) == 0:
        print("No point detected")
        return

    cue_point = Point(cue_coord[0], cue_coord[1])
    stick_point = Point(stick_coord[0], stick_coord[1])
    path_of_white_ball(cue_point, stick_coord, cue_coord[2])
    #path_of_white_ball(p1, p2, RADIUS)
    first_ball = ball_collide_first(cue_point, ball_coord)
    if first_ball == cue_point:
        print("No collision")
        return


def test():
    p1 = Point(25, 0)                    # White ball centre
    p2 = Point(30, 0)                     # Point from cue stick
    ball_coord = []
    ball_coord.append([0,-8,5])          # Ball which lies in the path
    path_of_white_ball(p1, p2, RADIUS)
    first_ball = ball_collide_first(p1, ball_coord)
    if first_ball == p1:
        print("No collision")
    else:
        point_collision = find_collision_point(p1,first_ball,RADIUS)
        print(point_collision)
        #plot_white_ball_path()
        plot_graph(point_collision, first_ball, p1)



if __name__ == '__main__':
    test()
    #main()



