import math
from sympy import Point, Line, Circle, intersection, Ray, pi
from sympy import plot_implicit, cos, sin, symbols, Eq, And
from sympy import symbols
from sympy.plotting import plot
import matplotlib.pyplot as plt
import numpy as np
import ball_detection as detection

pathBallW = []   # contains the lines which the cue ball will follow
pathBallN = []   # contains the lines which the normal ball will follow
RADIUS = 5

class myline:
    def __init__(self, slope, y_intercept):
        self.m = float(slope)
        self.c = float(y_intercept)

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def path_of_white_ball_after_collision(m, c, r):
    var = r * (math.sqrt(1 + (m*m)))
    c1 = c + var
    c2 = c - var
    pathBallW.append(myline(m, c1))
    print("New lines are\ny = %.2fx + %.2f" % (m, c1))
    pathBallW.append(myline(m, c))
    print("y = %.2fx + %.2f" % (m, c))
    pathBallW.append(myline(m, c2))
    print("y = %.2fx + %.2f" % (m, c2))

def plot_graph(point_inter, circle_centre, point_stick):
    l1 = Line(Point(1, pathBallW[0].m + pathBallW[0].c), Point(0, pathBallW[0].c))
    l2 = Line(Point(1, pathBallW[2].m + pathBallW[2].c), Point(0, pathBallW[2].c))

    white_ball_centre = Point(float(2 * point_inter.x - circle_centre.x), float(2 * point_inter.y - circle_centre.y))
    '''p = intersection(Line(Point(1, pathBallW[1].m + pathBallW[1].c), Point(0, pathBallW[1].c)), Circle(point_inter, 4))
    
    if distance_bw_points(p[0],point_stick) < distance_bw_points(p[1],point_stick):
        white_ball_centre = p[0]
    else:
        white_ball_centre = p[1]
    '''
    #t = intersection(Line(Point(0, pathBallW[1].c), slope=pathBallW[1].m), Line(circle_centre, slope=pathBallN[0].m))
    #white_ball_centre = t[0]
    x = np.linspace(-30, 25, 10)

    circle1 = plt.Circle((circle_centre.x,circle_centre.y), RADIUS, color='r')
    circle2 = plt.Circle((point_stick.x, point_stick.y), RADIUS, color='black')
    circle3 = plt.Circle((white_ball_centre.x, white_ball_centre.y), RADIUS, color='grey')

    fig, ax = plt.subplots()
    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(circle3)

    y = pathBallW[0].m*x + pathBallW[0].c
    plt.plot(x, y, 'b')
    y = pathBallW[2].m*x + pathBallW[2].c
    plt.plot(x, y, 'b')
    y = pathBallN[0].m*x + pathBallN[0].c
    plt.plot(x, y, 'r')

    pathBallW[:] = []

    if pathBallN[0].m == 0:
        m = float('inf')
    else:
        m = float(-1/pathBallN[0].m)
    c = float(white_ball_centre.y - m*white_ball_centre.x)

    path_of_white_ball_after_collision(m, c, RADIUS)

    plt.axis("equal")
    plt.title('Graph')
    plt.xlabel('x', color='#1C2833')
    plt.ylabel('y', color='#1C2833')
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()


def path_of_white_ball(p1, p2, r):
    if p2.x == p1.x:
        m = float('inf')
    else:
        m = float((p2.y - p1.y)/(p2.x - p1.x))
    normal_slope = -1/m
    cue_circle = Circle(p1, r)
    normal_line = Line(p1, slope=normal_slope)
    points = intersection(cue_circle, normal_line)
    middle_ray = Ray(p1, p2).rotate(pi)
    pathBallW.append(middle_ray.parallel_line(points[0]))
    pathBallW.append(middle_ray)
    pathBallW.append(middle_ray.parallel_line(points[1]))

def calculate_new_path(point_collision, ball_centre):
    if point_collision.y == ball_centre.y:
        slope_new_direction = float('inf')
    else:
        slope_new_direction = float((point_collision.y - ball_centre.y)/(1.0*(point_collision.x - ball_centre.x)))
    new_path = myline(slope_new_direction, ball_centre.y - slope_new_direction * ball_centre.x)
    pathBallN.append(new_path)

def find_collision_point(cue_point, ball_point, radius):
    point_collision = cue_point
    slope_line = pathBallW[1].slope
    white_ball_ray = pathBallW[1]
    white_ball_line = Line(cue_point, slope=slope_line)
    coeff = white_ball_line.coefficients
    ball_circle = Circle(ball_point, radius)
    point1 = cue_point
    point2 = intersection(white_ball_ray.perpendicular_line(cue_point), Line(ball_point, slope=slope_line))
    while point1 != point2:
        mid_point = Point((point1.x+point2.x)/2, (point1.y+point2.y)/2)
        mid_line = Line(mid_point, slope_line)
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
                point2 = mid_point
            else:
                point1 = mid_point
    return point_collision


def ball_collide_first(cue_point, ball_coord):
    min_distance = 1e9
    first_ball = cue_point
    for coord in ball_coord:
        ball_circle = Circle(Point(coord[0], coord[1]), coord[2])
        if len(intersection(pathBallW[0], ball_circle)) >= 1 or len(intersection(pathBallW[2], ball_circle)) >= 1:
            d = cue_point.distance(ball_circle)
            if min_distance > d:
                min_distance = d
                first_ball = ball_circle
    return first_ball

p1 = Point(12, 0)                    # White ball centre
p2 = Point(6, 7)                     # Point from cue stick

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


if __name__ == '__main__':
    main()


p1 = Point(12, 0)                    # White ball centre
p2 = Point(6, 7)                     # Point from cue stick
ball_centre = Point(-8, 18)          # Ball which lies in the path
path_of_white_ball(p1, p2, RADIUS)
#collision_using_binary(ball_centre, p1)


