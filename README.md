# Image Processing

This is a Python library designed for efficient and easy image processing with OpenGl shaders.  
It work with almost any types of images, including PIL Image, pygame Surface, numpy ndarray, and moderngl texture.  
The library provide a lot of processing filters and effects based on moderngl shaders. It allow you to create fully customized shaders programs writted in GLSL. With simplicity in mind, it lets you create processes that run multiple shaders on the same time.

## Installation

Download the source code and place the processing folder in your project directory.

## Usage

- To process an image, you first need a shader object. You can create one with a pre-build filter or by providing the custom glsl source code :
```python
import processing as ip

# create a pre-build shader that invert image colors by providing a shader type (ip.[Constant]) :
shader = ip.Shader(ip.INVERSION)

# create a custom shader with glsl source code :
fragment_code = ip.readFile('path\\to\\fragment\\shader.glsl') # or any string that contain glsl code
shader = ip.Shader(fragment=fragment_code)
```
You can also provide a vertex shader source code, but either fragment and vertex shader and not necessary : if not specified, the default program will be used.
- You can modify the shader uniforms to custom it with the .setUniforms() method :
```python
shader.setUniforms(direction=(150, 0), kernel=(2, 2, 2, 2, -17, 2, 2, 2, 2), etc...)
```
Warning : not all shaders have modifiable uniforms. Check the shader uniforms first in the shader guide.
- Now you can run the shader on an image like that :
```python
image = ... # any type of supported images (PIL images, pygame surfaces, numpy ndarray, moderngl textures)
processed_texture = shader.run(image) # return a ip.Texture object
```
In this case the image is automatically converted into an ip.Texture when passed in the .run() method.
- You can create textures with :
```python
texture = ip.Texture(image_source)
texture.size # access the texture dimensions (width, height)
texture.tex # access the moderngl texture
```
They are very usefull as they can be saved or converted into all the supported images format :
```python
pil_img = texture.toImage()
surface = texture.toSurface()
array = texture.toArray()
texture.save('file\\path\\with\\image\\name.extension')
```
- Finally, you can create process which can run multiple shaders at the same time :
```python
process = ip.Process(ip.MOTION_BLUR, ip.NOISE_REMOVER, ip.BOX_BLUR, ip.RGBA, etc...) # created with filters
# or create your own shaders first :
shader1 = ip.Shader(fragment='fragment code')
shader2 = ip.Shader(ip.GRAYSCALE)
process = ip.Process(shader1, shader2)
# you can also create one with differents source :
process = Process(ip.MOTION_BLUR, shader1)
# run the process
output_tex = process.run(image_source)
```
You can modify a process with :
```python
process.remove(step_index) # remove a shader step
process.add(shader or const) # add a new shader step at the end of the process
process.insert(shader or const, index) # insert a new step at an index, like a list
process[index] # access a shader step with it index
```

## Requirements

To run, the library require Pillow, numpy, moderngl, and pygame. Install all of these by running this line on a command shell :
```bash
pip install -r requirements.txt
```

## Contributing

If you encounter any issues, have suggestions, or need support, please don't hesitate to reach out by creating an issue in the repository.  
All feedbacks are welcome.

## License

The library is licensed under the MIT license - see the `LICENSE` file for details.
