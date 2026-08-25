# 🟣 Proyecto Violeta — Autonomous Companion Drone for Women's Safety

An autonomous aerial companion drone designed to enhance personal safety in urban environments. Built on a **3DR Solo** platform with a **Raspberry Pi 4** as companion computer, running **ROS 2 Jazzy** and a real-time computer vision pipeline using **PyTorch** and **DroneKit**.

---

## 🚀 Overview

Proyecto Violeta is a robotics + AI system that enables a drone to autonomously detect and follow a person, providing aerial oversight in situations where personal safety may be at risk. The system includes a **web-based mission control interface** accessible from any device on the local network.

**Key capabilities:**
- Real-time person detection and tracking via computer vision
- Autonomous follow mode using GPS navigation (DroneKit + MAVLink)
- Live telemetry dashboard (position, battery, armed state, flight mode)
- Web UI with Flask + Socket.IO — accessible from a phone or laptop
- Edge inference on Raspberry Pi 4 (no cloud dependency)

---

## 🛠️ Hardware Requirements

| Component | Description |
|---|---|
| 3DR Solo | Main drone platform with Open Solo 4 firmware |
| Raspberry Pi 4 | Companion computer (Ubuntu 24.04) |
| MicroSD ≥ 8GB (Class 10) | For Raspberry Pi OS |
| LiPo 4S battery | Fully charged before any operation |
| Ethernet cable | For initial network setup |

---

## 🧰 Tech Stack

- **ROS 2 Jazzy** + **MAVROS** — drone communication layer
- **DroneKit** — Python API for vehicle control via MAVLink
- **PyTorch** — computer vision model for person detection
- **Flask** + **Flask-SocketIO** — real-time web interface
- **OpenCV** — image processing pipeline
- **Python 3**

---

## 📁 Repository Structure

```
Violeta-Dron/
├── solo_guard_dk3.py     # Main script: vision pipeline, follow logic, web UI
├── manual_violeta.md     # Full implementation manual (Spanish)
└── README.md
```

---

## ⚙️ Setup & Installation

See [`manual_violeta.md`](./manual_violeta.md) for the full step-by-step guide, which covers:

1. Installing Open Solo 4 firmware on the 3DR Solo
2. Raspberry Pi 4 OS setup and SSH configuration
3. ROS 2 Jazzy + MAVROS installation
4. Python dependencies
5. Network configuration (drone ↔ Raspberry Pi ↔ laptop)
6. Running the system and using the web interface
7. Flight procedures and troubleshooting

---

## ▶️ Quick Start

```bash
# On the Raspberry Pi, once all dependencies are installed:
python3 solo_guard_dk3.py
```

Then open a browser on any device connected to the same network and navigate to:
```
http://<raspberry-pi-ip>:5000
```

---

## ⚠️ Safety Notes

- Always ensure the LiPo battery is **fully charged** before flashing firmware — a power loss mid-flash can corrupt the SD card (see manual section 3 for recovery steps).
- Test all autonomous flight logic in **simulation or a safe open area** before real deployment.
- This project is a research and academic prototype. Always follow local drone regulations.

---

## 👩‍💻 Authors

**Camila Vargas Medorio** — Robotics & Telecommunications Engineering, UDLAP  
[camilavargasmedorio@icloud.com](mailto:camilavargasmedorio@icloud.com)

---

## 📌 Status

🔬 Active development — academic research project, UDLAP 2026
