#version 330 core

struct PointLight{
    vec3 pos;
    vec3 colour;
    float strength;
    float amb;
};

in vec3 fragmentPos;
in vec2 fragmentTexCoord;
in vec3 fragmentNormal;

out vec4 colour;

uniform sampler2D image;
uniform vec3 camPos;
uniform PointLight Light;

vec3 calculatePointLight(PointLight light, vec3 fragPosition, vec3 fragNormal);

void main()
{
    vec3 temp = vec3(0.0);

    temp += calculatePointLight(Light, fragmentPos, fragmentNormal);

    colour = vec4(temp, 1);
}


vec3 calculatePointLight(PointLight light, vec3 fragmentPos, vec3 fragNormal) {

    vec3 baseTexture = texture(image, fragmentTexCoord).rgb;
    vec3 result = vec3(0.0);

    //geometric data
    vec3 fragLight = light.pos - fragmentPos;
    float distance = length(fragLight);
    fragLight = normalize(fragLight);
    vec3 fragCamera = normalize(camPos - fragmentPos);
    vec3 halfVec = normalize(fragLight + fragCamera);

    //ambient
    result += light.amb * baseTexture;

    //diffuse
    result += light.colour * light.strength * max(0.0, dot(fragNormal, fragLight)) / (distance * distance) * baseTexture;

    //specular
    result += light.colour * light.strength * pow(max(0.0, dot(fragNormal, halfVec)),32) / (distance * distance);

    return result;
}