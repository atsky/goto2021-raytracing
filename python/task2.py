import numpy as np
from numba import jit, njit

import render_app


def vec3(x, y, z):
    return np.array([x, y, z], dtype=float)


# Функция возвращает квадрат длины вектора
def length2(x):
    return x.dot(x)


# Функция возвращает длину вектора
def length(x):
    return np.sqrt(x.dot(x))


# Функция возвращает нормализованный вектор x
def normalize(x):
    return x / length(x)


def sky_color(v):
    t = 0.5 * (v[1] + 1.0)
    return (1.0 - t) * vec3(1.0, 1.0, 1.0) + t * vec3(0.5, 0.7, 1.0)


def get_pixel_color(i, j, width, height):
    #
    x = 2.0 * i / width - 1.0
    y = 2.0 * j / height - 1.0

    origin = None
    screen_point = None
    direction = None

    return sky_color(direction)


def draw_all():
    render_app.RenderApp(get_pixel_color, 300, 200, result_file='image.png')


draw_all()
