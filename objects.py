from graphics import *
from models import Model


class Object:
    def __init__(self,pos: list[float], eulers: list[float], scalers: float,mesh: Model, material: Material):
        self.pos = np.array(pos, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
        self.mesh = mesh
        self.material = material
        self.scalers = scalers
        
    def tick(self) -> None:
        ...

    def get_model_matrix(self) -> np.ndarray:
        model_mat = pyrr.matrix44.create_identity(dtype=np.float32)
        
        #Aplly scalling
        model_mat = pyrr.matrix44.multiply(
            m1= model_mat,
            m2 = np.array([[self.scalers[0],0,0,0],
                           [0,self.scalers[1],0,0],
                           [0,0,self.scalers[2],0],
                           [0,0,0,          1]], dtype=np.float32)
        )

        #apply rotations

        #Y axis rotation
        model_mat = pyrr.matrix44.multiply(
            m1= model_mat, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = GLOBAL_X,
                theta = np.radians(self.eulers[0]), 
                dtype = np.float32
            )
        )
        #X axis rotation
        model_mat = pyrr.matrix44.multiply(
            m1= model_mat, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = GLOBAL_Y,
                theta = np.radians(self.eulers[1]), 
                dtype = np.float32
            )
        )
        #Z axis rotation
        model_mat = pyrr.matrix44.multiply(
            m1= model_mat, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = GLOBAL_Z,
                theta = np.radians(self.eulers[2]), 
                dtype = np.float32
            )
        )
        
        #apply translation
        model_mat = pyrr.matrix44.multiply(
            m1= model_mat, 
            m2=pyrr.matrix44.create_from_translation(
                vec=np.array(self.pos),dtype=np.float32
            )
        )

        return model_mat
    
    
    def draw_model(self, modelMatrixLocation:int) -> None:
        glUniformMatrix4fv(
                modelMatrixLocation, 1, GL_FALSE, 
                self.get_model_matrix())
           
        self.material.use()
        self.mesh.bind()
        self.mesh.draw()

    def free(self):
        self.mesh.free()




class SpinningObject(Object):
    def tick(self) -> None:
        self.eulers[1] += 1
        
        if self.eulers[0] > 360:
            self.eulers[0] -= 360

        if self.eulers[1] > 360:
            self.eulers[1] -= 360

        if self.eulers[2] > 360:
            self.eulers[2] -= 360






class Scene:
    def __init__(self, objects: list[Object], camera: Camera, light: Light):
        self.objects = objects
        self.camera = camera
        self.light = light


    def draw(self, shader:Shader) -> None:
        #set model and view matricies
        self.update_camera(shader)
        self.update_lighting(shader)

        modelMatrixLocation = glGetUniformLocation(shader,"model")
        for object in self.objects:
            object.draw_model(modelMatrixLocation)

    def tick(self) -> None:
        for object in self.objects:
            object.tick()

    def update_camera(self,shader:Shader) -> None:
        #update projection matrix
        glUniformMatrix4fv(
            glGetUniformLocation(shader,"projection"),
            1, GL_FALSE, self.camera.get_proj_matrix()
            )
        
        #update view matrix
        glUniformMatrix4fv(
            glGetUniformLocation(shader,"view"),
            1, GL_FALSE, self.camera.get_view_matrix()
            )
        
        #update camera pos
        glUniform3fv(glGetUniformLocation(shader,"camPos"), 1, self.camera.pos)
    
        
        self.camera.update()


    def update_lighting(self, shader:Shader) -> None:
        self.light.update_uniforms(shader)
    

