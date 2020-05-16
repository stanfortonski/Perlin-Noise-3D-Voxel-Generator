import sys, unittest, glfw
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.base.shader import Shader
from engine.base.program import *
import helper

class ProgramTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.window = helper.initAndGetWindow()

    @classmethod
    def tearDownClass(cls):
        glfw.terminate()

    def testLinking(self):
        try:
            program = Program()
            program.attachShader(Shader('resources/shaders/test_vert.vs', GL_VERTEX_SHADER))
            program.attachShader(Shader('resources/shaders/test_frag.fs', GL_FRAGMENT_SHADER))
            program.link()
            self.assertEqual(program.getId(), 1)
        except RuntimeError:
            self.assertTrue(False)

    def testLinked(self):
        try:
            program = getLinkedProgram('resources/shaders/test_vert.vs', 'resources/shaders/test_frag.fs')
            self.assertEqual(program.getId(), 1)
        except RuntimeError:
            self.assertTrue(False)

    def testErrorCompile(self):
        try:
            program = Program()
            program.attachShader(Shader('resources/shaders/test_vert.vs', GL_VERTEX_SHADER))
            program.attachShader(Shader('resources/shaders/error.fs', GL_FRAGMENT_SHADER))
            program.link()
            self.assertTrue(False)
        except RuntimeError:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()