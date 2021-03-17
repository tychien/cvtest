from colorfilters import HSVFilter
import cv2 

img = cv2.imread('dolphin6.jpg')
window = HSVFilter(img)
window.show()

print(f'lower: {window.lowerb} upper: {window.upperb}.')
