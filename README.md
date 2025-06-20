# VirtXStream 
VirtXStream is a tool that creates a virtual display on the X server using an NVIDIA GPU and streams it to a tablet (or any external device) over a VNC server. It provides a simple way to use a tablet as a second screen — either wirelessly or over USB — with configurable display parameters.

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

## How to use
### Clone the repo
```bash
# Clone the repo
git clone https://github.com/MertYksl03/VirtXStream.git
cd VirtXStream
```
### Run the program
```bash
python main.py 
```

### Creating dummy config
> [!CAUTION]  
>
> ## Disclaimer- Use at Your Own Risk
>
>*This feature of the program edits the system configuration files. This can create some unwanted situations or break your system.*
>

0. Run the program with sudo: ```sudo python main.py```
1. Click configure button at the below of Dummy Config label.
2. Enter the name of the nvidia x11 config file on your system (It's located at ```/usr/share/X11/xorg.conf.d/```) and select an available port.
3. Reboot your PC.
4. Click the button Enable
5. Boom!!! You created ur dummy config

### Configuring and Enabling Virtual display
To configure the virtual display click configure button that located at the bottom of Virtual Display sign. Then select a resolution and position that how you want to use your second display.    
Now you can enable your display with clicking the Enable button.

### ADB server (Android Only)
To connect and see your virtual display with _cable connection_, you can create an ADB server by clicking the Enable button that located at the below of ADB server sign.

### VNC server
Click the button called Enable to start Vnc server running. The app shows you the ip addresses and port. You can connect with any VNC viewer you choose.    
Clickin the Configure button allows you to configure some setting about VNC server such as port and do you want just USB connection. If you want to customize your VNC click this button.

