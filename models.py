from graphics import *


class Model:
    def __init__(self):
        pass
    
    def bind(self) -> None:

        glBindVertexArray(self.vao)
    

    def draw(self) -> None:
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)


    def free(self) -> None:
        
        glDeleteVertexArrays(1,(self.vao,))
        glDeleteBuffers(1,(self.vbo,))




class Demo_Triangle(Model):
    def __init__(self):

        # x, y, z, r, g, b
        vertices = (
            -0.5, -0.5, 0.0,   1.0, 0.0, 0.0,
             0.5, -0.5, 0.0,   0.0, 1.0, 0.0,
             0.0,  0.5, 0.0,   0.0, 0.0, 1.0
        )
        vertices = np.array(vertices, dtype=np.float32)

        self.vertex_count = 3

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    



    
class Tex_demo_triangle(Model):
    def __init__(self):
        
        vertices = (
            -0.5, -0.5, 0.0,    1.0, 0.0, 0.0,    0.0, 1.0,
             0.5, -0.5, 0.0,    0.0, 1.0, 0.0,    1.0, 1.0,
             0.0,  0.5, 0.0,    0.0, 0.0, 1.0,    0.5, 0.0
        )

        vertices = np.array(vertices, dtype=np.float32)

        self.vertex_count = 3

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)


        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))



class Cube(Model):
        def __init__(self):
                # x, y, z, s, t
            vertices = (
                -0.5, -0.5, -0.5, 0, 0,
                0.5, -0.5, -0.5, 1, 0,
                0.5,  0.5, -0.5, 1, 1,

                0.5,  0.5, -0.5, 1, 1,
                -0.5,  0.5, -0.5, 0, 1,
                -0.5, -0.5, -0.5, 0, 0,

                -0.5, -0.5,  0.5, 0, 0,
                0.5, -0.5,  0.5, 1, 0,
                0.5,  0.5,  0.5, 1, 1,

                0.5,  0.5,  0.5, 1, 1,
                -0.5,  0.5,  0.5, 0, 1,
                -0.5, -0.5,  0.5, 0, 0,

                -0.5,  0.5,  0.5, 1, 0,
                -0.5,  0.5, -0.5, 1, 1,
                -0.5, -0.5, -0.5, 0, 1,

                -0.5, -0.5, -0.5, 0, 1,
                -0.5, -0.5,  0.5, 0, 0,
                -0.5,  0.5,  0.5, 1, 0,

                0.5,  0.5,  0.5, 1, 0,
                0.5,  0.5, -0.5, 1, 1,
                0.5, -0.5, -0.5, 0, 1,

                0.5, -0.5, -0.5, 0, 1,
                0.5, -0.5,  0.5, 0, 0,
                0.5,  0.5,  0.5, 1, 0,

                -0.5, -0.5, -0.5, 0, 1,
                0.5, -0.5, -0.5, 1, 1,
                0.5, -0.5,  0.5, 1, 0,

                0.5, -0.5,  0.5, 1, 0,
                -0.5, -0.5,  0.5, 0, 0,
                -0.5, -0.5, -0.5, 0, 1,

                -0.5,  0.5, -0.5, 0, 1,
                0.5,  0.5, -0.5, 1, 1,
                0.5,  0.5,  0.5, 1, 0,

                0.5,  0.5,  0.5, 1, 0,
                -0.5,  0.5,  0.5, 0, 0,
                -0.5,  0.5, -0.5, 0, 1
            )
            self.vertex_count = len(vertices)//5
            vertices = np.array(vertices, dtype=np.float32)

            self.vao = glGenVertexArrays(1)
            glBindVertexArray(self.vao)
            self.vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))

            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))




class ObjMesh(Model):
    def __init__(self, filename):
        vertices = self.loadMesh(filename)
        self.vertex_count = len(vertices)//8
        vertices = np.array(vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        #Vertices
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        #position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))

        #texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))

        #normal
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))


    def loadMesh(self, filename: str) -> list[float]:
        v = []
        vt = []
        vn = []
        vertices = []

        with open(filename, "r") as file:
            line = file.readline()

            while line:

                words = line.split(" ")
                match words[0]:
                    case "v":
                        v.append(self.read_vertex_data(words))
                    case "vt":
                        vt.append(self.read_texcoord_data(words))
                    case "vn":
                        vn.append(self.read_normal_data(words))
                    case "f":
                        self.read_face_data(words, v, vt, vn, vertices)
                line = file.readline()

        return vertices

    def read_vertex_data(self, words: list[str]) -> list[float]:
        
        return [
            float(words[1]),
            float(words[2]),
            float(words[3])
        ]
        
    def read_texcoord_data(self, words: list[str]) -> list[float]:

        return [
            float(words[1]),
            float(words[2])
        ]
        
    def read_normal_data(self, words: list[str]) -> list[float]:

        return [
            float(words[1]),
            float(words[2]),
            float(words[3])
        ]

    def read_face_data(
        self,
        words: list[str], 
        v: list[list[float]], vt: list[list[float]], 
        vn: list[list[float]], vertices: list[float]) -> None:


        triangleCount = len(words) - 3

        for i in range(triangleCount):

            self.make_corner(words[1], v, vt, vn, vertices)
            self.make_corner(words[2 + i], v, vt, vn, vertices)
            self.make_corner(words[3 + i], v, vt, vn, vertices)

    def make_corner(self, corner_description: str, 
        v: list[list[float]], vt: list[list[float]], 
        vn: list[list[float]], vertices: list[float]) -> None:

        v_vt_vn = corner_description.split("/")
        
        for element in v[int(v_vt_vn[0]) - 1]:
            vertices.append(element)
        for element in vt[int(v_vt_vn[1]) - 1]:
            vertices.append(element)
        for element in vn[int(v_vt_vn[2]) - 1]:
            vertices.append(element)