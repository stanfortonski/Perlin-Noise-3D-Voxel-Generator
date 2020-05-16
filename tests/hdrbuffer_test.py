import sys, unittest, glfw
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.buffer.hdrbuffer import HDRbuffer
import helper

class HDRbufferTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
       cls.window = helper.initAndGetWindow()

    @classmethod
    def tearDownClass(cls):
        glfw.terminate()

    def testHDRbuffer(self):
        width, height = 101, 102
        hdrbuffer = HDRbuffer()
        hdrbuffer.create(width, height)

        self.assertEqual(hdrbuffer.hdrFBO.getId(), 1)
        self.assertEqual(hdrbuffer.rboDepth, 1)
        self.assertEqual(hdrbuffer.colorBuffers[0], 1)
        self.assertEqual(hdrbuffer.colorBuffers[1], 2)
        self.assertEqual(hdrbuffer.width, width)
        self.assertEqual(hdrbuffer.height, height)

if __name__ == '__main__':
    unittest.main()