from colorfilters import HSVFilter
import cv2 

img = cv2.imread('IMG_8617.JPG')
window = HSVFilter(img)
window.show()

print(f'lower: {window.lowerb} upper: {window.upperb}.')
