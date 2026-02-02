<a name="readme-top"></a>

<div align="center">
  <a href="https://github.com/alexandr-tk/sirius">
    <img src="assets/logo.png" alt="Logo" width="120" height="120">
  </a>

  <h3 align="center">Sirius</h3>

  <p align="center">
    Open-source drone show orchestration tool for Blender
    <br />
    <a href="https://github.com/alexandr-tk/sirius/issues">Report Bug</a>
    ·
    <a href="https://github.com/alexandr-tk/sirius/issues">Request Feature</a>
  </p>
</div>

<div align="center">
  <a href="https://github.com/alexandr-tk/sirius/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/alexandr-tk/sirius?style=for-the-badge" alt="Contributors" />
  </a>
  <a href="https://github.com/alexandr-tk/sirius/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/alexandr-tk/sirius?style=for-the-badge" alt="License" />
  </a>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#features">Features</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

**Sirius** is a modular add-on designed to bring professional drone show orchestration capabilities directly into the Blender viewport. It aims to bridge the gap between artistic animation and hardware deployment by providing tools for parametric generation, swarm safety validation, and data export.

The project is currently in **Alpha** status and under active development.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
* [![Blender](https://img.shields.io/badge/Blender-E87D0D?style=for-the-badge&logo=blender&logoColor=white)](https://www.blender.org/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

* Blender 3.6 or 4.0+
* Basic understanding of Blender's Python API (if contributing)

### Installation

1. Download the latest release `.zip` file from the releases page (or clone the repository).
2. Open Blender.
3. Go to **Edit > Preferences > Add-ons**.
4. Click **Install...** and select the downloaded `.zip` file.
5. Enable the add-on by checking the box next to **Sirius**.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Features

The core architecture focuses on modularity, separating logic for Panels, Operators, and Property groups to allow for easy extension.

* **Parametric Grid Generation:** Instantly spawn drones in customizable grid formations (rows, columns, spacing).
* **Real-time Visualization:** Dynamic material assignments for LED color and emission testing directly in the viewport.
* **Modular Architecture:** Clean code structure designed for open-source contribution and scalability.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

- [x] **Parametric Grid Generation**
- [x] **Real-time LED Visualization**
- [ ] **Collision-Free Pathfinding:** Integration of A* algorithms to auto-calculate safe transitions between formations.
- [ ] **Swarm Safety Checks:** Velocity and proximity validation for 500+ agent swarms.
- [ ] **CSV Export Engine:** Export animation data (XYZ + Color) to industry-standard formats for hardware uploads.

See the [open issues](https://github.com/alexandr-tk/sirius/issues) for a full list of proposed features and known issues.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

**Alex Tkachyov** - [LinkedIn](https://linkedin.com/in/alexandr-tkachyov)

Project Link: [https://github.com/alexandr-tk/sirius](https://github.com/alexandr-tk/sirius)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
