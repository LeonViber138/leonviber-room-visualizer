import trimesh
from trimesh.creation import box
from trimesh.visual import ColorVisuals
from trimesh.scene import Scene

# Room dimensions from DXF rules (example: 5m x 4m x 2.7m)
room_width = 5.0
room_depth = 4.0
wall_height = 2.7
wall_thickness = 0.1
floor_thickness = 0.05

# Colors
wall_color = [220, 220, 220, 255]
window_color = [150, 200, 255, 255]
door_color = [139, 69, 19, 255]
floor_color = [240, 240, 240, 255]

def create_colored_box(extents, position, color):
    mesh = box(extents=extents)
    mesh.apply_translation(position)
    mesh.visual = ColorVisuals(mesh, face_colors=color)
    return mesh

# Floor
floor = create_colored_box(
    (room_width, room_depth, floor_thickness),
    (room_width / 2, room_depth / 2, floor_thickness / 2),
    floor_color
)

# Four Walls
walls = []

# Left wall
walls.append(create_colored_box(
    (wall_thickness, room_depth, wall_height),
    (0, room_depth / 2, wall_height / 2),
    wall_color
))

# Right wall
walls.append(create_colored_box(
    (wall_thickness, room_depth, wall_height),
    (room_width, room_depth / 2, wall_height / 2),
    wall_color
))

# Back wall
walls.append(create_colored_box(
    (room_width, wall_thickness, wall_height),
    (room_width / 2, room_depth, wall_height / 2),
    wall_color
))

# Front wall
walls.append(create_colored_box(
    (room_width, wall_thickness, wall_height),
    (room_width / 2, 0, wall_height / 2),
    wall_color
))

# Window in back wall (centered)
window = create_colored_box(
    (1.2, 0.05, 1.0),
    (room_width / 2, room_depth + 0.03, 1.5),
    window_color
)

# Door in front wall (right side)
door = create_colored_box(
    (0.9, 0.05, 2.2),
    (room_width - 1.0, -0.03, 1.1),
    door_color
)

# Build scene
scene = Scene()
scene.add_geometry(floor, node_name="Floor")

for i, wall in enumerate(walls):
    scene.add_geometry(wall, node_name=f"Wall_{i+1}")

scene.add_geometry(window, node_name="Window")
scene.add_geometry(door, node_name="Door")

# Export
scene.export("resources/empty_room.glb")
print("Empty room GLB generated at 'resources/empty_room.glb'")
