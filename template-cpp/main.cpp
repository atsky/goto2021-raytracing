#include <iostream>
#include <memory>

#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION

#include "stb_image.h"
#include "stb_image_write.h"

#include "util.h"
#include "vectors.h"

using std::shared_ptr;
using std::make_shared;

const int MAX_ITER = 50;

int mandelbrot(double real, double imag) {
    double zReal = real;
    double zImag = imag;

    for (int i = 0; i < MAX_ITER; ++i) {
        double r2 = zReal * zReal;
        double i2 = zImag * zImag;

        if (r2 + i2 > 4.0) return i;

        zImag = 2.0 * zReal * zImag + imag;
        zReal = r2 - i2 + real;
    }
    return MAX_ITER;
}


class my_ray_tracer : public abstract_ray_tracer {
public:
    my_ray_tracer() {
    }

    vec3 get_pixel_color(int i, int j, int image_width, int image_height) override {
        double x = -0.5 + 3 * (double(i) / image_width - 0.5);
        double y = 3 * (double(j) / image_height - 0.5);
        x = x * image_width / image_height;

        int k = mandelbrot(x, y);
        if (k == MAX_ITER) {
            return {0, 0, 0};
        }
        int v = 765 * k / MAX_ITER;
        vec3 color;

        if (v > 510) {
            color = vec3(255, 255, v % 255);
        } else if (v > 255) {
            color = vec3(255, v % 255, 0);
        } else {
            color = vec3(v % 255, 0, 0);
        }

        return color / 255.0;
    }
};


int render_simp(std::shared_ptr<abstract_ray_tracer> ray_tracer, size_t width, size_t height) {
    unsigned char *image_data = new unsigned char[width * height * 3];

    const size_t channels = 3;
    for (int j = 0; j < height; j++) {
        for (int i = 0; i < width; i++) {
            vec3 color = ray_tracer->get_pixel_color(i, j, width, height);
            int t = i + j * width;
            image_data[t * 3] = static_cast<int>(255.999 * clamp(color.x(), 0, 1));
            image_data[t * 3 + 1] = static_cast<int>(255.999 * clamp(color.y(), 0, 1));
            image_data[t * 3 + 2] = static_cast<int>(255.999 * clamp(color.z(), 0, 1));
        }
    }

    stbi_write_png("image.png", width, height, channels, image_data, width * channels);
    return 0;
}

int main() {
    render_simp(make_shared<my_ray_tracer>(), 600, 400);
    return 0;
}
