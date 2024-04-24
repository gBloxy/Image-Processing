
from os.path import dirname


path = dirname(__file__) + '\\'


def uniformError(name, error):
    print(f'The following error occured during setting the {name} uniform to a shader program :')
    print(error)


def equalize(d, keys, src):
    for k in keys:
        d[k] = d[src]


def fromFile(path: str) -> str:
    with open(path) as file:
        code = file.read()
    return code
