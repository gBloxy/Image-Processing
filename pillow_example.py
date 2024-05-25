
from PIL import Image

# import the image processing library
from processing import *


# load the image with PIL
image = Image.open('C:/Users/gaspa/Documents/Gaspard/projects/image processing/image.png')

# create a new process of some pre-builds shaders
process = Process(MOTION_BLUR, NOISE_REMOVER, BOX_BLUR, RGBA)

# access a shader step with its index and set his uniforms to customize the effect
process[0].setUniforms(direction=(150, 0)) # index 0 : give access to the motion blur shader instance
process[3].setUniforms(r=1.1)

# execute the process on the image (run all the shader steps on it)
tex = process.run(image)

# convert the output into a PIL Image
pil_img = tex.toImage()

# display the original and processed images
image.show('original')
pil_img.show('processed')
