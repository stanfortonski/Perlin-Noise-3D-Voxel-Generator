import sys, unittest, glfw, glm
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.effect.shadow import Shadow
from engine.renderable.model import Model
from engine.base.shader import Shader
from engine.base.program import *
import helper

class BloomHDRTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.window = helper.initAndGetWindow()
        cls.model = Model('resources/models/monkey.json')

    @classmethod
    def tearDownClass(cls):
        glfw.terminate()

    def testBloomHDRRendering(self):
        program = getLinkedProgram('resources/shaders/shadow_test.vs', 'resources/shaders/shadow_test.fs')
        depthProgram = getLinkedProgram('resources/shaders/shadow_depth.vs', 'resources/shaders/shadow_depth.fs')

        lightPos = glm.vec3(0, 5, 1)

        program.use()
        program.setMat4('viewProject', helper.getViewProject())
        program.setVec3('viewPos', glm.vec3(0, 0, -5))
        program.setVec3('lightPos', lightPos)

        self.model.setMultiplePositions([[0, 1, 0], [0, -1, 0]])

        shadow = Shadow(lightPos, 0.1, 100)
        shadow.create(512, 512)

        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT)
            glClearColor(0.0, 0.0, 0.0, 0.0)
            
            shadow.castShadow(depthProgram)
            self.model.drawMultiple(depthProgram)
            shadow.endCastShadow(program)

            glViewport(0, 0, 800, 600)
            self.model.drawMultiple(program)
            
            glfw.poll_events()
            glfw.swap_buffers(self.window)

if __name__ == '__main__':
    unittest.main()