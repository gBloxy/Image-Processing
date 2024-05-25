#version 330 core

uniform sampler2D display;

in vec2 uv;
out vec4 frag_col;

void main()
{
    frag_col = vec4(1. - texture(display, uv).rgb, 1.);
}