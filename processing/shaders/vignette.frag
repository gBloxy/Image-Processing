#version 330 core

uniform sampler2D display;
uniform vec2 res;
uniform float intensity = 0.3;

in vec2 uv;
out vec4 frag_col;

void main()
{
    float width = intensity * 1000.;
    
    vec2 suv = abs(uv * 2.0 - 1.0);
    
    vec4 col = texture(display, uv);
    
    vec2 u = width / res * 0.5;
    
    u = smoothstep(vec2(0), u, 1.0 - suv);
    
    frag_col = col * u.x * u.y;
}