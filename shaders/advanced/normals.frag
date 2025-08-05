#version 330 core

in vec2 fragmentTexCoord;
in vec3 fragmentNormal;

out vec4 color;



uniform sampler2D image;

void main()
{
    color = texture(image, fragmentTexCoord);
    color.x = fragmentNormal.x;
    color.y = fragmentNormal.y;
    color.z = fragmentNormal.z;

}