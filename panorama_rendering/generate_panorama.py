import numpy as np
import pyrender
import trimesh
import cv2
import py360convert
import os

# ----------------- Look At Matrix -----------------
def create_look_at_matrix(eye, target, up):
    forward = (target - eye)
    forward /= np.linalg.norm(forward)

    right = np.cross(up, forward)
    right /= np.linalg.norm(right)

    true_up = np.cross(forward, right)
    true_up /= np.linalg.norm(true_up)

    mat = np.eye(4)
    mat[0, :3] = right
    mat[1, :3] = true_up
    mat[2, :3] = forward
    mat[:3, 3] = eye
    return mat

# ----------------- Settings -----------------
GLB_PATH = "resources/furnished_room.glb"
OUTPUT_DIR = "outputs"
PANORAMA_IMAGE = os.path.join(OUTPUT_DIR, "panorama_from_center.png")
CUBEMAP_SIZE = 512  # resolution of each face

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------- Load GLB -----------------
loaded = trimesh.load(GLB_PATH)
if isinstance(loaded, trimesh.Scene):
    mesh = loaded.dump(concatenate=True)
else:
    mesh = loaded

# ----------------- Create Scene -----------------
scene = pyrender.Scene(ambient_light=[0.3, 0.3, 0.3])  # add ambient light
scene.add(pyrender.Mesh.from_trimesh(mesh, smooth=False))

# Add a directional light
light = pyrender.DirectionalLight(color=np.ones(3), intensity=3.0)
scene.add(light, pose=np.eye(4))

# ----------------- Camera Center -----------------
bbox = mesh.bounds
center = [(bbox[0][i] + bbox[1][i]) / 2 for i in range(3)]
camera_pos = np.array(center)
camera_pos[2] += 1.5

renderer = pyrender.OffscreenRenderer(CUBEMAP_SIZE, CUBEMAP_SIZE)

# ----------------- Cube Faces -----------------
directions = {
    "front":  np.array([0, 1, 0]),
    "back":   np.array([0, -1, 0]),
    "left":   np.array([-1, 0, 0]),
    "right":  np.array([1, 0, 0]),
    "up":     np.array([0, 0, 1]),
    "down":   np.array([0, 0, -1]),
}

images = {}

for name, direction in directions.items():
    up_vec = np.array([0, 0, 1]) if name not in ["up", "down"] else np.array([0, 1, 0])
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 2.0)
    cam_pose = create_look_at_matrix(camera_pos, camera_pos + direction, up_vec)
    node = scene.add(camera, pose=cam_pose)
    color, _ = renderer.render(scene)
    images[name] = color
    scene.remove_node(node)

renderer.delete()

# ----------------- Assemble 3x4 Dice -----------------
H, W, _ = images["front"].shape
dice = np.zeros((H * 3, W * 4, 3), dtype=np.uint8)

dice[H:2*H, 0:W]     = images["left"]
dice[H:2*H, W:2*W]   = images["front"]
dice[H:2*H, 2*W:3*W] = images["right"]
dice[H:2*H, 3*W:4*W] = images["back"]
dice[0:H, W:2*W]     = images["up"]
dice[2*H:3*H, W:2*W] = images["down"]

# ----------------- Convert to Panorama -----------------
equirect = py360convert.c2e(dice, 1024, 2048)

# ----------------- Save Output -----------------
cv2.imwrite(PANORAMA_IMAGE, cv2.cvtColor(equirect, cv2.COLOR_RGB2BGR))
print(f"Panorama saved to '{PANORAMA_IMAGE}'")
