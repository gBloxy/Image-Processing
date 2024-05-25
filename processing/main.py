
import pygame
import moderngl
import numpy as np
from PIL import Image
from array import array
from os import listdir

from processing.const import *
from processing.core import readFile, uniformError, path


ctx = moderngl.create_standalone_context()

vbo = ctx.buffer(data=array('f', [
    -1.0,  1.0,  0.0,  0.0, # topleft
     1.0,  1.0,  1.0,  0.0, # topright
    -1.0, -1.0,  0.0,  1.0, # bottomleft
     1.0, -1.0,  1.0,  1.0, # bottomright
    ]))


def load(shader) -> tuple:
    files = listdir(path + 'shaders')
    if f'{shader}.frag' in files:
        frag = readFile(path + 'shaders\\' + f'{shader}.frag')
    else:
        frag = default_codes[0]
    if f'{shader}.vert' in files:
        vert = readFile(path + 'shaders\\' + f'{shader}.vert')
    else:
        vert = default_codes[1]
    return (frag, vert)


default_codes = load('default')

codes = {
    DEFAULT        : default_codes,
    CRT            : load('crt-screen'),
    GAUSSIAN_BLUR  : load('gaussian-blur'),
    BLOOM          : load('bloom'),
    GRAYSCALE      : load('grayscale'),
    BOX_BLUR       : load('box-blur'),
    CONVOLUTION    : load('convolution'),
    NOISE_REMOVER  : load('noise-remover'),
    RGBA           : load('rgba'),
    CARTOON        : load('cartoon'),
    EMBOSS_WHITE   : load('emboss-white'),
    BUMP           : load('bump'),
    MOTION_BLUR    : load('motion-blur'),
    RADIAL_BLUR    : load('radial-blur'),
    VIGNETTE       : load('vignette'),
    SEPIA          : load('sepia'),
    INVERSION      : load('inversion'),
    FISH_EYE       : load('fish-eye'),
    BARREL         : load('barrel'),
    ANTI_FISH_EYE  : load('anti-fish-eye')
}

for k in [SHARPEN, EMBOSS, EDGE, LAPLACE]:
    codes[k] = codes[CONVOLUTION]

kernels = {
    SHARPEN  : ( 0, -1,  0, -1,  5, -1,  0, -1,  0),
    EMBOSS   : (-2, -1,  0, -1,  1,  1,  0,  1,  2),
    EDGE     : ( 0,  1,  0,  1, -4,  1,  0,  1,  0),
    LAPLACE  : (-1, -1, -1, -1,  8, -1, -1, -1, -1)
}


class Texture():
    """
    Texture class for representing images and handle an OpenGL Texture object.
    """
    def __init__(self, source):
        if type(source) == moderngl.Texture:
            self.tex = source
            self.flip(False, True)
        
        elif isinstance(source, Image.Image):
            source = np.array(source)
            self.tex = ctx.texture((source.shape[1], source.shape[0]), components=source.shape[2], data=source.copy())
        
        elif type(source) == pygame.Surface:
            source = pygame.transform.flip(source, False, True)
            data = pygame.image.tobytes(source, 'RGBA')
            self.tex = ctx.texture(source.get_size(), components=4, data=data)
        
        elif type(source) == np.ndarray:
            source = np.flipud(source)
            self.tex = ctx.texture((source.shape[1], source.shape[0]), components=source.shape[2], data=source.copy())
        
        else:
            raise TypeError('Invalid source type : '+str(type(source)))
    
    @property
    def size(self):
        return self.tex.size
    
    def release(self) -> None:
        """
        Release the OpenGL texture.
        
        Warning : This will make this Texture unusable.
        """
        self.tex.release()
    
    def toSurface(self) -> pygame.Surface:
        """
        Convert the Texture to a pygame Surface.
        """
        buffer = self.tex.read()
        surf = pygame.image.frombytes(buffer, self.tex.size, 'RGBA', flipped=True)
        return surf
    
    def toArray(self) -> np.ndarray:
        """
        Convert the Texture to a numpy array.
        """
        buffer = self.tex.read()
        width, height = self.tex.size
        array = np.frombuffer(buffer, dtype=np.uint8)
        array = array.reshape((height, width, self.tex.components))
        return array
    
    def toImage(self) -> Image:
        """
        Convert the Texture to a PIL Image.
        """
        array = self.toArray()
        image = Image.fromarray(array)
        return image
    
    def flip(self, x: bool, y: bool):
        """
        Flip this Texture on x or y axis.
        """
        array = self.toArray()
        if x:
            array = np.fliplr(array)
        if y:
            array = np.flipud(array)
        self.write(array.copy())
    
    def write(self, data) -> None:
        """
        Write new data into the moderngl Texture.
        """
        self.tex.write(data)
    
    def save(self, file_path: str) -> None:
        """
        Save this Texture to a file.
        
        file_path (str) : the file path to save the Texture. It must indicate a file with the desired name and extension.
        """
        surf = self.toSurface()
        pygame.image.save(surf, file_path)


class Shader():
    """
    Shader class responsible for procesing images with a GLSL shader.
    
    type_ : The shader type to create a pre-build shader.
    fragment and vertex (str): GLSL code to create a custom shader without pre-builded type.
    If only one code is passed, the other will be set to the default code.
    """
    def __init__(self, type_: int=None, fragment: str=None, vertex: str=None):
        if type(type_) == int:
            self.frag, self.vert = codes[type_]
            
        elif type_ is None:
            if type(fragment) == str:
                self.frag = fragment
            else:
                self.frag = codes[DEFAULT][0]
            
            if type(vertex) == str:
                self.vert = vertex
            else:
                self.vert = codes[DEFAULT][1]
        
        else:
            self.frag, self.vert = codes[DEFAULT]
        
        self.index = 0
        self.program = ctx.program(vertex_shader=self.vert, fragment_shader=self.frag)
        self.vao = ctx.vertex_array(self.program, [(vbo, '2f 2f', 'vert', 'texcoord')])
        
        if type_ in kernels:
            self._setUniform('kernel', kernels[type_])
        
        self._bind('display')
    
    def _bind(self, uniform):
        index = self.index
        self.program[uniform] = index
        self.index += 1
        return index
    
    def _setUniform(self, name, uniform):
        try:
            self.program[name] = uniform
        except Exception as error:
           return error
    
    def _setUniformTex(self, name, tex):
        try:
            index = self._bind(name)
            tex.use(index)
        except Exception as error:
            return error
    
    def setUniforms(self, **uniforms) -> None:
        """
        Update the shader uniforms.
        """
        for name in uniforms:
            u = uniforms[name]
            if type(u) != pygame.Surface:
                error = self._setUniform(name, u)
                if error:
                    uniformError(name, error)
            else:
                tex = Texture(u).toTexture()
                error = self._setUniformTex(name, tex)
                if error:
                    uniformError(name, error)
    
    def run(self, source) -> Texture:
        """
        Run the shader on a texture and return the processed texture.
        
        source : the texture to process with the shader. It can be a Texture or anything that represent an image.
        """
        if type(source) != Texture:
            source = Texture(source)
        
        src = source.tex
        src.use(0)
        
        try:
            self._setUniform('res', src.size)
        except:
            pass
        
        texture = ctx.texture(src.size, components=4)
        
        fbo = ctx.framebuffer(texture)
        fbo.use()
        
        self.vao.render(mode=moderngl.TRIANGLE_STRIP)
        
        fbo.release()
        
        return Texture(texture)


class Process():
    """
    A Process can automatically run multiple shaders on the same texture in a predifined order.
    """
    def __init__(self, *stages):
        self.stages = []
        for s in stages:
            self.stages.append(self._add(s))
    
    def __getitem__(self, key):
        return self.stages[key]
    
    def _add(self, step):
        if type(step) == int:
            return Shader(step)
        elif type(step) == Shader:
            return step
        else:
            raise TypeError(f'This obj : {step} is not a valid step')
    
    def remove(self, index: int) -> None:
        """
        Remove a shader step from the process.
        
        index : the step index in the process order.
        """
        self.stages.pop(index)
    
    def add(self, step) -> None:
        """
        Add a shader step to the process.
        
        step : either a pre-build filter constant or a custom shader.
        """
        self.stages.append(self._add(step))
    
    def insert(self, step, index: int) -> None:
        """
        Insert a shader step in the process order at an index.
        
        step : either a pre-build filter constant or a custom shader.
        index : the step index in the process order.
        """
        self.stages.insert(index, self._add(step))
    
    def run(self, source) -> Texture:
        """
        Execute the shaders process on a texture and return the processed texture.
        """
        if type(source) != Texture:
            tex = Texture(source)
        else:
            tex = source
        
        for shader in self.stages:
            tex = shader.run(tex)
        
        return tex
