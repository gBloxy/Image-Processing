#version 330 core

uniform sampler2D display;
uniform vec2 res;

in vec2 uv;
out vec4 frag_col;

void main()
{
    vec3  col = texture( display, vec2(uv.x, uv.y) ).xyz;
	float lum = dot(col,vec3(0.333));
	
	vec3  nor = normalize( vec3( dFdx(lum), 64.0 / res.x, dFdy(lum) ) );
	float lig = 0.5 + dot(nor, vec3(0.7, 0.2, -0.7));
    col = vec3(lig);
    
    frag_col = vec4(col, 1.0);
}