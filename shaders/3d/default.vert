#version 330 core

layout (location=0) in vec3 vertexPos;
layout (location=1) in vec2 vertexTexCoord;
layout (location=2) in vec3 vertexNormal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec3 fragmentPos;
out vec2 fragmentTexCoord;
out vec3 fragmentNormal;

void main()
{
    gl_Position = projection * view * model * vec4(vertexPos, 1.0);
    fragmentPos = (model * vec4(vertexPos, 1.0)).xyz;
    fragmentTexCoord = vertexTexCoord;
    fragmentNormal = normalize(mat3(model)*vertexNormal);
    
}