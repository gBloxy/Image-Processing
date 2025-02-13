#version 330 core

#define NB_COLORS 2

uniform sampler2D display;

in vec2 uv;
out vec4 frag_col;

// Define MONOCHROME
vec3 monochrome_palette[NB_COLORS] = vec3[](
    vec3 (0.0, 0.0, 0.0), // black
    vec3 (1.0, 1.0, 1.0) // white
);

// Function to find the nearest color in the palette
vec3 closestColor(vec3 color) {
    float minDist = 1000.0;
    vec3 bestMatch = color;

    for (int i = 0; i < NB_COLORS; i++) {
        float dist = distance(color, monochrome_palette[i]);
        if (dist < minDist) {
            minDist = dist;
            bestMatch = monochrome_palette[i];
        }
    }
    return bestMatch;
}


void main()
{
    vec3 color = texture(display, uv).rgb;
    vec3 newColor = closestColor(color);
    frag_col = vec4(newColor, 1.0);
}
