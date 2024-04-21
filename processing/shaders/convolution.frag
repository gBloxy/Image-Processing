#version 330 core

uniform sampler2D display;
uniform mat3 kernel = mat3(0, 0, 0, 0, 1, 0, 0, 0, 0);
uniform vec2 res;

in vec2 uv;
out vec4 frag_col;

const float direction[3] = float[3](-1.0, 0.0, 1.0);

void main()
{
    vec4 color = vec4(0);
    
    for (int x = 0; x < 3; x++)
    {
        for (int y = 0; y < 3; y++)
        {
            vec2 offset = vec2(direction[x], direction[y]) / res;
            color += texture(display, uv+offset) * kernel[x][y];
        }
    }
    
    frag_col = vec4(color.rgb, 1.);
}