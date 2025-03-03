import subprocess
import shutil

class VirtualDisplay:
    # Global variables
    status = None
    active_resolution = None
    width = None
    height = None
    position = None

    def __init__(self, port_name):
        # self.app = app                               # The referance to app object 
        # self.main_port_name = self.app.main_port     # The port that main display is connected to
        # self.port_name = self.app.port_name          # The port that virtaul display is "connected" to
        self.port_name = port_name
        self.status = False

    def plug_virtual_display(self,main_port_name,port_name):

        # Check for dependencies
        if not shutil.which("cvt"):
            return False, "cvt program not found"
        if not shutil.which("xrandr"):
            return False, "xrandr not found"
        
        # Check if the width or height or position are configured
        if self.width == None or self.height == None or self.position == None:
            # This should be changed. Not descriptive enough
            return False, "Virtual display did not configured"


        # Create a mode with cvt program 
        mode_creation_program = "cvt"
        resolution = self.create_mode(mode_creation_program, self.width, self.height, 60) # refresh rate is hardcoed as 60 
        # resolution[0] = modeline, resolution[1] = mode name with quotes, resolution[2] = mode name without quotes

        # Check if creating mode is succesfull or not 
        if resolution == False:
            return False, "Couldn't create a mode"
        

        create_command = f"xrandr --newmode {resolution[0]}"
        add_command = f"xrandr --addmode {port_name} {resolution[1]}" # this command requires mode name with quotes
        plug_command = f"xrandr --output {port_name} --{self.position} {main_port_name} --mode {resolution[2]}" # this command requires mode name without quotes

        try :
            # Create new mode to xrandr 
            subprocess.run(create_command.split()) # dont need to check
            # Add new mode to xrandr
            subprocess.run(add_command.split()) # dont need to check
            # Plug the new mode 
            subprocess.run(plug_command.split(), check=True)
        except subprocess.CalledProcessError as e:
            return False, f"Failed to configure display: \n{e}"

        self.active_resolution = resolution[2]
        self.status = True
        return True, "Display configured succesfully"



    def unplug_virtual_display(self):
        try:
            # Unlug the virtaul display (does not render)
            unplug_command = f"xrandr --output {self.port_name} --off"
            subprocess.run(unplug_command.split(), check=True)
        except subprocess.CalledProcessError as e:
            return False, f"Failed to disconnect virtual display \n{e}"

        self.active_resolution = None
        self.status = False
        return True, "Virtual display is disconnected"

    def create_mode(self, program, width ,height, refresh_rate):
        mode_process = None
        width = str(width)
        height = str(height)
        refresh_rate = str(refresh_rate)
        
        try:
            mode_process = subprocess.Popen([program , width, height, refresh_rate], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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