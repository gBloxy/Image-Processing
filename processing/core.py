
from os.path import dirname


path = dirname(__file__) + '\\'


def uniformError(name, error):
    print(f'The following error occured during setting the {name} uniform to a shader program :')
    print(error)


def readFile(path: str) -> str:
    with open(path) as file:
        data = file.read()
    return data
