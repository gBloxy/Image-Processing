#version 330 core

uniform sampler2D display;

in vec2 uv;
out vec4 frag_col;

void main()
{
    frag_col = texture(display, uv);
    float g = dot(frag_col.rgb, vec3(0.299, 0.587, 0.114));
    frag_col.rgb = vec3(g, g, g);
}