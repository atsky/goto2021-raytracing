import math

import numpy as np
from numba import jit, njit
from matplotlib import image

import render_app


def get_texture(img, u, v):
    shape = img.shape
    i = int(v * shape[0])
    j = int(u * shape[1])
    return img[i, j, :]


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


def reflected(direction, normal):
    return direction - 2 * np.dot(direction, normal) * normal


def sky_color(p):
    phi = math.atan2(-p[2], p[0]) + math.pi

    u = phi / (2 * math.pi)
    v = (1 - p[1]) / 2

    return get_texture(sky, u, v)


def hit_sphere(center, radius, origin, direction):
    oc = origin - center
    a = np.dot(direction, direction)
    b = 2.0 * np.dot(oc, direction)
    c = np.dot(oc, oc) - radius * radius
    discriminant = b * b - 4 * a * c

    if discriminant < 0:
        return -1

    return (-b - math.sqrt(discriminant)) / (2 * a)


objects = [
    {
        'center': vec3(0, 0.32, -1),
        'radius': 0.3,
        'color': vec3(1, 0.3, 0.3)
    },
    {
        'center': vec3(-0.3, -0.2, -1),
        'radius': 0.3,
        'color': vec3(0.3, 1.0, 0.3)
    },
    {
        'center': vec3(0.3, -0.2, -1),
        'radius': 0.3,
        'color': vec3(0.3, 0., 1.0)
    },
    {
        'center': vec3(0, -100.5, -1),
        'radius': 100,
        'color': vec3(0.8, 0.8, 0.8)
    },
]


def nearest_intersected_object(origin, direction):
    min_t = np.inf
    best_result = None

    for obj in objects:
        pass

        center = obj['center']
        radius = obj['radius']

        t = hit_sphere(center, radius, origin, direction)
        if 0 < t < min_t:
            min_t = t
            p = origin + t * direction
            normal = normalize(p - center)

            best_result = t, obj, p, normal

    return best_result

def get_ray(i, j, width, height):
    x = 2.0 * i / width - 1.0
    y = 2.0 * j / height - 1.0
    ratio = float(width) / height
    x = x * ratio
    y = -y
    origin = np.array([0, 0, 0])
    screen_point = np.array([x, y, -1])
    direction = normalize(screen_point - origin)
    return origin, direction

def get_pixel_color(i, j, width, height):
    origin, direction = get_ray(i, j, width, height)

    return trace_ray(direction, origin, 10)


def trace_ray(direction, origin, depth):
    result = nearest_intersected_object(origin, direction)
    if result is None:
        return sky_color(direction)
    t, obj, p, normal = result

    d = get_diffuse_light_intensivity(normal, p)

    s = 0.2 + d

    return s * obj['color']

def get_diffuse_light_intensivity(normal, p):
    light_position = np.array([15.0, 8.0, 2.0])
    light_vector = light_position - p
    cos = np.dot(normalize(light_vector), normal)

    if cos < 0:
        cos = 0

    result = nearest_intersected_object(p, normalize(light_vector))

    if result is not None and result[0] > 1e-10:
        cos = 0

    # Уменьшаем интенсивность света с удалением от источника
    l2 = length2(light_vector)

    return 200 * cos / l2


sky = (image.imread('images/envmap_2.jpeg') / 255.0)


def draw_all():
    render_app.RenderApp(get_pixel_color, 600, 400, result_file='image.png')


draw_all()
