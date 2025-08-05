from graphics import *
from models import *
from objects import *

class App:

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.set_up_window()
        
        self.init_assets()

        self.set_onetime_uniforms()

    
    def set_up_window(self) -> None:
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((self.width,self.height), pg.OPENGL|pg.DOUBLEBUF)

        pg.display.set_caption("OpenGL Demo")

        glClearColor(0.1, 0.2, 0.2, 1)
        glEnable(GL_DEPTH_TEST)

        self.clock = pg.time.Clock()


    

    def init_assets(self) -> None:
        
        wood = Material("textures/wood.jpg")
        metal = Material("textures/metal.png")

        self.materials = [wood,metal]



        camera = Camera(fov = 45, aspect = self.width/self.height, near = 0.1, far = 10, pos=[0,0,-3], eulers=[0,0,0])



        #cube = Object(pos = [0,0,0], eulers = [0,0,0], mesh = Cube(), material = wood)

        #cube2 = SpinningObject(pos = [0,0,3], eulers = [0,0,0], mesh = Cube(), material = metal)

        wood_monkey = SpinningObject(pos = [0,0,0], 
                                eulers = [90,0,180], 
                                scalers=[1,1,1], 
                                mesh = ObjMesh("models/monkey.obj"), 
                                material = wood)

        metal_monkey = SpinningObject(pos = [0,0,0], 
                                eulers = [90,0,180], 
                                scalers=[1,0.5,1], 
                                mesh = ObjMesh("models/monkey.obj"), 
                                material = metal)
        
        sun = Light([0,5,-3] ,[1.0, 1.0, 1.0] ,0.2 ,10)

        self.objects = [wood_monkey, metal_monkey]

        shader1 = Shader(
            vertex_filepath = "shaders/3d/default.vert", 
            fragment_filepath = "shaders/advanced/blinphong.frag")
        
        self.shaders = [shader1]
        
        scene1 = Scene(objects = [wood_monkey],camera = camera, light=sun)
        scene2 = Scene(objects = [metal_monkey],camera = camera, light=sun)

        self.scenes = [scene1,scene2]

        self.scene = self.scenes[0]

        self.postProcNone = PostProcessingEffect(window_size=(self.width,self.height),effect="none")
        self.postProcInvert = PostProcessingEffect(window_size=(self.width,self.height),effect="invert")
        self.postProcGrey = PostProcessingEffect(window_size=(self.width,self.height),effect="greyscale")
        
        
    
    def set_onetime_uniforms(self) -> None:

        self.shader = self.shaders[0]
        self.shader.use()

        glUniform1i(glGetUniformLocation(self.shader.program, "image"), 0)
    
        self.projectionMatrixLocation = glGetUniformLocation(self.shader.program,"projection")

        self.modelMatrixLocation = glGetUniformLocation(self.shader.program,"model")

        self.viewMatrixLocation = glGetUniformLocation(self.shader.program,"view")


    def run(self) -> None:
        
        running = True
        while (running):
            #check events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
                if event.type == pg.KEYDOWN:
                    if (event.key == pg.K_SPACE):
                        print("space key pressed ")

                    if (event.key == pg.K_w):
                        self.scene.camera.move((0.4,0,0))
                    if (event.key == pg.K_s):
                        self.scene.camera.move((-0.4,0,0))
                    if (event.key == pg.K_a):
                        self.scene.camera.move((0,-0.4,0))
                    if (event.key == pg.K_d):
                        self.scene.camera.move((0,0.4,0))
                    if (event.key == pg.K_q):
                        self.scene.camera.move((0,0,0.4))
                    if (event.key == pg.K_e):
                        self.scene.camera.move((0,0,-0.4))
                    
            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT)
            glClear(GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader.program)
            
            proc = self.postProcGrey
            proc.use()
            #render all objects
            self.scene.draw(self.shader.program)

            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            proc.draw_to_screen()

            #update objects in the scene
            self.scene.tick()

            pg.display.flip()

            #timing
            self.clock.tick(60)



    def quit(self) -> None: 
        for object in self.objects:
            object.free()
        
        for material in self.materials:
            material.free()

        for shader in self.shaders:
            shader.free()

        pg.quit()


if __name__ == "__main__":

    my_app = App(1000,1000)
    my_app.run()
    my_app.quit()

