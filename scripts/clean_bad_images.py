from PIL import Image
from glob import glob
import os

images = glob("data/train/images/*/*.jpg")
for image in images:
    try:
        im = Image.open(image)
        im.verify()
    except OSError:
        print(f"removing bad image: {image}")
        os.remove(image)