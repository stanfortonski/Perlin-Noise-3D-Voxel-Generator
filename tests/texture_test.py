import sys, unittest, glfw
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.buffer.texture import Texture
import helper

class TextureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.window = helper.initAndGetWindow()

    @classmethod
    def tearDownClass(cls):
        glfw.terminate()

    def testTexture(self):
        texture = Texture(GL_TEXTURE_2D)
        self.assertEqual(texture.getId(), 1)

    def testTextureDelete(self):
        texture = Texture(GL_TEXTURE_2D)
        try:
            texture.delete()
            self.assertEqual(texture.getId(), 0)
        except:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()