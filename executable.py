import glfw, glm, math
from OpenGL.GL import *
from engine.base.program import getLinkedProgram
from engine.renderable.model import Model
from engine.buffer.texture import *
from engine.buffer.hdrbuffer import HDRbuffer
from engine.buffer.blurbuffer import Blurbuffer
from engine.effect.shadow import Shadow
from engine.effect.bloom import Bloom
from engine.generator import generateVoxelPositions
from engine.camera import Camera
from engine.config import config

cube, hdrbuffer, blurbuffer, lastPosX, lastPosY = None, None, None, None, None
firstTime = True
width, height = config['window_width'], config['window_height']
camera = Camera(glm.vec3(config['world_width']/2, config['world_height']+1, config['world_depth']/2))

def main():
    global hdrbuffer, blurbuffer, cube

    if not glfw.init():
        print('Failed to initialize GLFW.')
        return
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.SAMPLES, config['sampling_level'])
    
    if config['fullscreen']:
        global width, height
        mode = glfw.get_video_mode(glfw.get_primary_monitor())
        width, height = mode.size.width, mode.size.height
        window = glfw.create_window(mode.size.width, mode.size.height, config['app_name'], glfw.get_primary_monitor(), None)
    else:
        window = glfw.create_window(width, height, config['app_name'], None, None)
    if not window:
        print('Failed to create GLFW Window.')
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glfw.set_framebuffer_size_callback(window, resizeCallback)
    glfw.set_cursor_pos_callback(window, mouseMove)
    glfw.set_key_callback(window, keyCallback)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK) 

    program = getLinkedProgram('resources/shaders/vert.vs', 'resources/shaders/frag.fs')
    depthProgram = getLinkedProgram('resources/shaders/shadow_depth.vs', 'resources/shaders/shadow_depth.fs')
    blurProgram = getLinkedProgram('resources/shaders/blur.vs', 'resources/shaders/blur.fs')
    hdrProgram = getLinkedProgram('resources/shaders/hdr.vs', 'resources/shaders/hdr.fs')

    blurProgram.use()
    blurProgram.setInt('image', 0)

    hdrProgram.use()
    hdrProgram.setInt('sceneMap', 0)
    hdrProgram.setInt('bloomMap', 1)

    hdrbuffer = HDRbuffer()
    hdrbuffer.create(width, height)
    blurbuffer = Blurbuffer()
    blurbuffer.create(width, height)

    bloom = Bloom(hdrbuffer, hdrProgram, blurbuffer, blurProgram)

    lightPos = glm.vec3(10, 100, 0)
    perspective = glm.perspective(45, width/height, config['near_plane'], config['far_plane'])

    shadow = Shadow(lightPos, config['near_plane'], config['far_plane'])
    shadow.create(config['shadow_width'], config['shadow_height'])

    cube = Model('resources/models/cube.json')
    texture = loadTexture2D('resources/textures/diffuse.jpg')
    normal = loadTexture2D('resources/textures/normal.jpg')
    specular = loadTexture2D('resources/textures/specular.jpg')
    depth = loadTexture2D('resources/textures/depth.jpg')
    
    blockPositions = generateVoxelPositions(config['world_width'], config['world_height'], config['world_width'])
    cube.setMultiplePositions(blockPositions)
    blockPositions.clear()

    lastTime = glfw.get_time()
    while not glfw.window_should_close(window):
        if config['debug_mode']:
            print(glGetError())

        currentTime = glfw.get_time()
        deltaTime = currentTime - lastTime
        lastTime = currentTime

        lightPos.x = config['world_width']/2
        lightPos.z = math.sin(currentTime*0.1) * config['world_depth']*2
        lightPos.y = config['world_height']*2
        shadow.updateMatrix(lightPos, config['near_plane'], config['far_plane'])

        moveInput(window, deltaTime)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.1, 0.2, 0.8, 1)

        shadow.castShadow(depthProgram)
        cube.drawMultiple(depthProgram)
        shadow.endCastShadow(program)

        hdrbuffer.bind()
        glViewport(0, 0, width, height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        program.use()
        program.setMat4('viewProject', perspective * camera.getViewMatrix())
        program.setVec3('viewPos', camera.position)
        program.setVec3('lightPos', lightPos)

        glActiveTexture(GL_TEXTURE1)
        program.setInt('mat.diffuseMap', 1)
        texture.bind()

        glActiveTexture(GL_TEXTURE2)
        program.setInt('mat.normalMap', 2)
        normal.bind()

        glActiveTexture(GL_TEXTURE3)
        program.setInt('mat.specularMap', 3)
        specular.bind()

        glActiveTexture(GL_TEXTURE4)
        program.setInt('mat.depthMap', 4)
        depth.bind()
        program.setFloat('mat.shininess', 128)
        program.setFloat('mat.heightScale', 0.12)
        
        cube.drawMultiple(program)
        hdrbuffer.unbind()
        hdrbuffer.finalize()

        bloom.drawProcessedScene()

        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()

def resizeCallback(window, w, h):
    if h > 0:
        global width, height, hdrbuffer, blurbuffer
        width, height = w, h
        perspective = glm.perspective(45, width/height, config['near_plane'], config['far_plane'])
        hdrbuffer.delete()
        hdrbuffer.create(width, height)
        blurbuffer.delete()
        blurbuffer.create(width, height)

def keyCallback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, glfw.TRUE)
    if key == glfw.KEY_G and action == glfw.PRESS:
        global cube
        positions = generateVoxelPositions(config['world_width'], config['world_height'], config['world_width'])
        cube.setMultiplePositions(positions)

def mouseMove(win, posX, posY):
    global firstTime, camera, lastPosX, lastPosY
    if firstTime:
        lastPosX = posX
        lastPosY = posY
        firstTime = False

    camera.rotate(posX - lastPosX, lastPosY - posY)
    lastPosX = posX
    lastPosY = posY

def moveInput(win, time):
    if glfw.get_key(win, glfw.KEY_W) == glfw.PRESS:
        camera.moveTop(time)
    if glfw.get_key(win, glfw.KEY_S) == glfw.PRESS:
        camera.moveBottom(time)
    if glfw.get_key(win, glfw.KEY_A) == glfw.PRESS:
        camera.moveLeft(time)
    if glfw.get_key(win, glfw.KEY_D) == glfw.PRESS:
        camera.moveRight(time)

if __name__ == '__main__':
    main()