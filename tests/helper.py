from OpenGL.GL import *
from engine.base.shader import Shader
from engine.base.program import Program
import glfw, glm

width, height = 800, 600

def initAndGetWindow():
    
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    window = glfw.create_window(width, height, 'OpenGL Test', None, None)
    glfw.make_context_current(window)
    return window

def getViewProject():
    return getProjection() * getView()

def getProjection():
    return glm.perspective(45, width/height, 0.1, 100)

def getView():
    return glm.lookAt(glm.vec3(0, 0, -5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))