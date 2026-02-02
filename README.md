<div align="center">
  <img src="assets/logo.png" alt="Sirius Logo" width="120" height="auto" />
  
  <h1>Sirius</h1>
  
  <p>
    <strong>Open-source drone show orchestration tool for Blender</strong>
  </p>

  <p>
    <a href="https://github.com/alexandr-tk/sirius/graphs/contributors">
      <img src="https://img.shields.io/github/contributors/alexandr-tk/sirius" alt="Contributors" />
    </a>
    <a href="https://github.com/alexandr-tk/sirius/blob/main/LICENSE">
      <img src="https://img.shields.io/github/license/alexandr-tk/sirius" alt="License" />
    </a>
  </p>

  <h4>
    🚧 Status: Alpha / Active Development 🚧
  </h4>
</div>

<br />

## Features

### Implemented
* **Parametric Grid Generation:** Instantly spawn `N` drones in customizable grid formations (rows, columns, spacing).
* **Real-time Visualization:** Dynamic material assignments for LED color/emission testing in the viewport.
* **Modular Architecture:** Separated logic for Panels, Operators, and Property groups for easy extension.

### Roadmap (In Development)
* **Collision-Free Pathfinding:** Integrating an algorithm (likely A*) to auto-calculate safe transitions between formations.
* **Swarm Safety Checks:** Velocity and proximity validation for 500+ agent swarms.
* **CSV Export Engine:** Export animation data (XYZ + Color) to industry-standard `.csv` formats for hardware uploads.

**Tech Stack:** Python · Blender API · 3D Visualization · Algorithm Design
