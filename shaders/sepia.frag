#version 330 core

uniform sampler2D display;

in vec2 uv;
out vec4 frag_col;

void main()
{
    vec4 texColor = texture(display, uv);
    
    float red = (.3 * texColor.r) + (.189 * texColor.b) + (.769 * texColor.g) + (0. * texColor.a);
    float green = (.3 * texColor.r) + (.168 * texColor.b) + (.686 * texColor.g) + (0. * texColor.a);
    float blue = (.272 * texColor.r) + (.131 * texColor.b) + (.534 * texColor.g) + (0. * texColor.a);
    
    frag_col = vec4(red, green, blue, 1.);

}