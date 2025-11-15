"""
IMAGES -> PDF
Example of usage: python3 to_pdf --path ~/data/ --resize 0.3
"""
from PIL import Image
import os
import time
import argparse

IMAGE_PATH = '~/data/'
OUT_FILENAME = 'Result.pdf'
RESIZE_RATIO = 1
ROTATE_ANGLE = 0


def get_items(path):
    items = os.listdir(path)
    items = ["/".join([path, i]) for i in sorted(items)]
    items = [i for i in items if os.path.isfile(i)]
    items = [i for i in items if i.endswith('.jpg') or i.endswith('.png')]
    print("Found images:", items, "\n")
    return items


def resize(image, resize_ratio):
    if resize_ratio != 1:
        image = image.resize((int(image.size[0]*resize_ratio), int(image.size[1]*resize_ratio)), Image.LANCZOS)
    return image


def rotate(image, rotate_angle):
    if rotate_angle != 0:
        image = image.rotate(rotate_angle, expand=True)
    return image


def create_pdf(image_paths, out_filename=OUT_FILENAME, resize_ratio=RESIZE_RATIO, rotate_angle=ROTATE_ANGLE):
    if not image_paths:
        print("No image paths found.")
        return

    images = [Image.open(i) for i in image_paths]
    t1 = time.perf_counter()
    print("Conversion...")
    images = [i.convert('RGB') for i in images]
    t2 = time.perf_counter()
    print("... Took:", t2 - t1)
    print("Resizing...")
    images = [resize(i, resize_ratio) for i in images]
    images = [rotate(i, rotate_angle) for i in images]
    out = os.path.split(image_paths[0])[0] + "/" + out_filename
    print("Saving...", out)
    images[0].save(
        out,
        'PDF',
        resolution=100.00,
        save_all=True,
        append_images=images[1:]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert set of images to single PDF")
    parser.add_argument("--path", help="path to images to be converted, default: ~/data/")
    parser.add_argument("--resize", help="resize image ratio, default: 1, no resize", type=float)
    parser.add_argument("--rotate", help="rotate image (in degrees), default: 0, no rotation", type=int)
    args = parser.parse_args()
    path_to_imgs = args.path and args.path or IMAGE_PATH
    resize_ratio = args.resize and args.resize or RESIZE_RATIO
    rotate_angle = args.rotate and args.rotate or ROTATE_ANGLE
    items = get_items(path_to_imgs)
    create_pdf(items, OUT_FILENAME, resize_ratio, rotate_angle)
