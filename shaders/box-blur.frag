#version 330 core

uniform sampler2D display;
uniform vec2 res;
uniform int kernel = 3;

in vec2 uv;
out vec4 frag_col;

void main()
{
    vec4 color = vec4(0.);
    int min_val = - (kernel - 1) / 2;
    int max_val = min_val + kernel;
    
    for (int x = min_val; x < max_val; x++)
    {
        for (int y = min_val; y < max_val; y++)
        {
            vec2 offset = vec2(x, y) / res.xy;
            color += texture(display, uv + offset);
        }
    }
    
    color /= pow(kernel, 2);
    frag_col = color;
}