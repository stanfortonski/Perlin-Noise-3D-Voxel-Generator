#version 330 core

out vec4 fragColor;

in vec2 texCoords;

uniform sampler2D sceneMap;
uniform sampler2D bloomMap;

void main()
{             
    const float gamma = 1.1;
    const float exposure = 0.72;
    vec3 sceneColor = texture(sceneMap, texCoords).rgb;
    vec3 bloomColor = texture(bloomMap, texCoords).rgb;
    vec3 hdrColor = sceneColor + bloomColor;
    
    vec3 result = vec3(1.0) - exp(-hdrColor * exposure); 
    result = pow(result, vec3(1.0 / gamma));
    fragColor = vec4(result, 1.0);
}