from OpenGL.GL import *
from engine.renderable.quad import Quad

class Bloom:
    def __init__(self, hdrbuffer, hdrProgram, blurbuffer, blurProgram):
        self.hdrbuffer = hdrbuffer
        self.hdrProgram = hdrProgram
        self.blurbuffer = blurbuffer
        self.blurProgram = blurProgram
        self.quad = Quad()

    def drawProcessedScene(self):
        horizontal, firstIteration = True, True
        horizontalVal, NhorizontalVal = 1, 0
        self.blurProgram.use()
        for i in range(10):
            if horizontal:
                horizontalVal, NhorizontalVal = 1, 0
            else:
                horizontalVal, NhorizontalVal = 0, 1

            self.blurProgram.setInt('horizontal', horizontal)
            glBindFramebuffer(GL_FRAMEBUFFER, self.blurbuffer.FBOs[horizontalVal])
            glActiveTexture(GL_TEXTURE0)
            if firstIteration:
                glBindTexture(GL_TEXTURE_2D, self.hdrbuffer.colorBuffers[1])
                firstIteration = False
            else:
                glBindTexture(GL_TEXTURE_2D, self.blurbuffer.colorBuffers[NhorizontalVal])
                firstIteration = False
                
            horizontal = not horizontal
            self.quad.draw()

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.hdrProgram.use()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.hdrbuffer.colorBuffers[0])
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.blurbuffer.colorBuffers[NhorizontalVal])
        self.quad.draw()