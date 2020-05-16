import math, glm

class Camera:
    def __init__(self, position):
        self.position = position
        self.up = glm.vec3(0, 1, 0)
        self.worldUp = glm.vec3(0, 1, 0)
        self.pitch = 0
        self.yaw = 0
        self.speed = 20
        self.sensitivity = 0.25
        self.updateVectors()

    def moveRight(self, time):
        self.position += self.right * (self.speed * time)
  
    def moveLeft(self, time):
        self.position -= self.right * (self.speed * time)

    def moveTop(self, time):
        self.position += self.direction * (self.speed * time)

    def moveBottom(self, time):
        self.position -= self.direction * (self.speed * time)

    def rotate(self, offsetX, offsetY):
        self.yaw += offsetX * self.sensitivity
        self.pitch += offsetY * self.sensitivity
        if self.pitch > 89:
            self.pitch = 89
        elif self.pitch < -89:
            self.pitch = -89
        self.updateVectors()
    
    def updateVectors(self):
        x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        y = math.sin(glm.radians(self.pitch))
        z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        front = glm.vec3(x, y, z)
        self.direction = glm.normalize(front)
        self.right = glm.normalize(glm.cross(self.direction, self.worldUp))
        self.up = glm.normalize(glm.cross(self.right, self.direction))

    def getViewMatrix(self):
        return glm.lookAt(self.position, self.position + self.direction, self.up)