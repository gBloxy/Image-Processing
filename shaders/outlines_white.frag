#version 330 core

uniform sampler2D display;
uniform vec2 res;

in vec2 uv;
out vec4 frag_col;

mat3 sobelX = mat3(-1.0, -2.0, -1.0,
                    0.0,  0.0,  0.0,
                    1.0,  2.0,  1.0);

mat3 sobelY = mat3(-1.0,  0.0,  1.0,
                   -2.0,  0.0,  2.0,
                   -1.0,  0.0,  1.0);

vec3 samplef(int x, int y){
	return texture(display, vec2(x,y)/res).xyz;
}

float lum(vec3 rgb){
	return (0.2126*rgb.r + 0.7152*rgb.g + 0.0722*rgb.b);
}

void main()
{
    vec3 sx = vec3(0);
    vec3 sy = vec3(0);
    
    for(int i=0; i<=2; i++)
    {
        for(int j=0; j<=2; j++)
        {
        	sx += samplef(int(uv.x * res.x)+i-1, int(uv.y * res.y)+j-1) * sobelX[i][j];
            sy += samplef(int(uv.x * res.x)+i-1, int(uv.y * res.y)+j-1) * sobelY[i][j];
        }
    }
    float finalLum = pow(lum(sx*sx + sy*sy), 0.5);
    if(finalLum < 0.4){
        finalLum = smoothstep(0.0,1.0,finalLum);
    }
    else{
        finalLum = 1.0;
    }
	frag_col = vec4(vec3(1.0 - finalLum), 1.0);
}