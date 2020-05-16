import sys, unittest, glfw
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.buffer.depthbuffer import Depthbuffer
import helper

class DepthbufferTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
       cls.window = helper.initAndGetWindow()

    @classmethod
    def tearDownClass(cls):
        glfw.terminate()

    def testDepthbuffer(self):
        width, height = 101, 102
        buffer = Depthbuffer()
        buffer.create(width, height)

        self.assertEqual(buffer.getId(), 1)
        self.assertEqual(buffer.type, GL_TEXTURE_2D)

if __name__ == '__main__':
    unittest.main()