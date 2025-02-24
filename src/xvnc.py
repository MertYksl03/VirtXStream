import subprocess
import signal
import os
import sys
import re

# TODO: ask the user for sudo prevs. if not sudo then do not execute.
# TODO: create a function to create and change the xorg conf file (make it create a dummy driver)

def create_mode():
    # Get the model info from cvt (or gtf)
    model_process = subprocess.Popen(["cvt" , "1280", "800"], stdout=subprocess.PIPE, text=True)
    output, _ = model_process.communicate() # That "_" there because the communicate function returns stdout and stderr in this case we dont need the srderr

    # Truncate the string to get the usefull part
    for line in output.splitlines():
        if line.startswith("Modeline"):
            resolution_model = line.split("Modeline", 1)[1].strip()
            break
    
    # Extract text inside double quotes
    match = re.search(r'"([^"]+)"', resolution_model)
    if match:
        resolution_name = match.group(1)  # Get the captured text

    # splitting all the spaces 
    return resolution_model.split(), resolution_name

def plug_display():
    resolution = create_mode() # resolution[0] = mode of the resolution, resolution[1] = name of the resolution
    print(resolution[0])
    print(resolution[1])

    # asd = '"1280x800_60.00"   83.50  1280 1352 1480 1680  800 803 809 831 -hsync +vsync'
    # xrandr --newmode "1280x800_60.00"   83.50  1280 1352 1480 1680  800 803 809 831 -hsync +vsync
    # xrandr --addmode HDMI-1-0 "1280x800_60.00"
    # xrandr --output HDMI-1-0 --right-of eDP --mode 1280x800_60.00

    newmode_args = ['xrandr', '--newmode'] + resolution[0]
    temp = '"' + resolution[1] + '"'
    addmode_args = ['xrandr', '--addmode', 'HDMI-1-0', temp] 
    output_args = ['xrandr', '--output', 'HDMI-1-0', '--right-of', 'eDP', '--mode'] + resolution[1]

    # subprocess.run(['xrandr', '--newmode'] + resolution[0])
    # subprocess.run(['xrandr', '--addmode', 'HDMI-1-0'] + resolution[1])
    # subprocess.run(['xrandr', '--output', 'HDMI-1-0', '--right-of', 'eDP', '--mode'] + resolution[1])
    
    # subprocess.run(newmode_args)
    # subprocess.run(addmode_args)
    # subprocess.run(output_args)

    # print(addmode_args)
    # print(output_args)

def start_adb_server():
    subprocess.run(['adb', 'start-server'])
    subprocess.run(['adb', 'reverse', 'tcp:5900', 'tcp:5900'])

def start_vnc_server():
    plug_display()
    start_adb_server()
    
    # Start the x11vnc server in the background and capture its PID
    vnc_process = subprocess.Popen(['x11vnc', '--clip', '1280x800+1920+0', '-viewonly', '-repeat', '-rfbwait', '3000', '-once', '-allow', '127.0.0.1', '-nodpms', '-noxdamage'])
    def cleanup():
        print("Stopping x11vnc...")
        vnc_process.terminate()
        print("Killing ADB server...")
        subprocess.run(['adb', 'kill-server'])
        print("Turning off HDMI-1-0...")
        subprocess.run(['xrandr', '--output', 'HDMI-1-0', '--off'])
        print("Cleanup complete.")

    # Handle script exit and Ctrl+C
    signal.signal(signal.SIGINT, lambda sig, frame: cleanup())
    signal.signal(signal.SIGTERM, lambda sig, frame: cleanup())

    # Keep script running until x11vnc stops or Ctrl+C is pressed
    vnc_process.wait()

if __name__ == "__main__":
    # start_vnc_server()
    plug_display()