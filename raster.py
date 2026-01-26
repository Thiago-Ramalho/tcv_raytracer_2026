import argparse
import importlib
from itertools import product

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def main(args):

    # load scene from file args.scene
    scene = importlib.import_module(args.scene).Scene()
    camera = scene.camera
    img_width = camera.img_width
    img_height = camera.img_height
    image = np.zeros((img_height, img_width, 3)) # create tensor for image: RGB

    # for each pixel, determine if it is inside any primitive in the scene
    # use cartesian product for efficiency
    for i, j in tqdm(product(range(img_height), range(img_width)), total=img_height*img_width):
        # middle of pixel coordinates
        x = j + 0.5
        y = i + 0.5
        # set background color
        image[i, j] = list(scene.background.as_list())
        # ray from camera
        ray = camera.ray(x, y)
        # if point is inside any primitive, set pixel color to that primitive's color
        for primitive, color in scene:
            hit_rec = primitive.hit(ray)
            if hit_rec.hit:
                # Simple shading: use the red channel as intensity
                intensity = max(0, hit_rec.normal.dot((scene.lights[0].position - hit_rec.point).normalize()))
                image[i, j] = [c * intensity for c in color.as_list()]
                break  # Stop at the first primitive that contains the point

    # invert lines for correct orientation
    image = np.flipud(image)
    # save image as png using matplotlib
    plt.imsave("output.png", image, vmin=0, vmax=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Raster module main function")
    parser.add_argument('-s', '--scene', type=str, help='Scene name', default='ball_scene')
    args = parser.parse_args()

    main(args)