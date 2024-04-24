
import pygame
import moderngl
from array import array
from os import listdir

from processing.const import *
from processing.core import fromFile, equalize, uniformError, path


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
        frag = fromFile(path + 'shaders\\' + f'{shader}.frag')
    else:
        frag = default_codes[0]
    if f'{shader}.vert' in files:
        vert = fromFile(path + 'shaders\\' + f'{shader}.vert')
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
    RADIAL_BLUR    : load('radial-blur')
}

equalize(codes, [SHARPEN, EMBOSS, EDGE, LAPLACE], CONVOLUTION)

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
        
        elif type(source) == pygame.Surface:
            source = pygame.transform.flip(source, False, True)
            data = pygame.image.tobytes(source, 'RGBA')
            self.tex = ctx.texture(source.get_size(), components=4, data=data)
            self.tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    
    @property
    def size(self) -> tuple:
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
        surf = pygame.image.frombuffer(buffer, self.tex.size, 'RGBA')
        # surf = pygame.transform.flip(surf, False, True)
        return surf
    
    def write(self, data) -> None:
        ...
    
    def save(self, file_path: str) -> None:
        """
        Save this Texture to a file.
        
        file_path (str) : the file path to save the Texture. It must indicate a file with the desired name and extension.
        """
        pygame.image.save()
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
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        
        fbo = ctx.framebuffer(texture)
        fbo.use()
        
        self.vao.render(mode=moderngl.TRIANGLE_STRIP)
        
        fbo.release()
        
        return Texture(texture)


class Process():
    ...
