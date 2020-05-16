import numpy as np
from OpenGL.GL import *
from OpenGL.error import NullFunctionError

class Mesh:
    def __init__(self, data):
        indicesList = self.__getIndicesList(data['faces'])
        self.__indicesLen = len(indicesList)
        indicesData = np.array(indicesList, dtype=np.uint32)
        vertexData = np.array(data['vertices'], dtype=np.float32)
        normalData = np.array(data['normals'], dtype=np.float32)
        texCoordsData = np.array(data['texturecoords'], dtype=np.float32)
        tangentData = np.array(data['tangents'], dtype=np.float32)
        
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indicesData, GL_STATIC_DRAW)

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertexData, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        self.VBO_N = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO_N)
        glBufferData(GL_ARRAY_BUFFER, normalData, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)

        self.VBO_TEX = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO_TEX)
        glBufferData(GL_ARRAY_BUFFER, texCoordsData, GL_STATIC_DRAW)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(2)

        self.VBO_TAN = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO_TAN)
        glBufferData(GL_ARRAY_BUFFER, tangentData, GL_STATIC_DRAW)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(3)

        self.VBO_POS = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO_POS)
        data = np.array([[0, 0, 0]], dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, data, GL_DYNAMIC_DRAW)
        glVertexAttribPointer(4, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(4)
        self.positionsLen = 1

        glVertexAttribDivisor(0, 0)
        glVertexAttribDivisor(1, 0)
        glVertexAttribDivisor(2, 0)
        glVertexAttribDivisor(3, 0)
        glVertexAttribDivisor(4, 1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def __getIndicesList(self, assimpIndices):
        indicesList = []
        for face in assimpIndices:
            for indice in face:
                indicesList.append(indice)
        return indicesList

    def setMultiplePositions(self, positions):
        data = np.array(positions, dtype=np.float32)
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO_POS)
        glBufferData(GL_ARRAY_BUFFER, data, GL_DYNAMIC_DRAW)
        glBindVertexArray(0)
        self.positionsLen = len(positions)

    def draw(self, program):
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, self.__indicesLen, GL_UNSIGNED_INT, None)

    def drawMultiple(self, program):
        glBindVertexArray(self.VAO)
        glDrawElementsInstanced(GL_TRIANGLES, self.__indicesLen, GL_UNSIGNED_INT, None, self.positionsLen)

    def __del__(self):
        self.delete()

    def delete(self):
        try:
            glDeleteVertexArrays(1, self.VAO)
            glDeleteBuffers(1, self.VBO)
            glDeleteBuffers(1, self.VBO_N)
            glDeleteBuffers(1, self.VBO_TEX)
            glDeleteBuffers(1, self.VBO_TAN)
            glDeleteBuffers(1, self.EBO)
            glDeleteBuffers(1, self.VBO_POS)
            self.VAO, self.VBO, self.VBO_N, self.VBO_TEX, self.VBO_TAN, self.EBO, self.VBO_POS = 0, 0, 0, 0, 0, 0, 0
        except (NullFunctionError, TypeError):
            pass 
