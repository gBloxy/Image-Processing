#version 330 core

uniform sampler2D display;

in vec2 uv;
out vec4 frag_col;

const float PI = 3.1415926535;

void main()
{
    float aperture = 178.0;
    float apertureHalf = 0.5 * aperture * (PI / 180.0);
    float maxFactor = sin(apertureHalf);
    
    vec2 xy = 2.0 * uv - 1.0;
    float d = length(xy);
    
    vec2 pos;
    
    if (d < (2.0-maxFactor))
    {
        d = length(xy * maxFactor);
        float z = sqrt(1.0 - d * d);
        float r = atan(d, z) / PI;
        float phi = atan(xy.y, xy.x);
        
        pos = vec2(r * cos(phi) + 0.5, r * sin(phi) + 0.5);
    }
    else
    {
        pos = uv;
    }
    
    frag_col = texture(display, pos);
}