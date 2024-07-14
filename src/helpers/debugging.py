"""
for debugging purposes only
"""

import os, json, sys
from PIL import Image
from helpers.settings import get_settings

resize_images = True

def print_maze(maze):
    for i in maze:
        print(i)

def resize_image(image_id, width, height, normal=True, hovered=True):
    if resize_images:
        settings = get_settings()
        theme_file = os.path.join(sys.path[0], settings['theme']['path'])
        file = open(theme_file, "r")
        contents = json.loads(file.read())
        file.close()
        images_folder = os.path.join(sys.path[0], "assets/images/")
        if (normal):
            image_file = contents[image_id]['images']['normal_image']['resource']
            img = Image.open(images_folder + image_file)
            img = img.resize((width, height))
            img = img.save(images_folder + image_file)
        if (hovered):
            image_file = contents[image_id]['images']['hovered_image']['resource']
            img = Image.open(images_folder + image_file)
            img = img.resize((width, height))
            img.save(images_folder + image_file)