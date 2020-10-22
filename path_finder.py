import math
from sympy import Point, Line, Circle, intersection, Ray
from sympy import plot_implicit, cos, sin, symbols, Eq, And
from sympy import symbols
from sympy.plotting import plot
import matplotlib.pyplot as plt
import numpy as np

pathBallW = []   # contains the lines which the cue ball will follow
pathBallN = []   # contains the lines which the normal ball will follow
radius = 5
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

    circle1 = plt.Circle((circle_centre.x,circle_centre.y), radius, color='r')
    circle2 = plt.Circle((point_stick.x, point_stick.y), radius, color='black')
    circle3 = plt.Circle((white_ball_centre.x, white_ball_centre.y), radius, color='grey')

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

    path_of_white_ball_after_collision(m, c, radius)

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
    ball = Circle(circle_centre, radius)
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



def ray_test(p1, p2, ball):
    r = Ray(p1,p2)
    c = Circle(Point(100,90), 5)
    points = intersection(r, c)
    for t in points:
        print(t)

p1 = Point(12, 0)                    # White ball centre
p2 = Point(6, 7)                     # Point from cue stick
ball_centre = Point(-8, 18)          # Ball which lies in the path
#circle_radius = 5
path_of_white_ball(p1, p2, radius)
#collision_using_binary(ball_centre, p1)
ray_test(p1,p2,ball_centre)

def collision_one_line(point_A, line_white, ball, circle_centre, radius):
    if pathBallW[line_white].m == 0:
        slope_circle_centre = float('inf')
    else:
        slope_circle_centre = float(-1 / (1.0*pathBallW[line_white].m))
    line_pass_centre = Line(circle_centre, slope=slope_circle_centre)
    pointAB = intersection(line_pass_centre, ball)
    if point_A.distance(pointAB[0]) <= point_A.distance(pointAB[1]):
        i = 0
    else:
        i = 1
    if pointAB[i].y == point_A.y:
        slope_new_direction = float('inf')
    else:
        slope_new_direction = float((-pointAB[i].x + point_A.x)/(1.0*(pointAB[i].y - point_A.y)))

    new_path = myline(slope_new_direction, circle_centre.y - slope_new_direction*circle_centre.x)
    pathBallN.append(new_path)
    point_inter = intersection(Line(circle_centre, slope=slope_new_direction), ball)
    if distance_bw_points(point_inter[0], point_A) <= distance_bw_points(point_inter[1], point_A):
        return point_inter[0]
    else:
        return point_inter[1]

def collision_with_ball(circle_centre, radius, point_stick):
    ball = Circle(circle_centre, radius)
    l1 = Line(Point(1, pathBallW[0].m + pathBallW[0].c), Point(0, pathBallW[0].c))
    l2 = Line(Point(1, pathBallW[2].m + pathBallW[2].c), Point(0, pathBallW[2].c))
    pointAB = intersection(l1, ball)
    pointCD = intersection(l2, ball)
    if point_stick.distance(pointAB[0]) <= point_stick.distance(pointAB[1]):
        point_inter = collision_one_line(pointAB[0], 0, ball, circle_centre, radius)
    else:
        point_inter = collision_one_line(pointAB[1], 0, ball, circle_centre, radius)

    plot_graph(point_inter, circle_centre, point_stick)