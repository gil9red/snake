from random import randrange

from OpenGL.GL import *
from OpenGL.GLUT import *


__author__ = 'ipetrash'

width, height = 400, 400  # window size
field_width, field_height = 50, 50  # internal resolution
interval = 300  # update interval in milliseconds


def refresh2d_custom(width, height, internal_width, internal_height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, internal_width, 0.0, internal_height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)  # start drawing a rectangle
    glVertex2f(x, y)  # bottom left point
    glVertex2f(x + width, y)  # bottom right point
    glVertex2f(x + width, y + height)  # top right point
    glVertex2f(x, y + height)  # top left point
    glEnd()  # done drawing a rectangle


snake = [(20, 20)]  # snake list of (x, y) positions
snake_dir = (1, 0)  # snake movement direction

food = []  # food list of type (x, y)


def draw_snake():
    glColor3f(0.0, 1.0, 0.0)  # set color to white
    for x, y in snake:  # go through each (x, y) entry
        draw_rect(x, y, 1, 1)  # draw it at (x, y) with width=1 and height=1


def draw_food():
    glColor3f(0.5, 0.5, 1.0)  # set color to blue
    for x, y in food:  # go through each (x, y) entry
        draw_rect(x, y, 1, 1)  # draw it at (x, y) with width=1 and height=1


def draw():  # draw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
    glLoadIdentity()  # reset position
    refresh2d_custom(width, height, field_width, field_height)

    draw_food()  # draw the food
    draw_snake()  # draw the snake

    glutSwapBuffers()  # important for double buffering


def vec_add(x1, y1, x2, y2):
    return x1 + x2, y1 + y2


def update(value):
    hx, hy = snake[0]  # get the snake's head x and y position
    vx, vy = snake_dir
    snake.insert(0, vec_add(hx, hy, vx, vy))  # insert new position in the beginning of the snake list
    snake.pop()  # remove the last element

    # spawn food with 20% chance
    if randrange(5) == 0:
        x, y = randrange(field_width), randrange(field_height)  # random spawn pos
        food.append((x, y))

    # let the snake eat the food
    for x, y in food:  # go through the food list
        if hx == x and hy == y:  # is the head where the food is?
            snake.append((x, y))  # make the snake longer
            food.remove((x, y))  # remove the food

    glutTimerFunc(interval, update, 0)  # trigger next update


def keyboard(*args):
    global snake_dir  # important if we want to set it to a new value

    key = args[0]
    if key == GLUT_KEY_LEFT:
        snake_dir = -1, 0  # left

    elif key == GLUT_KEY_UP:
        snake_dir = 0, 1  # up

    elif key == GLUT_KEY_RIGHT:
        snake_dir = 1, 0  # right

    elif key == GLUT_KEY_DOWN:
        snake_dir = 0, -1  # down


if __name__ == '__main__':
    # initialization
    glutInit()  # initialize glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)  # set window size
    glutCreateWindow(b"snake")  # create window with title
    glutDisplayFunc(draw)  # set draw function callback
    glutIdleFunc(draw)  # draw all the time
    glutSpecialFunc(keyboard)  # tell opengl that we want to check keys
    glutTimerFunc(interval, update, 0)  # trigger next update
    glutMainLoop()  # start everything