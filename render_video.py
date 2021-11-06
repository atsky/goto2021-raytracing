import math

import numpy as np
from numba import jit, njit
from matplotlib import image
from tqdm import trange

import render_app

import matplotlib.pyplot as plt


def get_texture(img, u, v):
    shape = img.shape
    i = int(v * shape[0])
    j = int(u * shape[1])
    return img[i % shape[0], j % shape[1], :]


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
        'center': vec3(0, 0.32, 0),
        'radius': 0.3,
        'color': vec3(1, 0.3, 0.3)
    },
    {
        'center': vec3(-0.3, -0.2, 0),
        'radius': 0.3,
        'color': vec3(0.3, 1.0, 0.3)
    },
    {
        'center': vec3(0.3, -0.2, 0),
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
    global frame_number
    a = np.sin(frame_number / 60 * math.pi) * 2.0
    b = np.cos(frame_number / 60 * math.pi) * 2.0

    look_from = np.array([a, 0.0, b])
    look_at = np.array([0.0, 0.0, 0.0])
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
    if depth == 0:
        return vec3(0, 0, 0)
    result = nearest_intersected_object(origin, direction)
    if result is None:
        return sky_color(direction)
    t, obj, p, normal = result

    new_direction = reflected(direction, normal)

    return obj['color'] * trace_ray(new_direction, p, depth - 1)


sky = (image.imread('images/envmap_1.jpeg') / 255.0)

frame_number = 60

import moviepy.editor as mvp
from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter

width = 300
height = 200

with FFMPEG_VideoWriter('out_0.mp4', (width, height), 30.0) as video:
    for i in range(120):
        frame_number = i
        print("frame ", i)
        image = np.zeros((height, width, 3))

        for j in trange(height):
            for i in range(width):
                image[j, i] = get_pixel_color(i, j, width, height)

        image = np.clip(image, 0, 1)
        img = (image * 255).astype(np.uint8)

        video.write_frame(img)

plt.imshow(image)
plt.show()
