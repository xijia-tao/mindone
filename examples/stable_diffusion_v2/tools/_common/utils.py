"common utility functions and classes"
import os
from functools import partial

from ldm.util import is_old_ms_version
from PIL import Image

from mindspore import ops

# get L2 norm operator
if not is_old_ms_version("2.0.0-alpha"):
    L2_norm_ops = partial(ops.norm, ord=2, dim=1, keepdim=True)
else:
    L2_norm_ops = partial(ops.norm, p=2, axis=1, keep_dims=True)


def load_images(paths):
    # load images
    images = []
    if os.path.isdir(paths) and os.path.exists(paths):
        paths = [
            os.path.join(root, file)
            for root, _, file_list in os.walk(os.path.join(paths))
            for file in file_list
            if file.endswith(".jpg")
            or file.endswith(".png")
            or file.endswith(".jpeg")
            or file.endswith(".JPEG")
            or file.endswith("bmp")
        ]
        paths.sort()
        images = [Image.open(p) for p in paths]
        paths = paths
    else:
        images = [Image.open(paths)]
        paths = [paths]
    images = [image.resize((224, 224)) for image in images]
    return images, paths
