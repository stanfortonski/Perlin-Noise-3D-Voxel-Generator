#version 330 core

layout (location = 0) out vec4 fragColor;
layout (location = 1) out vec4 brightColor;

in VS_OUT
{
    vec3 fragPos;
    vec3 normal;
    vec2 texCoords;
    vec3 tanLightPos;
    vec3 tanFragPos;
    vec3 tanViewPos;
    vec4 fragPosLightSpace;
} fs_in;

struct Textures
{
    sampler2D diffuseMap;
    sampler2D normalMap;
    sampler2D specularMap;
    sampler2D depthMap;
    float heightScale;
    float shininess;
};

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
uniform sampler2D shadowMap;
uniform Textures mat;

vec3 calcLight(Light light, Material material, vec3 normal, vec3 viewDir, float shadow);
vec2 parallaxMapping(vec3 viewDir);
float shadowCalculation();

void main()
{
    vec3 viewDir = normalize(fs_in.tanViewPos - fs_in.tanFragPos);
    vec2 texCoords = fs_in.texCoords;
    if (mat.heightScale > 0)
        texCoords = parallaxMapping(viewDir);

    vec3 normal = texture(mat.normalMap, texCoords).rgb;
    normal = normalize(normal * 2.0 - 1.0);

    Light globalLight;
    globalLight.position = fs_in.tanLightPos;
    globalLight.ambient = vec3(0.5);
    globalLight.diffuse = vec3(1.3);
    globalLight.specular = vec3(0.3);

    Material material;
    material.diffuse = texture(mat.diffuseMap, texCoords).rgb;
    material.specular = texture(mat.specularMap, texCoords).rgb;
    material.shininess = mat.shininess;

    float shadowVal = shadowCalculation();
    vec3 result = calcLight(globalLight, material, normal, viewDir, shadowVal);

    fragColor = vec4(result, 1.0);
    float brightness = dot(fragColor.rgb, vec3(0.2126, 0.7152, 0.0722));
    if (brightness > 1.0)
        brightColor = vec4(fragColor.rgb, 1.0);
	else
		brightColor = vec4(0.0, 0.0, 0.0, 1.0);
}

vec2 parallaxMapping(vec3 viewDir)
{
    const float minLayers = 10.0;
    const float maxLayers = 32.0;
    float numLayers = mix(maxLayers, minLayers, abs(dot(vec3(0.0, 0.0, 1.0), viewDir)));  
    float layerDepth = 1.0 / numLayers;
    float currentLayerDepth = 0.0;
    vec2 P = viewDir.xy * mat.heightScale;
    vec2 deltaTexCoords = P / numLayers;
    vec2 currentTexCoords = fs_in.texCoords;
    float currentDepth = texture(mat.depthMap, currentTexCoords).r;

    while (currentLayerDepth < currentDepth)
    {
        currentTexCoords -= deltaTexCoords;
        currentDepth = texture(mat.depthMap, currentTexCoords).r;
        currentLayerDepth += layerDepth;
    }

    vec2 prevTexCoords = currentTexCoords + deltaTexCoords;
    float afterDepth = currentDepth - currentLayerDepth;
    float beforeDepth = texture(mat.depthMap, prevTexCoords).r - currentLayerDepth + layerDepth;

    float weight = afterDepth / (afterDepth - beforeDepth);
    vec2 finalTexCoords = prevTexCoords * weight + currentTexCoords * (1.0 - weight);
    return finalTexCoords;
}

vec3 calcLight(Light light, Material material, vec3 normal, vec3 viewDir, float shadow)
{
    vec3 fragToLightDir = normalize(light.position - fs_in.tanFragPos);

    float diff = max(dot(fragToLightDir, normal), 0.0);
    vec3 halfwayDir = normalize(fragToLightDir + viewDir);
    float specAngle = max(dot(halfwayDir, normal), 0.0);
    float spec = pow(specAngle, material.shininess);

    vec3 ambient = light.ambient * material.diffuse;
    vec3 diffuse = light.diffuse  * diff;
    vec3 specular = light.specular * spec;
    return (ambient + (1.0 - shadow) * (diffuse + specular)) * (material.diffuse +  material.specular);
}

float shadowCalculation()
{
    vec3 projCoords = fs_in.fragPosLightSpace.xyz / fs_in.fragPosLightSpace.w;
    projCoords = projCoords * 0.5 + 0.5;
    float closestDepth = texture(shadowMap, projCoords.xy).r; 
    float currentDepth = projCoords.z;
    vec3 lightDir = normalize(lightPos - fs_in.fragPos);
    float bias = max(0.05 * (1.0 - dot(fs_in.normal, lightDir)), 0.005);
    float shadow = 0.0;
    vec2 texelSize = 1.0 / textureSize(shadowMap, 0);
    for (int x = -1; x <= 1; ++x)
    {
        for (int y = -1; y <= 1; ++y)
        {
            float pcfDepth = texture(shadowMap, projCoords.xy + vec2(x, y) * texelSize).r; 
            shadow += currentDepth - bias > pcfDepth ? 1.0 : 0.0;        
        }    
    }
    shadow /= 16.0;
    if (projCoords.z > 1.0)
        shadow = 0.0;
    return shadow;
}