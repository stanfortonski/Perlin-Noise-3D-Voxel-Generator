import sys, unittest, glfw, glm
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.buffer.hdrbuffer import HDRbuffer
from engine.buffer.blurbuffer import Blurbuffer
from engine.effect.bloom import Bloom
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
        hdrbuffer = HDRbuffer()
        hdrbuffer.create(800, 600)

        blurbuffer = Blurbuffer()
        blurbuffer.create(800, 600)

        program = getLinkedProgram('resources/shaders/bloomhdr_test.vs', 'resources/shaders/bloomhdr_test.fs')
        blurProgram = getLinkedProgram('resources/shaders/blur.vs', 'resources/shaders/blur.fs')
        hdrProgram = getLinkedProgram('resources/shaders/hdr.vs', 'resources/shaders/hdr.fs')

        program.use()
        program.setMat4('viewProject', helper.getViewProject())
        program.setVec3('viewPos', glm.vec3(0, 0, -5))
        program.setVec3('lightPos', glm.vec3(0, 5, 0))

        blurProgram.use()
        blurProgram.setInt('image', 0)

        hdrProgram.use()
        hdrProgram.setInt('sceneMap', 0)
        hdrProgram.setInt('bloomMap', 1)

        bloom = Bloom(hdrbuffer, hdrProgram, blurbuffer, blurProgram)

        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT)
            glClearColor(0.0, 0.0, 0.0, 0.0)
            
            hdrbuffer.bind()
            self.model.draw(program)
            hdrbuffer.unbind()
            hdrbuffer.finalize()

            bloom.drawProcessedScene()

            glfw.poll_events()
            glfw.swap_buffers(self.window)

if __name__ == '__main__':
    unittest.main()