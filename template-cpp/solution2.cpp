#include <iostream>
#include <memory>

#include "util.h"
#include "window.h"
#include "vectors.h"

using std::shared_ptr;
using std::make_shared;

const int MAX_ITER = 50;

vec3 sky_color(const vec3 &unit_direction) {
    auto t = 0.5 * (unit_direction.y() + 1.0);
    return (1.0 - t) * vec3(1.0, 1.0, 1.0) + t * vec3(0.5, 0.7, 1.0);
}


class my_ray_tracer : public abstract_ray_tracer {
public:
    my_ray_tracer() {
        double aspect_ratio = 1.5;
    }

    vec3 get_pixel_color(int i, int j, int image_width, int image_height) override {
        double x = 2.0 * i / image_width - 1.0;
        double y = 2.0 * j / image_height - 1.0;
        double ratio = float(image_width) / image_height;
        x = x * ratio;
        y = -y;

        vec3 origin(0, 0, -2);
        vec3 screen_point(x, y, -1);

        vec3 direction = normalize(screen_point - origin);

        return sky_color(direction);
    }
};

int main() {
    render(make_shared<my_ray_tracer>(), 600, 400);
    return 0;
}
