import os
from OpenGL.GL import *
from OpenGL.error import NullFunctionError

class Shader:
    def __init__(self, sourcePath, shaderType):
        self.__shaderId = 0
        if not os.path.exists(sourcePath):
            raise RuntimeError(f'Shader source file {sourcePath} does not exists.')
        self.__sourcePath = sourcePath
        self.shaderType = shaderType

    def compile(self):
        self.__shaderId = glCreateShader(self.shaderType)
        glShaderSource(self.__shaderId, self.__loadSource())
        glCompileShader(self.__shaderId)
        if glGetShaderiv(self.__shaderId, GL_COMPILE_STATUS) != GL_TRUE:
            info = glGetShaderInfoLog(self.__shaderId)
            raise RuntimeError(f'Shader compilation failed:\n{info}')

    def __loadSource(self):
        with open(self.__sourcePath) as file:
            source = file.read()
        return source

    def getId(self):
        return self.__shaderId

    def __del__(self):
        self.delete()

    def delete(self):
        try:
            glDeleteShader(self.__shaderId)
            self.__shaderId = 0
        except NullFunctionError:
            pass
