from PIL import Image
from processing import *

REDUCE_FACTOR = 2

# TODO: Get shaders from image-processing library
shaders = {
    CRT,
    GAUSSIAN_BLUR,
    BLOOM,
    GRAYSCALE,
    BOX_BLUR,
    CONVOLUTION,
    NOISE_REMOVER,
    RGBA,
    CARTOON,
    EMBOSS_WHITE,
    BUMP,
    MOTION_BLUR,
    RADIAL_BLUR,
    VIGNETTE,
    SEPIA,
    INVERSION,
    FISH_EYE,
    BARREL,
    ANTI_FISH_EYE,
    OUTLINES_WHITE,
    COMIC,
    SIMPLE_CARTOON,
}

# load the image with PIL
image = Image.open("image.png")
image = image.resize(
    (int(image.size[0] / REDUCE_FACTOR), int(image.size[1] / REDUCE_FACTOR)),
    Image.Resampling.LANCZOS,
)

with open("TEST-README.md", "w") as readme_file:
    # README header
    readme_file.write("# Shader results\n\n")
    readme_file.write("Here the samples results with applied shader effects.\n\n")
    readme_file.write("| Shader name | Image |\n")
    readme_file.write("| ------------- | ----- |\n")

    # Generate the samples
    for constant in shaders:
        constant_name = [
            name for name, value in globals().items() if value == constant
        ][0]

        try:
            print(f"Processing {constant_name}")
            # Apply ther shader
            process = Process(constant)
            tex = process.run(image)
            pil_img = tex.toImage()

            # Save the image
            filename = f"image_{constant_name}_shader.png"
            pil_img.save(filename)

            # Add sample to the README
            readme_file.write(f"| {constant_name} | ![Image]({filename}) |\n")
        except Exception:
            print(f"Error processing {constant_name}")
            readme_file.write(f"| {constant_name} | Erreur | \n")
