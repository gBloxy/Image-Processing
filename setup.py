from setuptools import setup, find_packages

setup(
    name="image-processing",
    version="0.1.0",
    author="gBloxy",
    description="An opengl image processing python library that work with any types of textures",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gBloxy/Image-Processing",
    packages=find_packages(),
    package_data={
        "processing": ["shaders/*"],
    },
    install_requires=["pygame", "moderngl", "numpy", "Pillow"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
