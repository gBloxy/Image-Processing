from PIL import Image
from processing import *

from processing.main import codes

REDUCE_FACTOR = 2

shaders = {}


# TODO: Get shaders from image-processing library
# Get all constants
def get_constants():
    global shaders

    for code in codes:
        constant_name = [name for name, value in globals().items() if value == code][0]
        shaders[code] = constant_name

    shaders = sorted(shaders.items(), key=lambda x: x[0])


# load the image with PIL
image = Image.open("image.png")
image = image.resize(
    (int(image.size[0] / REDUCE_FACTOR), int(image.size[1] / REDUCE_FACTOR)),
    Image.Resampling.LANCZOS,
)
get_constants()
with open("README.md", "w") as readme_file:
    # README header
    readme_file.write("# Shader results\n\n")
    readme_file.write("Here the samples results with applied shader effects.\n\n")
    readme_file.write("| Shader name | Image |\n")
    readme_file.write("| ------------- | ----- |\n")

    # Generate the samples
    for idx in range(1, len(shaders)):
        constant_name = shaders[idx][1]

        try:
            print(f"Processing {constant_name}")
            # Apply ther shader
            process = Process(idx)
            tex = process.run(image)
            pil_img = tex.toImage()

            # Save the image
            filename = f"image_{constant_name}_shader.png"
            pil_img.save(filename)

            # Add sample to the README
            readme_file.write(f"| {constant_name} | ![Image]({filename}) |\n")
        except Exception as e:
            print(e)
            print(f"Error processing {constant_name}")
            readme_file.write(f"| {constant_name} | Erreur | \n")
