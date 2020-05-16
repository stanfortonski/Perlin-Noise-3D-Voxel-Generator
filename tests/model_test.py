import sys, unittest, glfw, glm
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.renderable.model import Model
from engine.base.program import *
import helper

class ModelTest(unittest.TestCase):
    def setUp(self):
        self.window = helper.initAndGetWindow()

    @classmethod
    def tearDownClass(cls):
        glfw.terminate()

    def testModelLoading(self):
        model = Model('resources/models/monkey.json')
        self.assertEqual(len(model.meshes), 1)

    def testNoExistsModel(self):
        try:
            model = Model('resources/models/not.json')
            self.assertTrue(False)
        except RuntimeError:
            self.assertTrue(True)

    def testDraw(self):
        program = getLinkedProgram('resources/shaders/test_vert.vs', 'resources/shaders/test_frag.fs')
        program.use()
        program.setMat4('viewProject', helper.getViewProject())
        model = Model('resources/models/monkey.json')
        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT)
            glClearColor(0.0, 0.0, 0.0, 0.0)
            model.draw(program)
            glfw.poll_events()
            glfw.swap_buffers(self.window)
            
    def testDrawMultiple(self):
        program = getLinkedProgram('resources/shaders/test_vert.vs', 'resources/shaders/test_frag.fs')
        program.use()
        program.setMat4('viewProject', helper.getViewProject())
        model = Model('resources/models/monkey.json')
        model.setMultiplePositions([[0, 0, 0], [1, 1, 1]])
        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT)
            glClearColor(0.0, 0.0, 0.0, 0.0)
            model.drawMultiple(program)
            glfw.poll_events()
            glfw.swap_buffers(self.window)

if __name__ == '__main__':
    unittest.main()