#version 330 core

in vec2 fragmentTexCoord;

uniform sampler2D image;

out vec4 color;

void main()
{
    color = texture(image, fragmentTexCoord);
}