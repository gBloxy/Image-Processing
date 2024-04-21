#version 330 core

uniform sampler2D display;
uniform vec2 res;

in vec2 uv;
out vec4 frag_col;

#define INV_SQRT_OF_2PI 0.39894228040143267793994605993439  // 1.0/SQRT_OF_2PI
#define INV_PI 0.31830988618379067153776752674503

void main()
{
    float sigma = 5.0;
    float kSigma = 2.0;
    float threshold = .100;
    
    float radius = round(kSigma*sigma);
    float radQ = radius * radius;
    
    float invSigmaQx2 = .5 / (sigma * sigma);
    float invSigmaQx2PI = INV_PI * invSigmaQx2;
    
    float invThresholdSqx2 = .5 / (threshold * threshold);
    float invThresholdSqrt2PI = INV_SQRT_OF_2PI / threshold;
    
    vec4 centrPx = texture(display, uv);
    
    float zBuff = 0.0;
    vec4 aBuff = vec4(0.0);
    
    for(float x = -radius; x <= radius; x++)
    {
        float pt = sqrt(radQ-x*x);
        for(float y = -pt; y <= pt; y++)
        {
            vec2 d = vec2(x,y);

            float blurFactor = exp( -dot(d , d) * invSigmaQx2 ) * invSigmaQx2PI; 
            
            vec4 walkPx =  texture(display, uv + d / res);

            vec4 dC = walkPx-centrPx;
            float deltaFactor = exp( -dot(dC, dC) * invThresholdSqx2) * invThresholdSqrt2PI * blurFactor;
                                 
            zBuff += deltaFactor;
            aBuff += deltaFactor * walkPx;
        }
    }
    
    frag_col = aBuff / zBuff;
}