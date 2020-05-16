from OpenGL.GL import *
from OpenGL.error import NullFunctionError
from engine.buffer.framebuffer import Framebuffer
from engine.config import config

class HDRbuffer:
    def create(self, width, height):
        self.width = width
        self.height = height
        self.__createFBO()
        self.__createMultisampleFBO()
       
    def __createFBO(self):
        self.hdrFBO = Framebuffer()
        self.hdrFBO.bind()
        self.colorBuffers = glGenTextures(2)
        for i in range(2):
            glBindTexture(GL_TEXTURE_2D, self.colorBuffers[i])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB16F, self.width, self.height, 0, GL_RGB, GL_FLOAT, None)
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0 + i, GL_TEXTURE_2D, self.colorBuffers[i], 0)

        self.rboDepth = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.rboDepth)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.rboDepth)
        glDrawBuffers(2, [GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1])
        self.hdrFBO.checkComplete()

    def __createMultisampleFBO(self):
        self.__hdrFBO_MS = Framebuffer()
        self.__hdrFBO_MS.bind()
        self.__colorBuffersMS = glGenTextures(2)
        for i in range(2):
            glBindTexture(GL_TEXTURE_2D_MULTISAMPLE, self.__colorBuffersMS[i])
            glTexImage2DMultisample(GL_TEXTURE_2D_MULTISAMPLE, config['sampling_level'], GL_RGB16F, self.width, self.height, GL_TRUE)
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0 + i, GL_TEXTURE_2D_MULTISAMPLE, self.__colorBuffersMS[i], 0)

        self.__rboDepthMS = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.__rboDepthMS)
        glRenderbufferStorageMultisample(GL_RENDERBUFFER, config['sampling_level'], GL_DEPTH_COMPONENT, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.__rboDepthMS)
        glDrawBuffers(2, [GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1])
        self.__hdrFBO_MS.checkComplete()

    def bind(self):
        self.__hdrFBO_MS.bind()

    def finalize(self):
        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.__hdrFBO_MS.getId())
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, self.hdrFBO.getId())
        for i in range(2):
            glReadBuffer(GL_COLOR_ATTACHMENT0 + i)
            glDrawBuffer(GL_COLOR_ATTACHMENT0 + i)
            glBlitFramebuffer(0, 0, self.width, self.height, 0, 0, self.width, self.height, GL_COLOR_BUFFER_BIT, GL_NEAREST)
        glBindFramebuffer(GL_READ_FRAMEBUFFER, 0)
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def unbind(self):
        self.__hdrFBO_MS.unbind()

    def __del__(self):
        self.delete()

    def delete(self):
        self.hdrFBO.delete()
        self.__hdrFBO_MS.delete()
        try:
            glDeleteRenderbuffers(1, self.rboDepth)
            glDeleteRenderbuffers(1, self.rboDepthMS)
            glDeleteTextures(2, self.colorBuffers)
            glDeleteTextures(2, self.__colorBuffersMS)
            self.colorBuffers, self.__colorBuffersMS = 0, 0
            self.rboDepth, self.rboDepthMS = 0, 0
        except (NullFunctionError, TypeError):
            pass