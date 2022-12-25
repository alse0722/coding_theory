from lzw import LZW
import os
import sys
import numpy as np
import matplotlib.image as mpimg

print("0 - Сжатие, 1 - Расжатие")
oper = input()
if oper == "0":
    compressor = LZW('studies\\tkisi\\sample.tif')
    compressor.compress()
    img = mpimg.imread('studies\\tkisi\\sample.tif')
    size_origin = os.stat('studies\\tkisi\\sample.tif').st_size
    size_compress = os.stat('Compressed/sample_compressed.lzw').st_size
    print("Коэффициент сжатия: ")
    print(round(size_compress / size_origin, 3))
    width = np.size(img, 1)
    height = np.size(img, 0)
    quality = (101 - ((width * height) * 3) / size_compress)
    print("Качество сжатия: " + str(quality))
if oper == "1":
    decompressor = LZW('Compressed\sample_compressed.lzw')
    decompressor.decompress()
