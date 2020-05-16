import sys, unittest, glfw
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.buffer.texture import Texture
from engine.buffer.texture import loadTexture2D
import helper

class LoadTextureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.window = helper.initAndGetWindow()

    @classmethod
    def tearDownClass(cls):
        glfw.terminate()

    def testLoadTexture(self):
        texture = loadTexture2D('resources/textures/wall.jpg')
        self.assertEqual(texture.getId(), 1)
        self.assertEqual(texture.type, GL_TEXTURE_2D)

    def testLoadTextureNotExists(self):
        try:
            texture = loadTexture2D('resources/textures/not-exists.jpg')
            self.assertTrue(False)
        except:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()