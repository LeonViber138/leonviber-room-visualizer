# LeonViber Room Visualizer

**LeonViber Room Visualizer** is a Python-based tool that transforms architectural DXF floor plans into 3D scenes, places furniture based on rules, and generates panoramic 360° previews of interior spaces. It’s designed as a foundational step in pipelines where further AI processing or high-quality rendering is applied.

---

## 🔧 Features

- **DXF to 3D Model Conversion**  
  Automatically reads `.dxf` architectural drawings and generates 3D geometry for rooms and walls using predefined rules.

- **Automatic Furniture Placement**  
  Places basic furniture items in rooms (e.g., beds, sofas, kitchen units) based on simple room logic without AI models.

- **Panorama Generation**  
  Renders 360° panoramas from the center of each room, outputting clean geometric previews for downstream use (e.g., AI-to-image).

---

## 🚀 How It Works

1. **Phase 1 – DXF Parsing and 3D Generation**
   - Parses DXF files using `ezdxf`
   - Builds 3D models of walls and rooms using `trimesh` and `cadquery`
   - Exports `.glb` 3D models for further use

2. **Phase 2 – Furniture Placement**
   - Analyzes parsed geometry and applies fixed logic to place furniture
   - Furniture is added as simple blocks to visualize layout intent

3. **Phase 3 – Panorama Rendering**
   - Loads `.glb` file
   - Places a virtual camera at the center of the room
   - Renders six directional views and stitches them into a 360° image using `py360convert`

---

## 🖼️ Output Samples

3D View (Top-down):  
<img width="959" height="509" alt="3d space wtih furniture" src="https://github.com/user-attachments/assets/d58d58d0-2158-4166-a1d7-7d83d51b0eaf" />

## 🛠️ Installation

Make sure you have **Python 3.10+** installed. Then run:

```bash
pip install -r requirements.txt

▶️ Running the Project
Phase 1 – Generate 3D Model from DXF
python Phase_1_DXF_to_3D_Model/build_3d_model_from_dxf.py

Phase 2 – Add Furniture
python Phase_2_Furniture_Placement/add_furniture_to_model.py

Phase 3 – Generate Panorama
python Phase_3_Panorama_Rendering/generate_panorama.py
