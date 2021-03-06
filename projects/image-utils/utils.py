""" utility for image padding to a certain size, rotate or flip """
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from random import choice
import cv2
import matplotlib.pyplot as plt



def padding(img, size):
    '''resize image with unchanged aspect ratio using padding'''
    img_w, img_h = img.shape[1], img.shape[0]
    w, h = size
    new_w = int(img_w * min(w/img_w, h/img_h))
    new_h = int(img_h * min(w/img_w, h/img_h))
    resized_image = cv2.resize(img, (new_w, new_h), interpolation = cv2.INTER_CUBIC)
    canvas = np.full((h, w, 3), 128)
    canvas[(h-new_h)//2:(h-new_h)//2 + new_h,(w-new_w)//2:(w-new_w)//2 + new_w, :] = resized_image
    return canvas


def resize(img, size):
    img = img.resize(size, Image.BICUBIC)
    return img

def rotate(img, angle):
    img = img.rotate(angle, resample=Image.BICUBIC)
    return img

def blur(img):
    return img.filter(ImageFilter.SMOOTH)

def pixel_replace(image, threshold, replace, larger=False):
    """replace certain pixel
    Args:
        image: PIL.Image object
        threshold: threshold value
        replace: replace value
        larger: choose whether > or <

    Returns:
        A new PIL.Image object
    """
    image = np.array(image)
    if larger:
        image = np.where(image > threshold, replace, image)
    else:
        image = np.where(image < threshold, replace, image)
    return Image.fromarray(image)


def add_spot(image, num, color):
    """
    Args:
         image: PIL.Image object
         num: number of spot
         color: color of spot

    Returns:
        spotted_image PIL.Image object
    """
    data = np.array(image)

    try:
        height, width, channels = data.shape
    except:
        height, width = data.shape

    all_pos = [[i, j] for i in range(height) for j in range(width)]
    np.random.shuffle(all_pos)
    use_pos = all_pos[:num]
    for (x, y) in use_pos:
        data[x][y] = color
    img = Image.fromarray(data)
    return img


def rotate(image, resample=None, angle=None):
    if angle is None:
        angle = np.random.randint(-15, 15)
    if resample is None:
        resample = Image.BICUBIC
    image = image.rotate(angle, resample)
    return image


def remove_dark(img, fill):
    data = np.array(img)
    data_ = np.where(data==0, fill, data)
    img_ = Image.fromarray(data_)
    return img_

def add_arc(img):
    dr = ImageDraw.Draw(img)
    randint = np.random.randint(0, 2)
    fillcolors = [(122, 64, 48), (116, 42, 31), (90, 86, 48), (92, 63, 33), (80, 60, 71)]
    c = choice(fillcolors)
    offset = np.random.randint(-10, 10)
    if randint == 0:
        dr.arc([0, 0+offset, 140, 44], 50, -200, fill=c)
    elif randint == 1:
        dr.line((0, 20+offset, 140, 20), width=2, fill=c)
    elif randint == 2:
        dr.line((0, 20+offset, 100, 20), width=2, fill=c)
        
    return img

def add_triangle(imgdata, num=1, color=0):
    """
        y = (ax + theta) + A
        x -- width
        y -- height
    """
    height, width = imgdata.shape[:2]
    A = height // 2
    theta = np.random.randint(-90, 90)
    w = 2 * np.pi * num / width
    xs = list(range(width))
    ys = [int(A * np.sin(x * w + theta)) for x in xs]
    
    for (x, y) in zip(xs, ys):
        try:
            imgdata[y][x-1:x+1] = color
        except:
            imgdata[y][x] = color
    return imgdata


if __name__ == '__main__':
    img = Image.new('RGB', (100, 40), color=(255, 255, 255))
    data = np.array(img)
    data2 = add_triangle(data, num=3)
    img2 = Image.fromarray(data2)
    img2.save('test.png')