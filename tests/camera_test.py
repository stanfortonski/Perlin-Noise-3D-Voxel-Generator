import sys, unittest, glfw, glm
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.camera import Camera
import helper

class CameraTest(unittest.TestCase):
    def setUp(self):
        self.camera = Camera(glm.vec3(0, 0, 0))
        self.camera.speed = 2
        self.camera.sensitivity = 2
        self.projection = helper.getProjection()

    def testMoveTop(self):
        self.camera.moveTop(1)
        self.camera.updateVectors()

        expectedPos = self.camera.direction * 2
        self.assertEqual(expectedPos, self.camera.position)

    def testMoveBottom(self): 
        self.camera.moveBottom(1)
        self.camera.updateVectors()

        expectedPos = -self.camera.direction * 2
        self.assertEqual(expectedPos, self.camera.position)

    def testMoveleft(self): 
        self.camera.moveLeft(1)
        self.camera.updateVectors()

        expectedPos = -self.camera.right * 2
        self.assertEqual(expectedPos, self.camera.position)

    def testMoveRight(self): 
        self.camera.moveRight(1)
        self.camera.updateVectors()

        expectedPos = self.camera.right * 2
        self.assertEqual(expectedPos, self.camera.position)

    def testRotateX(self):
        self.camera.rotate(3, 0)
        self.camera.updateVectors()
        self.assertEqual(6, self.camera.yaw)

    def testRotateY(self):
        self.camera.rotate(0, 3)
        self.camera.updateVectors()
        self.assertEqual(6, self.camera.pitch)

        self.camera.rotate(0, 100)
        self.camera.updateVectors()
        self.assertEqual(89, self.camera.pitch)

        self.camera.rotate(0, -100)
        self.camera.updateVectors()
        self.assertEqual(-89, self.camera.pitch)
        

if __name__ == '__main__':
    unittest.main()