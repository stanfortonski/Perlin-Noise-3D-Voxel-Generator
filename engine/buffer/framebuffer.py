from OpenGL.GL import *
from OpenGL.error import NullFunctionError

class Framebuffer:
    def __init__(self):
        self.FBO = glGenFramebuffers(1)
        
    def checkComplete(self):
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError('Error when creating Framebuffer.')
        self.unbind()

    def getId(self):
        return self.FBO

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def __del__(self):
        self.delete()

    def delete(self):
        try:
            glDeleteFramebuffers(1, self.FBO)
            self.FBO = 0
        except (NullFunctionError, TypeError):
            pass
