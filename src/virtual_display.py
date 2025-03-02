import os 
import subprocess
import time 

class VirtualDisplay:
    def __init__(self, app):
        self.app = app                               # The referance to app object 
        self.main_port_name = self.app.main_port     # The port that main display is connected to
        self.port_name = self.app.port_name          # The port that virtaul display is "connected" to


    def plug_virtual_display(self, width, height, main_port_name, position, port_name):
        
        # Create a mode with cvt program 
        mode_creation_program = "cvt"
        resolution = self.create_mode(mode_creation_program, width, height) 
        # resolution[0] = modeline, resolution[1] = mode name with quotes, resolution[2] = mode name without quotes

        # Check if creating mode is succesfull or not 
        if resolution == False:
            return False, "Couldn't create a mode"
        
        print (resolution)

        # Create new mode to xrandr 
        create_command = f"xrandr --newmode {resolution[0]}"
        subprocess.run(create_command.split())

        # Add new mode to xrandr
        add_command = f"xrandr --addmode {port_name} {resolution[1]}" # this command requires mode name with quotes
        subprocess.run(add_command.split())

        # Plug the new mode 
        plug_command = f"xrandr --output {port_name} --{position} {main_port_name} --mode {resolution[2]}" # this command requires mode name without quotes
        subprocess.run(plug_command.split())



    def unplug_virtual_display(self):
        # Unlug the virtaul display (does not render)
        unplug_command = f"xrandr --output {self.port_name} --off"
        subprocess.run(unplug_command.split())

    def create_mode(self, program, width ,height):
        mode_process = None
        width = str(width)
        height = str(height)
        
        try:
            mode_process = subprocess.Popen([program , width, height], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception:
            return False 
        
        output = mode_process.stdout

        for line in output:
            if "Modeline" in line:
                mode = line.replace("Modeline", "").strip()
            
        # Both of them needed for xrandr commands
        mode_name_1 = mode.split()[0] # Mode name that in quotes
        mode_name_2 = mode_name_1.replace('"', "") # Mode name without quotes 
        
        return  mode, mode_name_1, mode_name_2