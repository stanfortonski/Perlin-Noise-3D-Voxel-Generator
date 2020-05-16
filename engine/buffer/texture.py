from OpenGL.GL import *
from OpenGL.error import NullFunctionError
from PIL import Image

class Texture:
    def __init__(self, type):
        self.type = type
        self.texture = glGenTextures(1)

    def getId(self):
        return self.texture

    def bind(self):
        glBindTexture(self.type, self.texture)

    def unbind(self):
        glBindTexture(self.type, 0)

    def __del__(self):
        self.delete()

    def delete(self):
        try:
            glDeleteTextures(1, self.texture)
            self.texture = 0
        except (NullFunctionError, TypeError):
            pass

def loadTexture2D(path):
    texture = Texture(GL_TEXTURE_2D)
    texture.bind()

    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    imgData = image.convert('RGBA').tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgData)

    glGenerateMipmap(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture