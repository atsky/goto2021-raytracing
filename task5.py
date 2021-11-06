import math

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


def hit_sphere(center, radius, origin, direction):
    pass


objects = [
    {
        'center': vec3(0, 0, -1),
        'radius': 0.5,
    },
    {
        'center': vec3(0, -100.5, -1),
        'radius': 100
    },
]


def get_nearest_intersection(direction, origin):
    min_t = np.inf
    best_result = None

    for obj in objects:
        pass

    return best_result


def get_ray(i, j, width, height):
    pass


def get_pixel_color(i, j, width, height):
    origin, direction = get_ray(i, j, width, height)

    intersection = get_nearest_intersection(direction, origin)

    if intersection is not None:
        obj, point, normal = intersection
        return (normal + 1) / 2

    return sky_color(direction)


def draw_all():
    render_app.RenderApp(get_pixel_color, 300, 200, result_file='image.png')


draw_all()
