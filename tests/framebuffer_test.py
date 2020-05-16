import sys, unittest, glfw
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.buffer.framebuffer import Framebuffer
from engine.buffer.depthbuffer import Depthbuffer
import helper

class FramebufferTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.window = helper.initAndGetWindow()

    @classmethod
    def tearDownClass(cls):
        glfw.terminate()

    def testFramebuffer(self):
        self.framebuffer = Framebuffer()
        self.framebuffer.bind()
        depthbuffer = Depthbuffer()
        depthbuffer.create(100, 100)
        depthbuffer.attach()
        self.framebuffer.checkComplete()
        self.assertEqual(self.framebuffer.getId(), 1)

    def testFramebuffer(self):
        self.framebuffer = Framebuffer()
        self.framebuffer.bind()
        self.assertRaises(RuntimeError, self.framebuffer.checkComplete)

if __name__ == '__main__':
    unittest.main()