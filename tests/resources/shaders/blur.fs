#version 330 core
#define WEIGHT_LEN 5

out vec4 fragColor;

in vec2 texCoords;

uniform sampler2D image;
uniform bool horizontal;
uniform float weight[WEIGHT_LEN] = float[](0.105, 0.1945945946, 0.1216216216, 0.0540540541, 0.0162162162);

void main()
{             
    vec2 texOffset = 1.0 / textureSize(image, 0);
    vec3 result = texture(image, texCoords).rgb * weight[0];
    if (horizontal)
    {
        for (int i = 0; i < WEIGHT_LEN; ++i)
        {
            result += texture(image, texCoords + vec2(texOffset.x * i, 0.0)).rgb * weight[i];
            result += texture(image, texCoords - vec2(texOffset.x * i, 0.0)).rgb * weight[i];
        }
    }
    else
    {
        for (int i = 0; i < WEIGHT_LEN; ++i)
        {
            result += texture(image, texCoords + vec2(0.0, texOffset.y * i)).rgb * weight[i];
            result += texture(image, texCoords - vec2(0.0, texOffset.y * i)).rgb * weight[i];
        }
    }
    fragColor = vec4(result, 1.0);
}