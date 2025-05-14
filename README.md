# X-Vnc-Gui
X-Vnc-Gui is a tool that creates a virtual display on the X server using an NVIDIA GPU and streams it to a tablet (or any external device) over a VNC server. It provides a simple way to use a tablet as a second screen — either wirelessly or over USB — with configurable display parameters.

## Features
🖥️ Create virtual X display powered by NVIDIA GPUs using xrandr and xorg.conf.

📱 Stream to tablets or external devices via a built-in or user-defined VNC server.

🔧 Configure resolution, refresh rate, position, and other display settings easily.

🔌 Optional ADB server for streaming over USB using reverse port forwarding.

🐧 Works well on Linux systems with NVIDIA graphics and X11.

## Use Cases
Extend your desktop to an Android tablet over Wi-Fi or USB.

Use your tablet as a secondary monitor while preserving GPU acceleration.

Create headless virtual displays for rendering or testing.

## Requirements
- Linux with X11 (Xorg)
- NVIDIA proprietary drivers
- x11vnc
- python13

Optional: adb for USB streaming

## Getting Started
```bash
Copy
Edit
# Clone the repo
git clone https://github.com/MertYksl03/X-Vnc-Gui.git
cd X-Vnc-Gui

# Run the setup or main script
python main.py 
```
