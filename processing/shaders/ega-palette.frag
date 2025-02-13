#version 330 core

uniform sampler2D display;

#define NB_COLORS 16

in vec2 uv;
out vec4 frag_col;

// Define EGA
vec3 ega_palette[NB_COLORS] = vec3[](
    vec3 (0.0, 0.0, 0.0), // black
    vec3 (0.0, 0.0, 0.67), // blue
    vec3 (0.0, 0.67, 0.0), // green
    vec3 (0.0, 0.67, 0.67), // Cyan
    vec3 (0.67, 0.0, 0.0), // red
    vec3 (0.67, 0.0, 0.67), // Magenta
    vec3 (0.67, 0.33, 0.0), // brown
    vec3 (0.67, 0.67, 0.67), // light gray
    vec3 (0.33, 0.33, 0.33), // dark gray
    vec3 (0.33, 0.33, 1.0), // light blue
    vec3 (0.33, 1.0, 0.33), // light green
    vec3 (0.33, 1.0, 1.0), // Cyan Clair
    vec3 (1.0, 0.33, 0.33), // light red
    vec3 (1.0, 0.33, 1.0), // light Magenta
    vec3 (1.0, 1.0, 0.33), // yellow
    vec3 (1.0, 1.0, 1.0) // white
);

// Function to find the nearest color in the palette
vec3 closestColor(vec3 color) {
    float minDist = 1000.0;
    vec3 bestMatch = color;

    for (int i = 0; i < NB_COLORS; i++) {
        float dist = distance(color, ega_palette[i]);
        if (dist < minDist) {
            minDist = dist;
            bestMatch = ega_palette[i];
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
