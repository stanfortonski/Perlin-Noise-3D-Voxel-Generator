#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoords;
layout (location = 4) in vec3 aInstancePos;

out VS_OUT
{
    vec3 fragPos;
    vec3 normal;
    vec2 texCoords;
} vs_out;

uniform mat4 viewProject;
uniform mat4 model;
uniform mat4 lightSpaceMatrix;

void main()
{
    vs_out.texCoords = aTexCoords;
    vs_out.normal = transpose(inverse(mat3(model))) * aNormal;
    vs_out.fragPos = vec3(model * vec4(aPos + aInstancePos, 1.0));

    gl_Position = viewProject * vec4(vs_out.fragPos, 1.0);
}