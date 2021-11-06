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
    }
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


def get_pixel_color(i, j, width, height):
    look_from = np.array([0.1, 0.7, -2.5])
    look_at = np.array([0.0, -0.5, 0.0])
    vup = np.array([0, 1, 0])

    w = normalize(look_from - look_at)
    u = normalize(np.cross(vup, w))
    v = np.cross(w, u)

    x = -0.5 + (i / width)
    y = -0.5 + (j / height)
    ratio = float(width) / height

    x = x * ratio
    y = -y

    origin = look_from
    direction = normalize(normalize(look_at - look_from) + u * x + v * y)

    return trace_ray(direction, origin, 10)


def trace_ray(direction, origin, depth):
    result = nearest_intersected_object(origin, direction)
    if result is None:
        return sky_color(direction)
    t, obj, p, normal = result

    new_direction = reflected(direction, normal)

    r = get_reflective(new_direction, p)
    d = get_light_intensivity(normal, p)

    s = 0.5 + d / 2

    n = normal
    phi = -math.atan2(n[2], n[0]) + math.pi
    u = phi / (2 * math.pi)
    v = (math.asin(n[1]) + math.pi)
    v = v / (2 * math.pi)

    a = int(u * 16)
    b = int(v * 16)

    if (a + b) % 2 == 1:
        color = obj['color']
    else:
        color = vec3(1, 1, 1)

    return r + s * color * trace_ray(new_direction, p, depth - 1)


def get_reflective(new_direction, p):
    light_position = np.array([15.0, 8.0, 2.0])
    cos = np.dot(normalize(light_position - p), new_direction)
    if cos < 0:
        cos = 0
    cos = math.pow(cos, 32)
    return cos


def get_light_intensivity(normal, p):
    light_position = np.array([15.0, 8.0, 2.0])
    cos = -np.dot(normalize(p - light_position), normal)

    if cos < 0:
        cos = 0

    t = p - light_position
    result = nearest_intersected_object(p, -normalize(t))

    if result is not None and result[0] > 1e-10:
        cos = 0

    return cos


sky = (image.imread('images/envmap_1.jpeg') / 255.0)


def draw_all():
    render_app.RenderApp(get_pixel_color, 600, 400, result_file='image.png')


draw_all()
