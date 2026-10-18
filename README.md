# 🕹️ learn_doom

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green?style=flat)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

A retro pseudo-3D raycasting engine written in pure Python using **Pygame**. Inspired by classic 90s first-person shooters like *Wolfenstein 3D* and *Doom*, this engine simulates a 3D environment out of a 2D grid matrix using mathematical ray projection.

---

## ✨ Key Features

- **⚡ Custom 3D Raycaster:** Renders a pseudo-3D world slice-by-slice across a 60° Field of View (FOV).
- **👁️ Fish-Eye Correction:** Applies cosine adjustment to correct fisheye distortion on flat wall surfaces.
- **🌫️ Distance-Based Shading:** Walls dynamically darken as depth increases, simulating atmospheric ambient lighting.
- **🎯 FPS Controls & Collision:** Supports continuous movement, strafing, turning, and wall collision detection.
- **🔫 Retro HUD Gun Overlay:** Draws a minimalist centered retro gun model over the rendered viewport.

---

## 📸 Preview

 +---------------------------------------------------+
 |                      [CEILING]                    |
 |                                                   |
 |        +-------+                 +-------+        |
 |        | WALL  |    [DEEP WALL]  | WALL  |        |
 |        | (Red) |      (Dark)     | (Red) |        |
 |        +-------+                 +-------+        |
 |                                                   |
 |                      [FLOOR]                      |
 |                        / \                        |
 |                       |===|  <- [WEAPON]          |
 +---------------------------------------------------+

---

## 🛠️ Requirements & Installation

### Prerequisites
* **Python 3.8+** installed on your machine.

### Installation

1. Clone or download this repository:
   git clone https://github.com/your-username/mini-doom-raycaster.git
   cd mini-doom-raycaster

2. Install the required dependency:
   pip install pygame

3. Launch the game:
   python main.py

---

## 🎮 Controls

| Action | Key / Control |
| :--- | :--- |
| **Move Forward / Back** | `W` / `S` or `Up` / `Down` |
| **Strafe Left / Right** | `A` / `D` |
| **Rotate Camera** | `Left` / `Right` Arrow Keys |
| **Exit Game** | Close Window (`X`) |

---

## 📂 Project Structure

├── main.py          # Main executable script containing raycasting engine & game loop
└── README.md        # Project documentation

---

## 🧮 How It Works

1. **Map Grid:** The level design uses a 2D list where `1` represents solid wall blocks and `0` represents empty space.
2. **Raycasting Loop:** Launches 120 individual rays across the player's 60° FOV.
3. **DDA / Ray Marching:** Steps outward in small increments until hitting a grid cell marked as `1`.
4. **Perspective Projection:** Calculates distance, adjusts for spherical curvature (`depth * cos(angle)`), and scales vertical wall slice rectangles accordingly.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for details.
