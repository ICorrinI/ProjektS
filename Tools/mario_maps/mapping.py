from PIL import Image
import numpy as np
import os

def png_to_parts_json(
    png_paths=[],
    json_path=""
):
    parts = {}

    for index, png_path in enumerate(png_paths, start=1):
        img = Image.open(png_path).convert("RGB")
        pixels = np.array(img)

        height, width, _ = pixels.shape

        color_to_id = {}
        id_to_color = {}
        next_id = 0

        world_map = []

        for y in range(height):
            row = []
            for x in range(width):
                rgb = tuple(int(v) for v in pixels[y, x])
                if rgb not in color_to_id:
                    color_to_id[rgb] = next_id
                    id_to_color[next_id] = rgb
                    next_id += 1
                row.append(color_to_id[rgb])
            world_map.append(row)

        parts[f"part{index}"] = {
            "width": width,
            "height": height,
            "palette": id_to_color,
            "map": world_map
        }

    # ---------- SCHÖNER JSON-EXPORT ----------
    with open(json_path, "w") as f:
        f.write("{\n  \"parts\": {\n")

        part_items = list(parts.items())
        for p_idx, (part_name, part) in enumerate(part_items):
            f.write(f'    "{part_name}": {{\n')
            f.write(f'      "width": {part["width"]},\n')
            f.write(f'      "height": {part["height"]},\n')

            # Palette
            f.write('      "palette": {\n')
            palette_items = list(part["palette"].items())
            for i, (pid, color) in enumerate(palette_items):
                r, g, b = color
                comma = "," if i < len(palette_items) - 1 else ""
                f.write(f'        "{pid}": [{r},{g},{b}]{comma}\n')
            f.write("      },\n")

            # Map
            f.write('      "map": [\n')
            for y, row in enumerate(part["map"]):
                comma = "," if y < len(part["map"]) - 1 else ""
                row_str = ",".join(str(v) for v in row)
                f.write(f"        [{row_str}]{comma}\n")
            f.write("      ]\n")

            comma = "," if p_idx < len(part_items) - 1 else ""
            f.write(f"    }}{comma}\n")

        f.write("  }\n}\n")

    print(f"✅ {len(parts)} Parts sauber formatiert exportiert → {json_path}")


# DIREKT AUFRUF
png_to_parts_json(
    png_paths=["1-1.png","1-2.png","1-3.png"],
    json_path="1.json"
)
