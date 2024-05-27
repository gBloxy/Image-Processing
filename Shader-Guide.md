# Image Processing Shader Guide

This guide will explain how to create custom GLSL shaders to use with my image processing library.  
It will only explain how to design fragment shaders.

## Version

Use version 330 core : all the pre-built filters use it, and other versions may not work.

## Inputs / Outputs

The input of all shaders is the coordinate of the currently processed pixel. It's a 2-dimensional vector (x, y) with 'x' and 'y' varying from 0.0 to 1.0. The point (0, 0) is the bottom-left image corner and the point (1, 1) is the top-right image corner. The vector is named `uv`.  
The shader output is a 4-dimensional vector representing the color of the current pixel (r, g, b, a). You can name it whatever you want. I personally name it `frag_col` or `fragColor`.

## Uniforms

A uniform is a global shader variable modifiable by the CPU, so you can change its value in your python code.  
To access the processed texture, a uniform is always required : `display`.  
You also have access to the texture dimensions (in pixels) with the `res` uniform.  
You can set as many uniforms as you want to make your shader customizable by the python code.

## Main function

The shader needs a main function to work : it's necessarily called `main()`.

## Example

```glsl
#version 330 core

uniform sampler2D display; // The processed texture is always necessary
uniform vec2 res; // Optional but prefer not to write it when you don't use it.

in vec2 uv;
out vec4 frag_col;

void main()
{
    vec4 color = texture(display, uv);
    frag_col = vec4(color.rgb, 1.0);
}
```

## Filters Uniforms

Some pre-buillt shaders have customizable uniforms :
+ RGBA : uniforms `float r=1.`, `float g=1.`, `float b=1.`, `float a=1.` : original pixel color multipliers.
+ BOX_BLUR : `int kernel=3` : the kernel size used to blur. Must be an odd number.
+ MOTION_BLUR : `vec2 direction=vec2(0, 0)` : vector that represents the motion effect direction, `float intensity=0.1` : the intensity of the motion blur effect.
+ RADIAL_BLUR : `vec2 center=vec2(0.5, 0.5)` : the center of the radial blur effect, `float intensity=0.1` : the intensity of the radial blur effect.
+ CONVOLUTION : `mat3 kernel=mat3(0, 0, 0, 0, 1, 0, 0, 0, 0)` : the factors matrix used in the convolution process.
+ BLOOM : `float spread=1.` : the bloom spread, `float intensity=0.5` : the bloom intensity.
+ BARREL : `float BarrelPower=1.5` : the barrel effect intensity.
+ ANTI_FISH_EYE : `float power=0.4` : the intensity of the effect.
+ VIGNETTE : `float intensity=0.3` : the vignette effect intensity, which controls the border size magnitude.
