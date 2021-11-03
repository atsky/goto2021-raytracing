import numpy as np
import matplotlib.pyplot as plt


def get_pixel_color(i, j, width, height):
    r = float(i) / (width - 1)
    g = float(j) / (height - 1)
    b = 0.25

    return np.array([r, g, b])


def draw_all():
    width = 300
    height = 200

    image = np.zeros((height, width, 3))

    for j in range(height):
        for i in range(width):
            image[j, i] = get_pixel_color(i, j, width, height)

    plt.imsave('image.png', image)


draw_all()
