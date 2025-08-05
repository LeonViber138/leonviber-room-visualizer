import ezdxf
import json
import os

# Load the DXF file
file_path = "CoffeeTable.dxf"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"DXF file not found at: {file_path}")

doc = ezdxf.readfile(file_path)
msp = doc.modelspace()

# Parsed geometry output
geometry_data = {
    "lines": [],
    "lwpolylines": [],
    "circles": [],
    "arcs": [],
}

# Iterate over entities
for entity in msp:
    etype = entity.dxftype()

    if etype == "LINE":
        geometry_data["lines"].append({
            "start": [entity.dxf.start.x, entity.dxf.start.y, entity.dxf.start.z],
            "end": [entity.dxf.end.x, entity.dxf.end.y, entity.dxf.end.z],
            "layer": entity.dxf.layer
        })

    elif etype == "LWPOLYLINE":
        points = []
        for point in entity.get_points():
            x, y, *_ = point
            points.append([x, y])
        geometry_data["lwpolylines"].append({
            "points": points,
            "is_closed": entity.closed,
            "layer": entity.dxf.layer
        })

    elif etype == "CIRCLE":
        geometry_data["circles"].append({
            "center": [entity.dxf.center.x, entity.dxf.center.y, entity.dxf.center.z],
            "radius": entity.dxf.radius,
            "layer": entity.dxf.layer
        })

    elif etype == "ARC":
        geometry_data["arcs"].append({
            "center": [entity.dxf.center.x, entity.dxf.center.y, entity.dxf.center.z],
            "radius": entity.dxf.radius,
            "start_angle": entity.dxf.start_angle,
            "end_angle": entity.dxf.end_angle,
            "layer": entity.dxf.layer
        })

# Output to JSON
output_file = "parsed_geometry.json"
with open(output_file, "w") as f:
    json.dump(geometry_data, f, indent=4)

print(f"DXF parsed and saved to '{output_file}' successfully.")
