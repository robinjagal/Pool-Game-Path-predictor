import math
from sympy import Point, Line, Circle, intersection, Ray
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
    c = float(p1.y - m*p1.x)
    var = r*(math.sqrt(1+(m*m)))
    c1 = c + var
    c2 = c - var
    pathBallW.append(myline(m, c1))
    print("y = %.2fx + %.2f" % (m, c1))
    pathBallW.append(myline(m, c))
    print("y = %.2fx + %.2f" % (m, c))
    pathBallW.append(myline(m, c2))
    print("y = %.2fx + %.2f" % (m, c2))

def distance_bw_points(p1, p2):
    var1 = float(p1.x - p2.x)
    var2 = float(p1.y - p2.y)
    return math.sqrt(var1*var1 + var2*var2)

def calculate_new_path(point_collision, ball_centre):
    if point_collision.y == ball_centre.y:
        slope_new_direction = float('inf')
    else:
        slope_new_direction = float((point_collision.y - ball_centre.y)/(1.0*(point_collision.x - ball_centre.x)))
    new_path = myline(slope_new_direction, ball_centre.y - slope_new_direction * ball_centre.x)
    pathBallN.append(new_path)

def collision_using_binary(circle_centre, point_stick):
    sign = pathBallW[1].m*circle_centre.x - circle_centre.y + pathBallW[1].c
    white_ball_line = Line(Point(1, pathBallW[1].m + pathBallW[1].c), Point(0, pathBallW[1].c))
    if sign < 0:
        sign = -1
    elif sign > 0:
        sign = 1

    l = circle_centre.y - pathBallW[1].m*circle_centre.x
    r = pathBallW[1].c
    ball = Circle(circle_centre, RADIUS)
    point_collision = circle_centre
    flag = 0
    while 1:
        mid = (l+r)/2.0
        l1 = Line(Point(1, pathBallW[1].m + mid), Point(0, mid))
        pointAB = intersection(l1, ball)
        if len(pointAB) == 2 and point_stick.distance(pointAB[0]) >= point_stick.distance(pointAB[1]):
            point_collision = pointAB[1]
        elif len(pointAB) == 2 or len(pointAB) == 1:
            point_collision = pointAB[0]
        else:
            flag = 1
            print("Last valid line was ")
            print("y = x*" + str(pathBallW[1].m) + " + " + str(mid))

        point_temp = Point(float(2*point_collision.x-circle_centre.x), float(2*point_collision.y-circle_centre.y))
        if white_ball_line.distance(point_temp) == 0 or flag == 1:
            if point_collision == circle_centre:
                print("No collision")
                break
            print("Point of collision: " + str(point_collision.x) + "," + str(point_collision.y))
            calculate_new_path(point_collision, circle_centre)
            plot_graph(point_collision, circle_centre, point_stick)
            break

        var = pathBallW[1].m*point_temp.x - point_temp.y + pathBallW[1].c
        if var < 0:
            var = -1
        elif var > 0:
            var = 1

        if var == sign:
            l = point_temp.y - pathBallW[1].m*point_temp.x
        else:
            r = point_temp.y - pathBallW[1].m*point_temp.x


def ball_collide_first(cue_point, ball_coord):
    min_distance = 1e9
    first_ball = cue_point
    for coord in ball_coord:
        ball_circle = Circle(Point(coord[0], coord[1]), RADIUS)
        if len(intersection(pathBallW[0], ball_circle)) >= 1 or len(intersection(pathBallW[2], ball_circle)) >= 1:
            d = cue_point.distance(ball_circle)
            if min_distance > d:
                min_distance = d
                first_ball = ball_circle
    return first_ball


def ray_test(p1, p2, ball):
    r = Ray(p1,p2)
    c = Circle(Point(100,90), 5)
    points = intersection(r, c)
    for t in points:
        print(t)

def main():
    image_address = '3.png'
    ball_coord, cue_coord, stick_coord = detection.detect_coordinates(image_address)
    cue_point = Point(cue_coord[0], cue_coord[1])
    first_ball = ball_collide_first(cue_point, ball_coord)
    if first_ball == cue_point:
        print("No collision")
        return
    print(ball_coord, cue_coord, stick_coord)


if __name__ == '__main__':
    main()


p1 = Point(12, 0)                    # White ball centre
p2 = Point(6, 7)                     # Point from cue stick
ball_centre = Point(-8, 18)          # Ball which lies in the path
#circle_radius = 5
path_of_white_ball(p1, p2, RADIUS)
#collision_using_binary(ball_centre, p1)
ray_test(p1,p2,ball_centre)

