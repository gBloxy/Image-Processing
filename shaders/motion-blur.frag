#version 330 core

uniform sampler2D display;
uniform vec2 res;
uniform vec2 direction = vec2(0.);
uniform float intensity = 0.1;

in vec2 uv;
out vec4 frag_col;

const int SampleCount = 64;


vec4 directionalBlur(in vec2 direction, in float intensity)
{
    vec4 color = vec4(0.);
    
    for (int i=1; i<=SampleCount; i++)
    {
        color += texture(display, uv + float(i) * intensity / float(SampleCount) * direction);
    }
  
    return color/float(SampleCount);
}


void main()
{
    vec2 middle = res * .5;
    float dist = length(direction) / length(middle);
    vec4 color = directionalBlur(normalize(direction), dist * intensity);
    
	frag_col = color;
}