
import pygame
import moderngl
from array import array
from os.path import dirname
from os import listdir

from processing.const import *


path = dirname(__file__) + '\\'

ctx = moderngl.create_standalone_context()

vbo = ctx.buffer(data=array('f', [
    -1.0,  1.0,  0.0,  0.0, # topleft
     1.0,  1.0,  1.0,  0.0, # topright
    -1.0, -1.0,  0.0,  1.0, # bottomleft
     1.0, -1.0,  1.0,  1.0, # bottomright
    ]))


def uniformError(name, error):
    print(f'The following error occured during setting the {name} uniform to a shader program :')
    print(error)


def fromFile(path: str):
    with open(path) as file:
        code = file.read()
    return code


def load(shader):
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


def equalize(d, keys, src):
    for k in keys:
        d[k] = d[src]


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
    BUMP           : load('bump')
}

equalize(codes, [SHARPEN, EMBOSS, EDGE, LAPLACE], CONVOLUTION)

kernels = {
    SHARPEN  : ( 0, -1,  0, -1,  5, -1,  0, -1,  0),
    EMBOSS   : (-2, -1,  0, -1,  1,  1,  0,  1,  2),
    EDGE     : ( 0,  1,  0,  1, -4,  1,  0,  1,  0),
    LAPLACE  : (-1, -1, -1, -1,  8, -1, -1, -1, -1)
}


class Texture():
    def __init__(self, source):
        if type(source) == moderngl.Texture:
            self.tex = source
        
        elif type(source) == pygame.Surface:
            data = pygame.image.tobytes(source, 'RGBA')
            self.tex = ctx.texture(source.get_size(), components=4, data=data)
            self.tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    
    @property
    def size(self):
        return self.tex.size
    
    def release(self):
        self.tex.release()
    
    def toTexture(self):
        return self.tex
    
    def toSurface(self):
        buffer = self.tex.read()
        surf = pygame.image.frombuffer(buffer, self.tex.size, 'RGBA')
        surf = pygame.transform.flip(surf, False, True)
        return surf


class Shader():
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
    
    def setUniforms(self, **uniforms):
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
    
    def run(self, source):
        if type(source) != Texture:
            source = Texture(source)
        
        src = source.toTexture()
        src.use(0)
        
        try:
            self._setUniform('res', src.size)
        except:
            pass
        
        texture = ctx.texture(src.size, 4)
        
        fbo = ctx.framebuffer(texture)
        fbo.use()
        
        self.vao.render(mode=moderngl.TRIANGLE_STRIP)
        
        src.release()
        
        return Texture(texture)
