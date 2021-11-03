import numpy as np
from numba import jit, njit

import render_app

import colorsys

MAX_ITER = 50


def rgb_conv(i):
    v = 765 * i / MAX_ITER
    if v > 510:
        color = (255, 255, v % 255)
    elif v > 255:
        color = (255, v % 255, 0)
    else:
        color = (v % 255, 0, 0)
    return np.array(color) / 255.0


def get_pixel_color(x, y, width, height):
    x = -1 + 4 * (float(x) / width - 0.5)
    y = 4 * (float(y) / height - 0.5)
    x *= height / width
    c = complex(x, y)

    z = 0

    for i in range(1, MAX_ITER):
        if abs(z) > 2:
            return rgb_conv(i)
        z *= z + c

    return np.array([0.0, 0.0, 0.0])


def draw_all():
    render_app.RenderApp(get_pixel_color, 600, 400)


draw_all()
