#version 330 core

layout (location = 0) out vec4 fragColor;
layout (location = 1) out vec4 brightColor;

in VS_OUT
{
    vec3 fragPos;
    vec3 normal;
    vec2 texCoords;
} fs_in;

struct Material
{
    vec3 diffuse;
    vec3 specular;
    float shininess;
};

struct Light
{
    vec3 position;
    vec3 diffuse;
    vec3 ambient;
    vec3 specular;
};

uniform vec3 lightPos;
uniform vec3 viewPos;

vec3 calcLight(Light light, Material material, vec3 normal, vec3 viewDir);
float shadowCalculation();

void main()
{
    vec3 viewDir = normalize(viewPos - fs_in.fragPos);
    vec3 normal = normalize(fs_in.normal);

    Light globalLight;
    globalLight.position = lightPos;
    globalLight.ambient = vec3(0.2);
    globalLight.diffuse = vec3(10.0);
    globalLight.specular = vec3(4.0);

    Material material;
    material.diffuse = vec3(0.7, 0.5, 0.5);
    material.specular = vec3(1.0, 0.75, 0.75);
    material.shininess = 64;

    vec3 result = calcLight(globalLight, material, normal, viewDir);

    fragColor = vec4(result, 1.0);
    float brightness = dot(fragColor.rgb, vec3(0.2126, 0.7152, 0.0722));
    if (brightness > 1.0)
        brightColor = vec4(fragColor.rgb, 1.0);
	else
		brightColor = vec4(0.0, 0.0, 0.0, 1.0);
}

vec3 calcLight(Light light, Material material, vec3 normal, vec3 viewDir)
{
    vec3 fragToLightDir = normalize(light.position - fs_in.fragPos);

    float diff = max(dot(fragToLightDir, normal), 0.0);
    vec3 halfwayDir = normalize(fragToLightDir + viewDir);
    float specAngle = max(dot(halfwayDir, normal), 0.0);
    float spec = pow(specAngle, material.shininess);

    vec3 ambient = light.ambient * material.diffuse;
    vec3 diffuse = light.diffuse * material.diffuse * diff;
    vec3 specular = light.specular  * material.specular * spec;
    return ambient + diffuse + specular;
}