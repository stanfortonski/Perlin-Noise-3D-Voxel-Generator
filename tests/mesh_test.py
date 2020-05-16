import sys, unittest, glfw
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.renderable.mesh import Mesh
import helper

class MeshTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.window = helper.initAndGetWindow()

    @classmethod
    def tearDownClass(cls):
        glfw.terminate()

    def testMeshInit(self):
        data = {
            'vertices': [1, 2, 3],
            'faces': [[1]],
            'normals': [1, 2, 3],
            'texturecoords': [1, 1, 1],
            'tangents': [1, 1, 1]
        }

        mesh = Mesh(data)
        self.assertEqual(mesh.VAO, 1)
        self.assertEqual(mesh.EBO, 1)
        self.assertEqual(mesh.VBO, 2)
        self.assertEqual(mesh.VBO_N, 3)
        self.assertEqual(mesh.VBO_TEX, 4)
        self.assertEqual(mesh.VBO_TAN, 5)
        self.assertEqual(mesh.VBO_POS, 6)
        

if __name__ == '__main__':
    unittest.main()