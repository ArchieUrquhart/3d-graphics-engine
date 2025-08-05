import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
import pyrr

GLOBAL_X = np.array([1,0,0], dtype=np.float32)
GLOBAL_Y = np.array([0,1,0], dtype=np.float32)
GLOBAL_Z = np.array([0,0,1], dtype=np.float32)


class Shader:
    def __init__(self, vertex_filepath: str, fragment_filepath: str):

        with open(vertex_filepath,'r') as f:
            vertex_src = f.readlines()

        with open(fragment_filepath,'r') as f: 

            fragment_src = f.readlines()

        self.vert = vertex_src
        self.frag = fragment_src
        
        self.program = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                     compileShader(fragment_src, GL_FRAGMENT_SHADER))

    def free(self) -> None:
        glDeleteProgram(self.program)

    def use(self) -> None:
        glUseProgram(self.program)
    




class Material:

    def __init__(self, filepath: str):

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        
        image = pg.image.load(filepath).convert_alpha()
        image_width,image_height = image.get_rect().size
        img_data = pg.image.tostring(image,'RGBA')
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image_width,image_height,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data)
        glGenerateMipmap(GL_TEXTURE_2D)


    def use(self) -> None:

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,self.texture)


    def free(self) -> None:

        glDeleteTextures(1, (self.texture,))






class Camera:
    def __init__(self, aspect: float, fov: float, near: float, far: float, pos:list[float], eulers: list[float]):
            self.aspect = aspect 
            self.fov = fov
            self.near = near
            self.far = far

            self.pos = np.array(pos, dtype=np.float32)
            self.eulers = np.array(eulers, dtype=np.float32)

            self.update()


    def get_proj_matrix(self) -> np.ndarray:
        proj_mat = pyrr.matrix44.create_perspective_projection(
                fovy = self.fov, aspect = self.aspect, 
                near = self.near, far = self.far, dtype=np.float32
            )
        
        return proj_mat
    
    def get_view_matrix(self) -> np.ndarray:
        view_mat = pyrr.matrix44.create_look_at(
            eye = self.pos,
            target = self.pos + self.forwards,
            up = self.up, dtype = np.float32)
        
        return view_mat
    
    def update(self):
        theta = self.eulers[1]
        phi = self.eulers[2]

        self.forwards = np.array(
            [
                np.sin(np.deg2rad(theta)) * np.cos(np.deg2rad(phi)),
                np.sin(np.deg2rad(phi)),
                np.cos(np.deg2rad(theta)) * np.cos(np.deg2rad(phi))
            ],
            dtype = np.float32
        )

        self.right = np.cross(self.forwards, GLOBAL_Y)

        self.up = np.cross(self.right, self.forwards)


    def move(self, d_pos) -> None:
        self.pos += d_pos[0] * self.forwards \
                  + d_pos[1] * self.right \
                  + d_pos[2] * self.up
    
    
    def spin(self, d_eulers) -> None:
        self.eulers += d_eulers

        self.eulers[0] %= 360
        self.eulers[1] = min(89, max(-89, self.eulers[1]))
        self.eulers[2] %= 360
    






class Light:
    def __init__(self,pos: list[float],colour: list[float],amb: np.float32,strength: np.float32):
        self.pos = np.array(pos, dtype = np.float32)
        self.colour = np.array(colour, dtype = np.float32)
        self.amb = amb
        self.strength = strength

    def update_uniforms(self, shader: Shader) -> None:
        #xyz position
        self.posLocation = glGetUniformLocation(shader,"Light.pos")
        #rgb of light
        self.colourLocation = glGetUniformLocation(shader,"Light.colour")
        #ambient lighting strength
        self.ambLocation = glGetUniformLocation(shader,"Light.amb")
        #lighting strength
        self.strengthLocation = glGetUniformLocation(shader,"Light.strength")

        glUniform3fv(self.posLocation,1,self.pos)
        glUniform3fv(self.colourLocation,1,self.colour)
        glUniform1f(self.ambLocation,self.amb)
        glUniform1f(self.strengthLocation,self.strength)







class PostProcessingEffect:
    def __init__(self, window_size, effect):
        self.width = window_size[0]
        self.height = window_size[1]
        self.effect = effect
    
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                               GL_TEXTURE_2D, self.texture, 0)

        self.depth_rb = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.depth_rb)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT,
                                    GL_RENDERBUFFER, self.depth_rb)
        
        
        """
        self.rbo = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.rbo)
        glRenderbufferStorage(GL_RENDERBUFFER,GL_DEPTH24_STENCIL8, window_size[0], window_size[1])
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.rbo)
        """

        """Setup VAO + shader to draw the framebuffer texture to screen."""

        self.shader = Shader("shaders/postProcess/main.vert", f"shaders/postProcess/{self.effect}.frag")
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        quad = np.array([
            -1, -1, 0, 0,
             1, -1, 1, 0,
            -1,  1, 0, 1,
             1,  1, 1, 1,
        ], dtype=np.float32)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, quad.nbytes, quad, GL_STATIC_DRAW)

        pos_loc = glGetAttribLocation(self.shader.program, 'position')
        uv_loc = glGetAttribLocation(self.shader.program, 'texcoord')
        glEnableVertexAttribArray(pos_loc)
        glVertexAttribPointer(pos_loc, 2, GL_FLOAT, False, 4 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(uv_loc)
        glVertexAttribPointer(uv_loc, 2, GL_FLOAT, False, 4 * 4, ctypes.c_void_p(8))

        glBindVertexArray(0)


    def use(self) -> None:
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.width, self.height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        

    def draw_to_screen(self) -> None:
        glViewport(0, 0, self.width, self.height)
        glDisable(GL_DEPTH_TEST)
        glUseProgram(self.shader.program)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glUniform1i(glGetUniformLocation(self.shader.program, "tex"), 0)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glBindVertexArray(0)

    def free(self) -> None:
        glDeleteTextures(1, (self.texture,))
        glDeleteFramebuffers(1,(self.fbo,))
        glDeleteRenderbuffers(1,(self.rbo,))


    