#!/usr/bin/env python
#-*- coding: utf8 -*-

from PIL import Image
from color import Color
from octree_quantizer import OctreeQuantizer

filename = 'misti'

def main():
    image = Image.open(filename + '.png')
    pixels = image.load()
    width, height = image.size

    octree = OctreeQuantizer()

    # agregar colores al octree
    for j in range(height):
        for i in range(width):
            octree.add_color(Color(*pixels[i, j]))

    # 256 colores para imagen de salida de 8 bits por píxel
    palette = octree.make_palette(64)

    # crear paleta para 256 colores como máximo y guardar en archivo
    palette_image = Image.new('RGB', (8, 8))
    palette_pixels = palette_image.load()
    for i, color in enumerate(palette):
        palette_pixels[i % 8, i / 8] = (int(color.red), int(color.green), int(color.blue))
    palette_image.save(filename + '_palette.png')

    # guardar imagen de salida
    out_image = Image.new('RGB', (width, height))
    out_pixels = out_image.load()
    for j in range(height):
        for i in range(width):
            index = octree.get_palette_index(Color(*pixels[i, j]))
            color = palette[index]
            out_pixels[i, j] = (int(color.red), int(color.green), int(color.blue))
    out_image.save(filename + '_out.png')


if __name__ == '__main__':
    main()
