import trimesh
from trimesh.creation import box
from trimesh.visual import ColorVisuals
from trimesh.scene import Scene

# Room size (same as before)
room_width = 5.0
room_depth = 4.0
wall_height = 2.7
wall_thickness = 0.1
floor_thickness = 0.05

# Colors
wall_color = [220, 220, 220, 255]
floor_color = [240, 240, 240, 255]
window_color = [150, 200, 255, 255]
door_color = [139, 69, 19, 255]
bed_color = [200, 100, 100, 255]
sofa_color = [100, 200, 100, 255]
table_color = [100, 100, 200, 255]
light_color = [255, 255, 150, 255]
kitchen_color = [160, 160, 160, 255]

def create_colored_box(extents, position, color):
    mesh = box(extents=extents)
    mesh.apply_translation(position)
    mesh.visual = ColorVisuals(mesh, face_colors=color)
    return mesh

scene = Scene()

# Floor
floor = create_colored_box(
    (room_width, room_depth, floor_thickness),
    (room_width / 2, room_depth / 2, floor_thickness / 2),
    floor_color
)
scene.add_geometry(floor, node_name="Floor")

# Walls
walls = []
walls.append(create_colored_box((wall_thickness, room_depth, wall_height), (0, room_depth / 2, wall_height / 2), wall_color))  # Left
walls.append(create_colored_box((wall_thickness, room_depth, wall_height), (room_width, room_depth / 2, wall_height / 2), wall_color))  # Right
walls.append(create_colored_box((room_width, wall_thickness, wall_height), (room_width / 2, room_depth, wall_height / 2), wall_color))  # Back
walls.append(create_colored_box((room_width, wall_thickness, wall_height), (room_width / 2, 0, wall_height / 2), wall_color))  # Front

for i, wall in enumerate(walls):
    scene.add_geometry(wall, node_name=f"Wall_{i+1}")

# Window (Back wall)
window = create_colored_box(
    (1.2, 0.05, 1.0),
    (room_width / 2, room_depth + 0.03, 1.5),
    window_color
)
scene.add_geometry(window, node_name="Window")

# Door (Front wall)
door = create_colored_box(
    (0.9, 0.05, 2.2),
    (room_width - 1.0, -0.03, 1.1),
    door_color
)
scene.add_geometry(door, node_name="Door")

# Furniture: Bed, Sofa, Table, Light

# Bed (Back-left)
bed = create_colored_box(
    (2.0, 1.6, 0.5),
    (1.2, room_depth - 1.2, 0.25),
    bed_color
)
scene.add_geometry(bed, node_name="Bed")

# Sofa (Front-right)
sofa = create_colored_box(
    (1.8, 0.8, 0.5),
    (room_width - 1.5, 1.0, 0.25),
    sofa_color
)
scene.add_geometry(sofa, node_name="Sofa")

# Table (center)
table = create_colored_box(
    (1.2, 0.7, 0.4),
    (room_width / 2, room_depth / 2, 0.2),
    table_color
)
scene.add_geometry(table, node_name="Table")

# Ceiling Light
light = create_colored_box(
    (0.2, 0.2, 0.1),
    (room_width / 2, room_depth / 2, 2.5),
    light_color
)
scene.add_geometry(light, node_name="CeilingLight")

# Kitchen counter (left wall)
kitchen = create_colored_box(
    (2.0, 0.5, 0.9),
    (1.1, 0.6, 0.45),
    kitchen_color
)
scene.add_geometry(kitchen, node_name="Kitchen")

# Export
scene.export("resources/basic_furniture_room.glb")
print("Basic furniture room GLB saved at 'resources/basic_furniture_room.glb'")
