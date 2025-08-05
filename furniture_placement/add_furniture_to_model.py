import trimesh
from trimesh.creation import box
from trimesh.scene import Scene
from trimesh.visual import ColorVisuals

# Load base floor mesh
room_mesh = trimesh.load("coffee_table.glb")
room_bounds = room_mesh.bounds
min_corner, max_corner = room_bounds
room_width = max_corner[0] - min_corner[0]
room_depth = max_corner[1] - min_corner[1]

# Room dimensions
floor_thickness = 0.1
wall_height = 2.8
wall_thickness = 0.1
room_center = [
    (min_corner[0] + max_corner[0]) / 2,
    (min_corner[1] + max_corner[1]) / 2,
    0
]

# Helper to create colored geometry
def create_colored_box(extents, position, color_rgb):
    obj = box(extents=extents)
    obj.apply_translation(position)
    obj.visual = ColorVisuals(obj, face_colors=color_rgb + [255])
    return obj

# Create four walls
walls = []

# Left wall
walls.append(create_colored_box(
    (wall_thickness, room_depth, wall_height),
    [min_corner[0] - wall_thickness / 2, room_center[1], wall_height / 2],
    [220, 220, 220]
))

# Right wall
walls.append(create_colored_box(
    (wall_thickness, room_depth, wall_height),
    [max_corner[0] + wall_thickness / 2, room_center[1], wall_height / 2],
    [220, 220, 220]
))

# Back wall
walls.append(create_colored_box(
    (room_width, wall_thickness, wall_height),
    [room_center[0], max_corner[1] + wall_thickness / 2, wall_height / 2],
    [220, 220, 220]
))

# Front wall
walls.append(create_colored_box(
    (room_width, wall_thickness, wall_height),
    [room_center[0], min_corner[1] - wall_thickness / 2, wall_height / 2],
    [220, 220, 220]
))

# Furniture: Bed, Sofa, Table, Ceiling Light
bed = create_colored_box((2.0, 1.6, 0.5),
                         [min_corner[0] + 1.1, max_corner[1] - 1.2, 0.25],
                         [200, 100, 100])  # Reddish

sofa = create_colored_box((1.8, 0.8, 0.5),
                          [max_corner[0] - 2.0, min_corner[1] + 1.2, 0.25],
                          [100, 200, 100])  # Greenish

table = create_colored_box((1.2, 0.7, 0.4),
                           [room_center[0], room_center[1], 0.2],
                           [100, 100, 200])  # Bluish

light = create_colored_box((0.2, 0.2, 0.1),
                           [room_center[0], room_center[1], 2.5],
                           [255, 255, 150])  # Yellow ceiling light

# Window 1 (in back wall)
window1 = create_colored_box((1.0, 0.05, 1.0),
                             [room_center[0] - 1.5, max_corner[1] + wall_thickness / 2 + 0.01, 1.5],
                             [180, 220, 255])  # Light blue glass look

# Window 2 (in right wall)
window2 = create_colored_box((0.05, 1.0, 1.0),
                             [max_corner[0] + wall_thickness / 2 + 0.01, room_center[1] - 1.2, 1.5],
                             [180, 220, 255])  # Light blue

# Door (in front wall)
door = create_colored_box((1.0, 0.05, 2.2),
                          [room_center[0] + 1.5, min_corner[1] - wall_thickness / 2 - 0.01, 1.1],
                          [139, 69, 19])  # Brown door

# Build scene
scene = Scene()
scene.add_geometry(room_mesh, node_name="Floor")
scene.add_geometry(bed, node_name="Bed")
scene.add_geometry(sofa, node_name="Sofa")
scene.add_geometry(table, node_name="Table")
scene.add_geometry(light, node_name="CeilingLight")
scene.add_geometry(window1, node_name="Window1")
scene.add_geometry(window2, node_name="Window2")
scene.add_geometry(door, node_name="Door")

for i, wall in enumerate(walls):
    scene.add_geometry(wall, node_name=f"Wall_{i+1}")

# Export to GLB
scene.export("room_with_furniture.glb")
print("GLB created with walls, windows, door, and furniture.")
