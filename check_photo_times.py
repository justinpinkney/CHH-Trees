from PIL import Image
from datetime import datetime
import sys
import glob
import os

def get_all_creation_times(directory):
    times = []
    files = glob.glob(directory + "/*.jpg")
    files.extend(glob.glob(directory + "/*.JPG"))
    for im_file in files:
        created_time = get_creation_time(im_file)
        times.append({"filename": os.path.basename(im_file),
                        "taken_at": created_time,
                        })
    return times

def get_creation_time(filename):
    im = Image.open(filename)
    exif = im._getexif()
    created_field = exif[0x9003]
    return datetime.strptime(created_field, "%Y:%m:%d %H:%M:%S")
