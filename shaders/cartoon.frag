#version 150

uniform sampler2D display;

in vec2 uv;
out vec4 frag_col;

#define EPS 2.e-3

void main()
{
    vec2 uvs = uv;
	uvs.x = uvs.x;
	vec2 uvx = uvs+vec2(EPS,0.);
	vec2 uvy = uvs+vec2(0.,EPS);
	
	vec2 ref = vec2(.5,.5);
	vec3 col0 = texture(display, ref).xyz;
	float lum0 = (col0.x+col0.y+col0.z)/3.;
	
	bool isin = (uvs.x > .5);
	
	vec3 tex, texx, texy;
	vec2 grad;
	float g = 1.;
	
	for (int i=0; i<30; i++) 
	{
		tex = texture(display, uvs).xyz;

		if (isin)
		{
			uvx = uvs+vec2(EPS,0.);
			uvy = uvs+vec2(0.,EPS);	
		}
		texx = texture(display, uvx).xyz;
		texy = texture(display, uvy).xyz;
		grad  = vec2(texx.x-tex.x,texy.x-tex.x); 
//		if (i==0) g = dot(grad,grad);
		
		uvs    += EPS*grad;
		uvx.x += EPS*grad.x;
		uvy.y += EPS*grad.y;
	}
	
	vec3 col = texture(display, uvs).xyz;
    vec3 m = vec3(.2,.1,.1);
	float lum = (col.x+col.y+col.z)/3.;
#if 1
	g = 4.*dot(grad,grad);
	g = pow(max(0.,1.-g),30.);
	g = clamp(g,0.,1.);
#endif
	col = g * col / pow(lum,.55);
	
	frag_col = vec4(col, 1.0);
}