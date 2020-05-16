#version 330 core

out vec4 fragColor;

in VS_OUT
{
    vec3 fragPos;
    vec3 normal;
    vec2 texCoords;
    vec4 fragPosLightSpace;
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
uniform sampler2D shadowMap;

vec3 calcLight(Light light, Material material, vec3 normal, vec3 viewDir, float shadow);
float shadowCalculation();

void main()
{
    vec3 viewDir = normalize(viewPos - fs_in.fragPos);
    vec3 normal = normalize(fs_in.normal);

    Light globalLight;
    globalLight.position = lightPos;
    globalLight.ambient = vec3(0.1);
    globalLight.diffuse = vec3(0.9);
    globalLight.specular = vec3(0.9);

    Material material;
    material.diffuse = vec3(0.5, 0.5, 0.5);
    material.specular = vec3(0.75, 0.75, 0.75);
    material.shininess = 64;

    float shadowVal = shadowCalculation();
    vec3 result = calcLight(globalLight, material, normal, viewDir,shadowVal);
    fragColor = vec4(result, 1.0);
}

vec3 calcLight(Light light, Material material, vec3 normal, vec3 viewDir, float shadow)
{
    vec3 fragToLightDir = normalize(light.position - fs_in.fragPos);

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
    shadow /= 9;
    if (projCoords.z > 1.0)
        shadow = 0.0;
    return shadow;
}