#version 330 core

uniform sampler2D display;
uniform vec2 res;
uniform float spread = 1;
uniform float intensity = 0.5;

in vec2 uv;
out vec4 frag_col;

void main()
{
    float uv_x = uv.x * res.x;
    float uv_y = uv.y * res.y;

    vec4 sum = vec4(0.0);
    
    for (int n = 0; n < 9; ++n)
    {
        uv_y = (uv.y * res.y) + (spread * float(n - 4));
        vec4 h_sum = vec4(0.0);
        h_sum += texelFetch(display, ivec2(uv_x - (4.0 * spread), uv_y), 0);
        h_sum += texelFetch(display, ivec2(uv_x - (3.0 * spread), uv_y), 0);
        h_sum += texelFetch(display, ivec2(uv_x - (2.0 * spread), uv_y), 0);
        h_sum += texelFetch(display, ivec2(uv_x - spread, uv_y), 0);
        h_sum += texelFetch(display, ivec2(uv_x, uv_y), 0);
        h_sum += texelFetch(display, ivec2(uv_x + spread, uv_y), 0);
        h_sum += texelFetch(display, ivec2(uv_x + (2.0 * spread), uv_y), 0);
        h_sum += texelFetch(display, ivec2(uv_x + (3.0 * spread), uv_y), 0);
        h_sum += texelFetch(display, ivec2(uv_x + (4.0 * spread), uv_y), 0);
        sum += h_sum / 9.0;
    }
    
    frag_col = texture(display, uv) + ((sum / 9.0) * intensity);
}