from OpenGL.GL import *
from OpenGL.error import NullFunctionError
from engine.buffer.framebuffer import Framebuffer
  
class Blurbuffer:
    def create(self, width, height):
        self.FBOs = glGenFramebuffers(2)
        self.colorBuffers = glGenTextures(2)
        for i in range(2):
            glBindFramebuffer(GL_FRAMEBUFFER, self.FBOs[i])
            glBindTexture(GL_TEXTURE_2D, self.colorBuffers[i])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB16F, width, height, 0, GL_RGB, GL_FLOAT, None)
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.colorBuffers[i], 0)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError('Error when creating Blur Framebuffers.')
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def __del__(self):
        self.delete()

    def delete(self):
        try:
            glDeleteFramebuffers(2, self.FBOs)
            glDeleteTextures(2, self.colorBuffers)
            self.colorBuffers = 0
        except NullFunctionError:
            pass