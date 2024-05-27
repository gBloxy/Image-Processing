#version 330 core

uniform sampler2D display;

in vec2 uv;
out vec4 frag_col;


const mat3 rgb2yuv_mat = mat3(
  0.2126,    0.7152,   0.0722,
 -0.09991,  -0.33609,  0.436,
  0.615,    -0.55861, -0.05639
);

const mat3 yuv2rgb_mat = mat3(
  1.0,  0.0,      1.28033,
  1.0, -0.21482, -0.38059,
  1.0,  2.12798,  0.0
);

vec3 rgb2yuv(vec3 rgb) {
  return rgb * rgb2yuv_mat;
}

vec3 yuv2rgb(vec3 rgb) {
  return rgb * yuv2rgb_mat;
}


void main()
{
	vec4 color = texture(display, uv); 
    vec3 yuv = rgb2yuv(color.rgb);
    vec3 rgb = yuv2rgb(vec3(floor(yuv.x * 2.0) / 2.0, yuv.yz));
    frag_col = vec4(rgb, 1.0);
}