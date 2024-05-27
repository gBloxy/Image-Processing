#version 330 core

uniform sampler2D display;
uniform vec2 res;
uniform float DotSize = 1.48;

in vec2 uv;
out vec4 frag_col;

#define D2R(d) radians(d)
#define MIN_S 4.0
#define MAX_S 4.0
#define SPEED 0.0

#define SST 0.888
#define SSQ 0.288

#define ORIGIN (0.5 * res)

float R;
float S;

vec4 rgb2cmyki(in vec3 c)
{
	float k = max(max(c.r, c.g), c.b);
	return min(vec4(c.rgb / k, k), 1.0);
}

vec3 cmyki2rgb(in vec4 c)
{
	return c.rgb * c.a;
}

vec2 px2uv(in vec2 px)
{
	return vec2(px / res);
}

vec2 grid(in vec2 px)
{
	return px - mod(px,S);
}

vec4 ss(in vec4 v)
{
	return smoothstep(SST-SSQ, SST+SSQ, v);
}

vec4 halftone(in vec2 fc,in mat2 m)
{
	vec2 smp = (grid(m*fc) + 0.5*S) * m;
	float s = min(length(fc-smp) / (DotSize*0.5*S), 1.0);
    vec3 texc = texture(display, px2uv(smp+ORIGIN)).rgb;
    texc = pow(texc, vec3(2.2)); // Gamma decode.
	vec4 c = rgb2cmyki(texc);
	return c+s;
}

mat2 rotm(in float r)
{
	float cr = cos(r);
	float sr = sin(r);
	return mat2(
		cr,-sr,
		sr,cr
	);
}

vec4 halftone()
{
    vec4 fragColor = vec4(1.0);
    R = SPEED*0.333;
    S = MIN_S + (MAX_S-MIN_S) * (0.5 - 0.5*cos(SPEED));
    
	vec2 fc = uv * res - ORIGIN;
	
	mat2 mc = rotm(R + D2R(15.0));
	mat2 mm = rotm(R + D2R(75.0));
	mat2 my = rotm(R);
	mat2 mk = rotm(R + D2R(45.0));
	
	float k = halftone(fc, mk).a;
	vec3 c = cmyki2rgb(ss(vec4(
		halftone(fc, mc).r,
		halftone(fc, mm).g,
		halftone(fc, my).b,
		halftone(fc, mk).a
	)));
    
    c = pow(c, vec3(1.0/2.2));
	fragColor = vec4(c, 1.0);
    return fragColor;
}

#define SIGMA 10.0
#define BSIGMA 0.1
#define MSIZE 15
//#define USE_CONSTANT_KERNEL
//#define SKIN_DETECTION

const bool GAMMA_CORRECTION = false; 
float kernel[MSIZE];

float normpdf(in float x, in float sigma) {
	return 0.39894 * exp(-0.5 * x * x/ (sigma * sigma)) / sigma;
}

float normpdf3(in vec3 v, in float sigma) {
	return 0.39894 * exp(-0.5 * dot(v,v) / (sigma * sigma)) / sigma;
}

float normalizeColorChannel(in float value, in float min, in float max) {
    return (value - min)/(max-min);
}

vec4 bilateral()
{
	vec4 fragColor = vec4(1.0);
    vec3 c = texture(display, uv).rgb;
    const int kSize = (MSIZE - 1) / 2;
    vec3 final_colour = vec3(0.0);
    float Z = 0.0;
    
#ifdef USE_CONSTANT_KERNEL
    // unfortunately, WebGL 1.0 does not support constant arrays...
    kernel[0] = kernel[14] = 0.031225216;
    kernel[1] = kernel[13] = 0.033322271;
    kernel[2] = kernel[12] = 0.035206333;
    kernel[3] = kernel[11] = 0.036826804;
    kernel[4] = kernel[10] = 0.038138565;
    kernel[5] = kernel[9]  = 0.039104044;
    kernel[6] = kernel[8]  = 0.039695028;
    kernel[7] = 0.039894000;
    float bZ = 0.2506642602897679;
#else
	//create the 1-D kernel
	for (int j = 0; j <= kSize; ++j) {
		kernel[kSize+j] = kernel[kSize-j] = normpdf(float(j), SIGMA);
	}
    float bZ = 1.0 / normpdf(0.0, BSIGMA);
#endif
   

    vec3 cc;
    float factor;
    //read out the texels
    
    vec2 fragCoord = uv * res;
    for (int i=-kSize; i <= kSize; ++i) {
        for (int j=-kSize; j <= kSize; ++j) {
            cc = texture(display, (fragCoord.xy+vec2(float(i),float(j))) / res).rgb;
            factor = normpdf3(cc-c, BSIGMA) * bZ * kernel[kSize+j] * kernel[kSize+i];
            Z += factor;
            if (GAMMA_CORRECTION) {
            	final_colour += factor * pow(cc, vec3(2.2));
            } else {
            	final_colour += factor * cc;
            }
        }
    }
    
    if (GAMMA_CORRECTION) {
    	fragColor = vec4(pow(final_colour / Z, vec3(1.0/2.2)), 1.0);
    } else {
    	fragColor = vec4(final_colour / Z, 1.0);
    }
    
    bool isSkin = true; 
    
#ifdef SKIN_DETECTION
    isSkin = false; 
    vec4 rgb = fragColor * 255.0;
    vec4 ycbcr = rgb;
    ycbcr.x = 16.0 + rgb.x*0.257 + rgb.y*0.504 + rgb.z*0.098;
    ycbcr.y = 128.0 - rgb.x*0.148 - rgb.y*0.291 + rgb.z*0.439;
    ycbcr.z = 128.0 + rgb.x*0.439 - rgb.y*0.368 - rgb.z*0.071;
    if (ycbcr.y > 100.0 && ycbcr.y < 118.0 &&
        ycbcr.z > 121.0 && ycbcr.z < 161.0) {
     	isSkin = true; 
    }
#endif
    return fragColor;
}


vec2 inv_res;


float luminance(vec4 color_in) {
	return 0.25 * color_in.r + 0.5 * color_in.g + 0.25 * color_in.b;
}

float luminance(sampler2D texture_in, vec2 uv, float bias) {
	vec4 sample_color = texture(texture_in, uv, bias);
	return luminance(sample_color);
}

float luminance(sampler2D texture_in, vec2 uv) {
	return luminance(texture_in, uv, 0.0);
}


const mat3 YCoCr_mat = mat3(
	1./4., 1./2., 1./4.,
    -1./4., 1./2., -1./4.,
    1./2., 0.0, -1./2.
);

vec3 YCoCr(vec3 color_in) {
	return YCoCr_mat * color_in;
}

vec3 YCoCr(sampler2D texture_in, vec2 uv) {
	return YCoCr(texture(texture_in, uv).xyz);
}
    

const mat3 sx = mat3( 
    1.0, 2.0, 1.0, 
    0.0, 0.0, 0.0, 
   -1.0, -2.0, -1.0 
);
const mat3 sy = mat3( 
    1.0, 0.0, -1.0, 
    2.0, 0.0, -2.0, 
    1.0, 0.0, -1.0 
);


float calc_sobel_res(mat3 I) {
	float gx = dot(sx[0], I[0]) + dot(sx[1], I[1]) + dot(sx[2], I[2]); 
	float gy = dot(sy[0], I[0]) + dot(sy[1], I[1]) + dot(sy[2], I[2]);

	return sqrt(pow(gx, 2.0)+pow(gy, 2.0));
}


vec3 sobel(vec2 uv) {
    mat3 Y;
    mat3 Co;
    mat3 Cr;
    
    vec3 temp; 
    for (int i=0; i<3; i++) {
        for (int j=0; j<3; j++) {
        	vec2 pos = uv + vec2(float(i-1) * inv_res.x, float(j-1) * inv_res.y);
            temp = YCoCr(display, pos);
            Y[i][j] = temp.x;
            Co[i][j] = temp.y;
            Cr[i][j] = temp.z;
	    }
	}
    
	return vec3(calc_sobel_res(Y), calc_sobel_res(Co), calc_sobel_res(Cr));
}

//toggle between cartoon and comic mode
#define COMIC


void main()
{
	vec4 fillColor = bilateral();
    vec4 halftoneColor = halftone();
    vec2 uv_mirror_x = vec2(uv.x, uv.y);
    
    //res = vec2(textureSize(display, 0));
    inv_res = vec2(1.) / res;
    
	//fragColor = vec4(vec3(YCoCr(display, uv_mirror_x).xyz), 1.0);
    //fragColor = vec4((texture(display, uv_mirror_x).xyz + sobel(uv_mirror_x))/2., 1.0);
    vec3 sobe_edge = sobel(uv_mirror_x);
    frag_col = vec4(sobe_edge, 1.0);
    
    frag_col = vec4(vec3(clamp((sobe_edge.x + sobe_edge.y + sobe_edge.z)/3., 0.0, 1.0)), 1.0);
    if (frag_col.x < 0.05) {
        frag_col = vec4(0.0);
    } 
#ifdef COMIC
    vec3 outlineColor = frag_col.xyz;
    frag_col.xyz = (halftoneColor.xyz + fillColor.xyz) / 2.0;
    frag_col.xyz -= outlineColor;
    
#else
    frag_col = (fillColor - frag_col);
#endif
    
    
}