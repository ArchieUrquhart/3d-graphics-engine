#version 330
in vec2 uv;
uniform sampler2D tex;
out vec4 outColor;
void main() {
    vec3 color = texture(tex, uv).rgb;
    outColor = vec4(1.0 - color, 1.0);  // Invert colors
}