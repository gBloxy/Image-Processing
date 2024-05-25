#version 330 core

uniform sampler2D display;
uniform float BarrelPower = 1.5;

in vec2 uv;
out vec4 frag_col;

const float PI = 3.1415926535;


vec2 Distort(vec2 p)
{
    float theta  = atan(p.y, p.x);
    float radius = length(p);
    radius = pow(radius, BarrelPower);
    p.x = radius * cos(theta);
    p.y = radius * sin(theta);
    return 0.5 * (p + 1.0);
}


void main()
{
    vec2 xy = 2.0 * uv - 1.0;
    vec2 pos;
    float d = length(xy);
    if (d < 1.0)
    {
        pos = Distort(xy);
    }
    else
    {
        pos = uv;
    }
    frag_col = texture(display, pos);
}