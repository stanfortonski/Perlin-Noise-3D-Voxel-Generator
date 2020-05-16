import glm
from OpenGL.GL import *
from engine.buffer.depthbuffer import Depthbuffer
from engine.buffer.framebuffer import Framebuffer

class Shadow:
    def __init__(self, lightPos, nearPlane, farPlane):
        self.updateMatrix(lightPos, nearPlane, farPlane)
    
    def updateMatrix(self, lightPos, nearPlane, farPlane):
        lightProjection = glm.ortho(-10, 10, -10, 10, nearPlane, farPlane)
        lightView = glm.lookAt(lightPos, glm.vec3(0), glm.vec3(0, 1, 0))
        self.lightSpaceMatrix = lightProjection * lightView

    def create(self, width, height):
        self.width = width
        self.height = height
        self.depthbuffer = Depthbuffer()
        self.framebuffer = Framebuffer()
        self.framebuffer.bind()
        self.depthbuffer.create(width, height)
        self.depthbuffer.attach()
        self.framebuffer.checkComplete()

    def castShadow(self, depthProgram):
        glDisable(GL_CULL_FACE)
        depthProgram.use()
        depthProgram.setMat4('lightSpaceMatrix', self.lightSpaceMatrix)
        glViewport(0, 0, self.width, self.height)
        self.framebuffer.bind()
        glClear(GL_DEPTH_BUFFER_BIT)
        
    def endCastShadow(self, program):
        self.framebuffer.unbind()
        program.use()
        program.setMat4('lightSpaceMatrix', self.lightSpaceMatrix)
        program.setInt('shadowMap', 10)
        glActiveTexture(GL_TEXTURE10)
        self.depthbuffer.bind()
        glEnable(GL_CULL_FACE)

    def delete(self):
        self.framebuffer.delete()
        self.depthbuffer.delete()