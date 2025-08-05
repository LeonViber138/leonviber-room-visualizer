import ezdxf
import cadquery as cq
import trimesh
import math
import os

# Input and output
DXF_PATH = "CoffeeTable.dxf"
OUTPUT_PATH = "coffee_table.glb"
EXTRUDE_HEIGHT = 0.05  # 5 cm thickness for coffee table top

# Check file exists
if not os.path.exists(DXF_PATH):
    raise FileNotFoundError(f"DXF file not found: {DXF_PATH}")

# Load DXF
doc = ezdxf.readfile(DXF_PATH)
msp = doc.modelspace()

# Start CadQuery sketch
sketch = cq.Workplane("XY")

# Draw DXF geometry
for entity in msp:
    if entity.dxftype() == "LINE":
        start = entity.dxf.start
        end = entity.dxf.end
        sketch = sketch.moveTo(start.x, -start.y).lineTo(end.x, -end.y)

    elif entity.dxftype() == "ARC":
        center = entity.dxf.center
        radius = entity.dxf.radius
        start_angle = math.radians(entity.dxf.start_angle)
        end_angle = math.radians(entity.dxf.end_angle)

        # Calculate arc start and end points
        start_x = center.x + radius * math.cos(start_angle)
        start_y = center.y + radius * math.sin(start_angle)
        end_x = center.x + radius * math.cos(end_angle)
        end_y = center.y + radius * math.sin(end_angle)

        # Draw arc with correct curvature
        sketch = sketch.moveTo(start_x, -start_y).radiusArc((end_x, -end_y), -radius)

# Close shape and extrude
outline = sketch.close()
solid = outline.extrude(EXTRUDE_HEIGHT)

# Tessellate to mesh (convert Vector to list)
vertices, faces = solid.val().tessellate(tolerance=0.01)
vertices = [[v.x, v.y, v.z] for v in vertices]

# Create and export mesh
mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
mesh.export(OUTPUT_PATH)

print(f"3D model generated and saved as '{OUTPUT_PATH}'")
