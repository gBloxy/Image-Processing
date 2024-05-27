#version 330 core

uniform sampler2D display;
uniform vec2 res;
uniform float power = 0.4;

in vec2 uv;
out vec4 frag_col;

#define EPSILON 0.000011

void main()
{
    vec2 p = gl_FragCoord.xy / res.x;
    
    float prop = res.x / res.y;
    vec2 m = vec2(0.5, 0.5 / prop);
    vec2 d = p - m;
    float r = sqrt(dot(d, d)); 
    
    float bind;
    
    if (prop < 1.0)
    {
        bind = m.x;
    } else {
        bind = m.y;
    }
    
    vec2 pos = m + normalize(d) * atan(r * -power * 10.0) * bind / atan(-power * bind * 10.0);
    
    frag_col = vec4(texture(display, vec2(pos.x, -pos.y * prop)).xyz, 1.0);
}