#version 330 core

uniform sampler2D display;

uniform float r = 1.;
uniform float g = 1.;
uniform float b = 1.;
uniform float a = 1.;

in vec2 uv;
out vec4 frag_col;

void main()
{
    vec4 col = texture(display, uv);
    col *= vec4(r, g, b, a);
    frag_col = col;
}