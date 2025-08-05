#version 330
in vec2 uv;
uniform sampler2D tex;
out vec4 outColor;
void main() {
    vec3 color = texture(tex, uv).rgb;
    float grey = dot(color.rgb, vec3(0.299, 0.587, 0.114));
    outColor = vec4(vec3(grey), 1.0);  // Invert colors
}