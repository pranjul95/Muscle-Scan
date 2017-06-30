import cv2
import numpy as np
import argparse
import math

ap = argparse.ArgumentParser()
#Takes frontal ,lateral images (jpg,png,etc) with white background and height weight of the person as input

ap.add_argument("-i", "--image1", required=True,
                help="path to the file")
ap.add_argument("-i1","--image2",required = True,
                help="path to the second image file")
ap.add_argument("-H","--height", type=float, required=True,
                help="height of the person")
ap.add_argument("-W","--weight", type=float, required=True,
                help="weight of the person")

args = vars(ap.parse_args())
im_in1 = cv2.imread(args["image1"], cv2.IMREAD_GRAYSCALE)
im_in2 = cv2.imread(args["image2"], cv2.IMREAD_GRAYSCALE)

height = args["height"]
weight = args["weight"]


def output_image(im_in):
    blur = cv2.GaussianBlur(im_in, (11, 11), 0)
    ret4, im_th4 = cv2.threshold(blur, 250, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    im_floodfill = im_th4.copy()

    h, w = im_th4.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    cv2.floodFill(im_floodfill, mask, (0, 0), 255)

    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    im_out = im_th4 | im_floodfill_inv

    return im_out

def matrix(im_out):
    rows, cols = im_out.shape
    pixel_array_of_arrays = [[]]
    for i in xrange(rows):
        j = 0
        pixel_per_row_array = []
        while j in xrange(cols):
            p = 0
            while im_out[i][j] == 255 and j in xrange(cols-1):
                p += 1
                j += 1
            if p > 0:
                pixel_per_row_array.append(p)
            else:
                j += 1
        if pixel_per_row_array:
            pixel_per_row_array = list(set(pixel_per_row_array))
            pixel_per_row_array.sort()
            m = pixel_per_row_array[-1:]
            pixel_array_of_arrays.append(m)
    return pixel_array_of_arrays

def height_pix(pixel_array_of_arrays):
    height_pixels = 0
    for i in (pixel_array_of_arrays):
        if i:
            height_pixels += 1
    return height_pixels
def circum(pix1, pix2):
    pi = 3.14159
    m = (pi/2)*(1.5*(pix1+pix2) - (pix1*pix2)**0.5)
    return m

def sizes(im_in1,im_in2,height,weight):
    size = []

    im_out1 = output_image(im_in1)
    im_out2 = output_image(im_in2)

    pixel_array_of_arrays1 = matrix(im_out1)
    pixel_array_of_arrays2 = matrix(im_out2)

    height_pixels1 = height_pix(pixel_array_of_arrays1)
    height_pixels2 = height_pix(pixel_array_of_arrays2)

    ppm = height/height_pixels1

    neck = []
    for x in xrange(height_pixels1 / 10, height_pixels1 / 5):
        neck.append(pixel_array_of_arrays1[x])
    neck_major = min(neck)
    neck2 = []
    for x in xrange(height_pixels2/10, height_pixels2/5):
        neck2.append(pixel_array_of_arrays2[x])
    neck_minor = min(neck2)
    neck_circum = circum(neck_major[0], neck_minor[0]) * ppm

    # shoulder1 = []
    # shoulder2 = []
    # for x in xrange(height_pixels1/ 5, height_pixels1 * 4 / 10):
    #     y = x * height_pixels2 / height_pixels1
    #     shoulder1.append(pixel_array_of_arrays1[x])
    #     shoulder2.append(pixel_array_of_arrays2[y])
    # shoulder_major = max(shoulder1)
    # shoulder_minor = shoulder2[shoulder1.index(max(shoulder1))]
    # shoulder_circum = circum(shoulder_major[0], shoulder_minor[0])

    chest = []
    for x in xrange(height_pixels1 / 5, height_pixels1 * 4/10):
        y = x*height_pixels2/height_pixels1
        if pixel_array_of_arrays1[x][0] < pixel_array_of_arrays1[x - 1][0] - (35/62)*2*height_pixels1 and pixel_array_of_arrays1[x][0] < pixel_array_of_arrays1 [x + 1][0] + 5:
            m = circum(pixel_array_of_arrays1[x][0], pixel_array_of_arrays2[y][0])
            chest.append(m)
    chest_circum = max(chest) * ppm

    waist1 = []
    waist2 = []
    for x in xrange(height_pixels1*3/10, height_pixels1*6/10):
        y = x * height_pixels2/height_pixels1
        waist1.append(pixel_array_of_arrays1[x])
        waist2.append(pixel_array_of_arrays2[y])
    waist_minor = min(waist2)
    waist_major = waist1[waist2.index(min(waist2))]
    hip_minor = max(waist2)
    hip_major = waist1[waist2.index(min(waist2))]

    waist_circum = circum(waist_major[0], waist_minor[0])*ppm
    hip_circum = circum(hip_major[0], hip_minor[0])*ppm


    for x in xrange(height_pixels1*6 / 10, height_pixels1 * 8 / 10):
        while pixel_array_of_arrays1[x] > hip_major[0]/2 and x < height_pixels1*8/10:
            x += 1
    y = x * height_pixels2 / height_pixels1
    thigh_major = pixel_array_of_arrays1[x]
    thigh_minor = pixel_array_of_arrays2[y]

    thigh_circum = circum(thigh_major[0], thigh_minor[0])*ppm

    # calves1 = []
    # calves2 = []
    # for x in xrange(height_pixels1*8/10, height_pixels1*65/80):
    #     y = x*height_pixels2/height_pixels1
    #     calves1.append(pixel_array_of_arrays1[x])
    #     calves2.append(pixel_array_of_arrays2[y])
    #
    # calves_minor = max(calves2)
    # calves_major = calves1[calves2.index(max(calves2))]
    #
    # calves_circum = circum(calves_minor[0], calves_major[0])*ppm
    # print calves_major
    # print calves_minor
    # print calves_circum

    surface_area = 0.007184*(weight**0.428)*(height**0.723)

    bvi = surface_area*(51.44*(weight/height) + 15.3)

    print "male or female?"
    choice = raw_input("> ")

    if choice == "male":
        body_fat = 495/(1.0324-0.19077*(math.log10(waist_circum - neck_circum)) + 0.15456*(math.log10(height)))-450
    else:
        body_fat = 495/(1.29579 - 0.35004*(math.log10(waist_circum + hip_circum - neck_circum))+ 0.22100*(math.log10(height)))-450

    lean_mass_weight = weight*(1-body_fat/100)

    total_body_water = lean_mass_weight*0.73

    #printing everything
    print "Your Height: %r" % height
    print "Your Weight: %r" % weight
    print "Neck: %r" % neck_circum
   # print "Shoulder: %r" % shoulder_circum
    print "Chest: %r" % chest_circum
    print "Waist: %r" % waist_circum
    print "Hip: %r" % hip_circum
    print "Thigh: %r" % thigh_circum
    print "Your total body fat: %r" % body_fat
    print "Your lean mass weight: %r" % lean_mass_weight
    print "Your total body water: %r" % total_body_water
    print "Your Body volume index: %r" % bvi
    return size

size = sizes(im_in1, im_in2, height, weight)
