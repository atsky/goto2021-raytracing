#ifndef RAYTRACING_WINDOW_H
#define RAYTRACING_WINDOW_H

#include <iostream>

#define STB_IMAGE_IMPLEMENTATION

#include "stb_image.h"
// GLEW
#define GLEW_STATIC

#include <GL/glew.h>

// GLFW
#include <GLFW/glfw3.h>

#include "vectors.h"

class abstract_ray_tracer {
public:
    virtual void reset(int width, int height) {

    }

    virtual vec3 get_pixel_color(int i, int j, int image_width, int image_height) = 0;
};

namespace {
    inline double clamp(double x, double min, double max) {
        if (x < min) return min;
        if (x > max) return max;
        return x;
    }

    class rasterizer {

    public:
        rasterizer(int width, int height, std::shared_ptr<abstract_ray_tracer> ray_tracer) :
                width(width), height(height), ray_tracer(ray_tracer) {

            image_data = new unsigned char[width * height * 3];
            color_data = new vec3[width * height];
            j = 0;
        }

        ~rasterizer() {
            delete[] image_data;
            delete[] color_data;
        }

        void process_batch();

        const unsigned char *get_data();

        unsigned int width;
        unsigned int height;
    private:

        std::shared_ptr<abstract_ray_tracer> ray_tracer;

        int j;

        vec3 *color_data;
        unsigned char *image_data;
    };

    void rasterizer::process_batch() {
        for (int i = 0; i < width; i++) {
            vec3 color = ray_tracer->get_pixel_color(i, j, width, height);
            int t = i + j * width;
            image_data[t * 3] = static_cast<int>(255.999 * clamp(color.x(), 0, 1));
            image_data[t * 3 + 1] = static_cast<int>(255.999 * clamp(color.y(), 0, 1));
            image_data[t * 3 + 2] = static_cast<int>(255.999 * clamp(color.z(), 0, 1));
        }
        j += 1;

        if (j >= height) {
            j = 0;
        }
    }

    const unsigned char *rasterizer::get_data() {
        return image_data;
    }

// Function prototypes
    void processInput(GLFWwindow *window);

// Window dimensions
    const GLuint WIDTH = 600, HEIGHT = 400;

// Shaders
    const GLchar *vertexShaderSource = "#version 330 core\n"
                                       "layout (location = 0) in vec3 aPos;\n"
                                       "layout (location = 1) in vec2 aTexCoord;\n"
                                       "\n"
                                       "out vec2 TexCoord;\n"
                                       "\n"
                                       "void main()\n"
                                       "{\n"
                                       "    gl_Position = vec4(aPos, 1.0);\n"
                                       "    TexCoord = aTexCoord;\n"
                                       "}";
    const GLchar *fragmentShaderSource = "#version 330 core\n"
                                         "out vec4 FragColor;\n"
                                         "  \n"
                                         "in vec2 TexCoord;\n"
                                         "\n"
                                         "uniform sampler2D ourTexture;\n"
                                         "\n"
                                         "void main()\n"
                                         "{\n"
                                         "    FragColor = texture(ourTexture, TexCoord);\n"
                                         "}";

// The MAIN function, from here we start the application and run the game loop
    int run_it(std::shared_ptr<abstract_ray_tracer> ray_tracer, int width, int height) {
        std::cout << "Starting GLFW context, OpenGL 3.3" << std::endl;
        // Init GLFW
        if (!glfwInit()) {
            std::cerr << "Failed to initialize GLFW\n" << std::endl;
            return -1;
        }
        // Set all the required options for GLFW
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // To make MacOS happy; should not be needed
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

        // Create a GLFWwindow object that we can use for GLFW's functions
        GLFWwindow *window = glfwCreateWindow(WIDTH, HEIGHT, "Ray tracer", nullptr, nullptr);
        if (window == nullptr) {
            std::cout << "Can't create window" << std::endl;
            return -1;
        }
        glfwMakeContextCurrent(window);

        // Set this to true so GLEW knows to use a modern approach to retrieving function pointers and extensions
        glewExperimental = GL_TRUE;
        // Initialize GLEW to setup the OpenGL Function pointers
        glewInit();

        {
            // Define the viewport dimensions
            int width, height;
            glfwGetFramebufferSize(window, &width, &height);
            glViewport(0, 0, width, height);
        }

        // Build and compile our shader program
        // Vertex shader
        GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
        glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
        glCompileShader(vertexShader);
        // Check for compile time errors
        GLint success;
        GLchar infoLog[512];
        glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
        if (!success) {
            glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
            std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
        }
        // Fragment shader
        GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
        glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
        glCompileShader(fragmentShader);
        // Check for compile time errors
        glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
        if (!success) {
            glGetShaderInfoLog(fragmentShader, 512, NULL, infoLog);
            std::cout << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" << infoLog << std::endl;
        }
        // Link shaders
        GLuint shaderProgram = glCreateProgram();
        glAttachShader(shaderProgram, vertexShader);
        glAttachShader(shaderProgram, fragmentShader);
        glLinkProgram(shaderProgram);
        // Check for linking errors
        glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
        if (!success) {
            glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
            std::cout << "ERROR::SHADER::PROGRAM::LINKING_FAILED\n" << infoLog << std::endl;
        }
        glDeleteShader(vertexShader);
        glDeleteShader(fragmentShader);


        // set up vertex image_data (and buffer(s)) and configure vertex attributes
        // ------------------------------------------------------------------
        float vertices[] = {
                // positions        // texture coords
                1.0f, 1.0f, 0.0f, 1.0f, 1.0f, // top right
                1.0f, -1.0f, 0.0f, 1.0f, 0.0f, // bottom right
                -1.0f, -1.0f, 0.0f, 0.0f, 0.0f, // bottom left
                -1.0f, 1.0f, 0.0f, 0.0f, 1.0f  // top left
        };
        unsigned int indices[] = {
                0, 1, 3, // first triangle
                1, 2, 3  // second triangle
        };
        unsigned int VBO, VAO, EBO;
        glGenVertexArrays(1, &VAO);
        glGenBuffers(1, &VBO);
        glGenBuffers(1, &EBO);

        glBindVertexArray(VAO);

        glBindBuffer(GL_ARRAY_BUFFER, VBO);
        glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

        // position attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void *) 0);
        glEnableVertexAttribArray(0);
        // texture coord attribute
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void *) (3 * sizeof(float)));
        glEnableVertexAttribArray(1);


        // load and create a texture
        // -------------------------
        unsigned int texture;
        glGenTextures(1, &texture);
        glBindTexture(GL_TEXTURE_2D,
                      texture); // all upcoming GL_TEXTURE_2D operations now have effect on this texture object
        // set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,
                        GL_REPEAT);    // set texture wrapping to GL_REPEAT (default wrapping method)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        // set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

        rasterizer rasterizer(width, height, ray_tracer);

        // render loop
        // -----------
        while (!glfwWindowShouldClose(window)) {
            // input
            // -----
            processInput(window);

            rasterizer.process_batch();
            rasterizer.process_batch();

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, rasterizer.width, rasterizer.height,
                         0, GL_RGB, GL_UNSIGNED_BYTE, rasterizer.get_data());
            glGenerateMipmap(GL_TEXTURE_2D);

            // bind Texture
            glBindTexture(GL_TEXTURE_2D, texture);

            // render container
            glUseProgram(shaderProgram);
            glBindVertexArray(VAO);
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);

            // glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
            // -------------------------------------------------------------------------------
            glfwSwapBuffers(window);
            glfwPollEvents();
        }

        // optional: de-allocate all resources once they've outlived their purpose:
        // ------------------------------------------------------------------------
        glDeleteVertexArrays(1, &VAO);
        glDeleteBuffers(1, &VBO);
        glDeleteBuffers(1, &EBO);

        // glfw: terminate, clearing all previously allocated GLFW resources.
        // ------------------------------------------------------------------
        glfwTerminate();
        return 0;
    }

// process all input: query GLFW whether relevant keys are pressed/released this frame and react accordingly
// ---------------------------------------------------------------------------------------------------------
    void processInput(GLFWwindow *window) {
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(window, true);
    }
}

int run(std::shared_ptr<abstract_ray_tracer> ray_tracer, int width, int height) {
    return run_it(ray_tracer, width, height);
}

#endif //RAYTRACING_WINDOW_H
