from PIL import Image
import numpy as np
import pprint

def png_to_draw_function(
    file_path,
    function_name="draw_icon_custom",
    array_name="icon_array",
    color_name="icon_colors"
):
    img = Image.open(file_path).convert("RGB")
    pixels = np.array(img)

    color_to_number = {}
    number_to_color = {}
    next_number = 0

    numbered_array = np.zeros((pixels.shape[0], pixels.shape[1]), dtype=int)

    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            rgb = tuple(pixels[y, x])
            if rgb not in color_to_number:
                color_to_number[rgb] = next_number
                number_to_color[next_number] = rgb
                next_number += 1
            numbered_array[y, x] = color_to_number[rgb]

    print(f"\ndef {function_name}(screen, x_offset, y_offset):")
    print(f"    {array_name} = np.array([")

    for row in numbered_array:
        clean_row = [int(v) for v in row]
        print("    " + str(clean_row) + ",")

    print("    ])\n")

    print(f"    {color_name} = {{")
    for k, (r, g, b) in number_to_color.items():
        print(f"        {int(k)}: ({int(r)}, {int(g)}, {int(b)}),")
    print("    }\n")

    print(
        f"draw_icon(screen, x_offset, y_offset,pixel_array={array_name},color_mapping={color_name},pixel_size=s.PIXEL_WIDTH)"
    )


# Beispiel
png_to_draw_function(
    "Mario.png",
    function_name="draw_icon_mario"
)