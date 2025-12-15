from PIL import Image
import numpy as np

def png_to_array_dynamic(file_path):
    img = Image.open(file_path).convert('RGB')
    pixels = np.array(img)
    
    color_to_number = {}  # speichert jede Farbe und die zugewiesene Zahl
    next_number = 0
    
    numbered_array = np.zeros((pixels.shape[0], pixels.shape[1]), dtype=int)
    
    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            rgb = tuple(pixels[y, x])
            if rgb not in color_to_number:
                color_to_number[rgb] = next_number
                next_number += 1
            numbered_array[y, x] = color_to_number[rgb]
    
    return numbered_array, color_to_number

# Beispielnutzung
file_path = 'Doodle.png'
array, mapping = png_to_array_dynamic(file_path)
print(array)
print("Farben-Zuordnung:", mapping)
