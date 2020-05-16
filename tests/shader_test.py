import sys, unittest, glfw
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.base.shader import Shader
import helper

class ShaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.window = helper.initAndGetWindow()

    @classmethod
    def tearDownClass(cls):
        glfw.terminate()

    def testCompile(self):
        shader = Shader('resources/shaders/test_vert.vs', GL_VERTEX_SHADER)
        shader.compile()
        self.assertEqual(shader.getId(), 1)

    def testShaderFileNotExist(self):
        try:
            shader = Shader('resources/shaders/not_exist.vs', GL_VERTEX_SHADER)
            self.assertTrue(False)
        except RuntimeError:
            self.assertTrue(True)

    def testCompileError(self):
        shader = Shader('resources/shaders/error.fs', GL_FRAGMENT_SHADER)
        self.assertRaises(RuntimeError, shader.compile)
        
if __name__ == '__main__':
    unittest.main()