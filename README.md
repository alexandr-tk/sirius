# Sirius — Blender Add-on for Drone Show Design

> 🚧 **Status: Alpha / Active Development** — Core architecture implemented; pathfinding & export modules in progress.

An experimental Python-based Blender add-on for orchestrating drone shows.  
Designed to streamline the workflow of generating takeoff grids, previewing lighting effects, and (soon) exporting flight paths to CSV.

<img width="1152" height="765" alt="Sirius Demo" src="https://github.com/user-attachments/assets/6cf8b290-9b42-45c7-aed2-5b4ada0e3666" />

## 🌟 Features

### ✅ Implemented
* **Parametric Grid Generation:** Instantly spawn `N` drones in customizable grid formations (rows, columns, spacing).
* **Real-time Visualization:** Dynamic material assignments for LED color/emission testing in the viewport.
* **Modular Architecture:** Separated logic for Panels, Operators, and Property groups for easy extension.

### 🚧 Roadmap (In Development)
* **Collision-Free Pathfinding:** Integrating an algorithm (likely A*) to auto-calculate safe transitions between formations.
* **Swarm Safety Checks:** Velocity and proximity validation for 500+ agent swarms.
* **CSV Export Engine:** Export animation data (XYZ + Color) to industry-standard `.csv` formats for hardware uploads.

---
**Tech Stack:** Python · Blender API · 3D Visualization · Algorithm Design