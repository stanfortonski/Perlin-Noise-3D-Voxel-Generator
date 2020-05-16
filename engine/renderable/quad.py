import numpy as np
from OpenGL.GL import *
from OpenGL.error import NullFunctionError

class Quad:
    def __init__(self):
        quadVertices = np.array([
            -1,  1, 0, 0, 1,
            -1, -1, 0, 0, 0,
            1,  1, 0, 1, 1,
            1, -1, 0, 1, 0,
        ], dtype=np.float32)

        self.quadVAO = glGenVertexArrays(1)
        self.quadVBO = glGenBuffers(1)
        glBindVertexArray(self.quadVAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.quadVBO)
        glBufferData(GL_ARRAY_BUFFER, quadVertices, GL_STATIC_DRAW)
        stride = np.dtype(np.float32).itemsize * 5
        offset = ctypes.c_void_p(np.dtype(np.float32).itemsize * 3)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, None)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, offset)
        glBindVertexArray(0)

    def draw(self):
        glDisable(GL_DEPTH_TEST)
        glBindVertexArray(self.quadVAO)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glEnable(GL_DEPTH_TEST)

    def __del__(self):
        self.delete()

    def delete(self):
        try:
            glDeleteVertexArrays(1, self.quadVAO)
            glDeleteBuffers(1, self.quadVBO)
            self.quadVAO, self.quadVBO = 0, 0
        except (NullFunctionError, TypeError):
            pass