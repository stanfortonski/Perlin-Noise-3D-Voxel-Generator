#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 4) in vec3 aInstancePos;

uniform mat4 model;
uniform mat4 viewProject;

void main()
{
    gl_Position = viewProject * model * vec4(aPos + aInstancePos, 1.0);
}