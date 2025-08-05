import pygame
from OpenGL.GL import *
import numpy as np
from PIL import Image

# === Load input image ===
input_image = Image.open("input.png").convert("RGB")
width, height = input_image.size
image_data = np.array(input_image)[::-1]  # Flip vertically for OpenGL
image_data = image_data.astype(np.uint8)

# === Initialize Pygame with hidden window ===
pygame.init()
pygame.display.set_mode((width, height), pygame.OPENGL | pygame.HIDDEN)

# === Create texture from input image ===
texture_id = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture_id)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# === Create output framebuffer ===
fbo = glGenFramebuffers(1)
glBindFramebuffer(GL_FRAMEBUFFER, fbo)

output_tex = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, output_tex)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, output_tex, 0)

assert glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE
glViewport(0, 0, width, height)

# === Compile shaders ===
VERTEX_SHADER = """
#version 330
in vec2 position;
out vec2 texcoord;
void main() {
    texcoord = (position + 1.0) / 2.0;
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330
in vec2 texcoord;
uniform sampler2D tex;
out vec4 outColor;
void main() {
    vec3 color = texture(tex, texcoord).rgb;
    outColor = vec4(1.0 - color, 1.0);  // Invert colors
}
"""

def compile_shader(src, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, src)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader).decode())
    return shader

# Link shader program
vs = compile_shader(VERTEX_SHADER, GL_VERTEX_SHADER)
fs = compile_shader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
program = glCreateProgram()
glAttachShader(program, vs)
glAttachShader(program, fs)
glLinkProgram(program)
glUseProgram(program)

# === Create fullscreen quad ===
quad_vertices = np.array([
    -1, -1,
     1, -1,
    -1,  1,
     1,  1,
], dtype=np.float32)

vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)

glBindVertexArray(vao)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, quad_vertices.nbytes, quad_vertices, GL_STATIC_DRAW)

pos_loc = glGetAttribLocation(program, 'position')
glEnableVertexAttribArray(pos_loc)
glVertexAttribPointer(pos_loc, 2, GL_FLOAT, GL_FALSE, 0, None)

# === Bind texture and render to FBO ===
glActiveTexture(GL_TEXTURE0)
glBindTexture(GL_TEXTURE_2D, texture_id)
glUniform1i(glGetUniformLocation(program, "tex"), 0)

glClearColor(0.0, 0.0, 0.0, 1.0)
glClear(GL_COLOR_BUFFER_BIT)

glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

# === Read pixels from FBO ===
glBindFramebuffer(GL_FRAMEBUFFER, fbo)
data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)

# === Save output image ===
output = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))
output = np.flipud(output)  # Flip back vertically
Image.fromarray(output).save("output.png")
print("Saved to output.png")

# === Cleanup ===
glDeleteFramebuffers(1, [fbo])
glDeleteTextures([texture_id, output_tex])
glDeleteProgram(program)
glDeleteShader(vs)
glDeleteShader(fs)
pygame.quit()
