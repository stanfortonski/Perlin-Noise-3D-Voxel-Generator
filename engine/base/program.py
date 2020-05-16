import glm
from engine.base.shader import Shader
from OpenGL.GL import *
from OpenGL.error import NullFunctionError

class Program:
    def __init__(self):
        self.__programId = 0
        self.shaders = []

    def attachShader(self, shader):
        self.shaders.append(shader)

    def link(self):
        self.__programId = glCreateProgram()
        for shader in self.shaders:
            shader.compile()
            glAttachShader(self.__programId, shader.getId())

        glLinkProgram(self.__programId)

        for shader in self.shaders:
            shader.delete()
        self.shaders.clear()

        if glGetProgramiv(self.__programId, GL_LINK_STATUS) != GL_TRUE:
            info = glGetProgramInfoLog(self.__programId)
            self.delete()
            raise RuntimeError(f'Error in program linking: {info}')

    def __del__(self):
        self.delete()

    def delete(self):
        try:
            glDeleteProgram(self.__programId)
            self.__programId = 0
        except NullFunctionError:
            pass

    def use(self):
        glUseProgram(self.__programId)

    def getId(self):
        return self.__programId

    def getAttribLocation(self, name):
        return glGetAttribLocation(self.__programId, name)

    def getUniformLocation(self, name):
        return glGetUniformLocation(self.__programId, name)

    def setInt(self, name, value):
        glUniform1i(self.getUniformLocation(name), value)

    def setFloat(self, name, value):
        glUniform1f(self.getUniformLocation(name), value)

    def setVec2(self, name, vec):
        glUniform2fv(self.getUniformLocation(name), 1, glm.value_ptr(vec))

    def setVec3(self, name, vec):
        glUniform3fv(self.getUniformLocation(name), 1, glm.value_ptr(vec))

    def setVec4(self, name, vec):
        glUniform4fv(self.getUniformLocation(name), 1, glm.value_ptr(vec))

    def setMat2(self, name, mat):
        glUniformMatrix2fv(self.getUniformLocation(name), 1, GL_FALSE, glm.value_ptr(mat))

    def setMat3(self, name, mat):
        glUniformMatrix3fv(self.getUniformLocation(name), 1, GL_FALSE, glm.value_ptr(mat))

    def setMat4(self, name, mat):
        glUniformMatrix4fv(self.getUniformLocation(name), 1, GL_FALSE, glm.value_ptr(mat))

def getLinkedProgram(vertPath, fragPath):
    program = Program()
    program.attachShader(Shader(vertPath, GL_VERTEX_SHADER))
    program.attachShader(Shader(fragPath, GL_FRAGMENT_SHADER))
    program.link()
    return program