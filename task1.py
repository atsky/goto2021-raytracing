import numpy as np
import math


def vec3(x, y, z):
    return np.array([x, y, z], dtype=float)


# Функция возвращает квадрат длины вектора
def length2(v):
    pass


# Функция возвращает длину вектора
def length(v):
    pass


# Функция возвращает нормализованный вектор x
def normalize(v):
    pass


def main():
    assert math.isclose(length2(vec3(1, 1, -1)), 3)

    assert math.isclose(length(vec3(1, 2, -1)), math.sqrt(6))

    assert math.isclose(length(normalize((vec3(1, 2, 3)))), 1.0)


if __name__ == "__main__":
    main()
