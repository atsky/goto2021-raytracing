import math

import numpy as np
from numba import jit, njit

import render_app

import pytest


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

def hit_sphere(center, radius, origin, direction):
    pass

def test_sphere1():
    center = vec3(0.9, -0.2, 0.5)
    radius = 0.7
    origin = vec3(0.2, -0.5, 0.5)
    direction = vec3(-0.9, -0.5, 0.6)
    assert hit_sphere(center, radius, origin, direction)


def test_sphere2():
    center = vec3(0.1, -0.6, -0.7)
    radius = 0.8
    origin = vec3(-0.6, -1, -0.1)
    direction = vec3(-0.1, 0.6, 0.9)
    assert not hit_sphere(center, radius, origin, direction)


def test_sphere3():
    center = vec3(0.2, -0.6, -0.2)
    radius = 0.5
    origin = vec3(0.5, -0.6, -0.1)
    direction = vec3(-0.2, -0.3, 0.4)
    assert hit_sphere(center, radius, origin, direction)


def test_sphere4():
    center = vec3(-0.2, -0.7, -0.7)
    radius = 0.6
    origin = vec3(0.5, -0.1, -0.6)
    direction = vec3(-0.7,  0.,   0.7)
    assert not hit_sphere(center, radius, origin, direction)