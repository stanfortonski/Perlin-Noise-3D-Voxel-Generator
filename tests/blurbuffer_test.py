import sys, unittest, glfw
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.buffer.blurbuffer import Blurbuffer
import helper

class BlurbufferTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.window = helper.initAndGetWindow()

    @classmethod
    def tearDownClass(cls):
        glfw.terminate()

    def testBlurbuffer(self):
        blurbuffer = Blurbuffer()
        blurbuffer.create(100,100)

        self.assertEqual(blurbuffer.FBOs[0], 1)
        self.assertEqual(blurbuffer.FBOs[1], 2)
        self.assertEqual(blurbuffer.colorBuffers[0], 1)
        self.assertEqual(blurbuffer.colorBuffers[1], 2)

if __name__ == '__main__':
    unittest.main()