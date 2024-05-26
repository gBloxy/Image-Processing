# Image Processing Shader Guide

This guide will explain you how to create custom glsl shaders to execute with my image processing library.  
It will only explain how to design fragment shaders.

## Version

Use the version 330 core : all of the pre-builds filters use it and another version may dont' work.

## Inputs / Outputs

The input of all shaders is the coordinate of the currently processed pixel. Its a 2 dimensionnal vector (x, y) with x and y variying from 0.0 to 1.0. The point (0, 0) is the bottom-left image corner. The point (1, 1) is the top-right image corner. The vector is named `uv`.  
The shader output is a 4 dimensionnal vector that represent the color of the current pixel (r, g, b, a). You can name it what you want. I personnally name it `frag_col` or `fragColor`.

## Uniforms

A uniform is a global shader variable modifiable by the cpu, so you can change it value in your python code.  
To get the processed texture, an uniform is always required : `display`.  
You have also access to the texture dimensions (in pixels) with the `res` uniform.  
You can set as much uniforms as you want to make your shader customizable by the python code.

## Main function

The shader need a main function to work : it's necessary called `main()`.

## Example

```glsl
#version 330 core

uniform sampler2D display; // the processed texture is always necessary
uniform vec2 res; // optional but prefer not write it when you don't use it.

in vec2 uv;
out vec4 frag_col;

void main()
{
    vec4 color = texture(display, uv);
    frag_col = vec4(color.rgb, 1.0);
}
```
