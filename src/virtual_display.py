import subprocess
import shutil

class VirtualDisplay:
    # Global variables
    status = None
    active_resolution = None
    width = None
    height = None
    position = None

    def __init__(self):
        self.port_name = None          # The port that virtaul display is "connected" to (It is look like unnecessary but it is.)
        self.resolutions = []          
        self.status = False

    def plug_virtual_display(self, main_port_name, port_name):

        self.port_name = port_name

        # Check for dependencies
        if not shutil.which("gtf"):
            return False, "gtf program not found"
        if not shutil.which("xrandr"):
            return False, "xrandr not found"
        
        # Check if the width or height or position are configured
        if self.width == None or self.height == None or self.position == None:
            # This should be changed. Not descriptive enough
            return False, "Virtual display did not initialized/configured"

        
        # If the vd doesn't have the wanted resolution create one 
        if self.check_resolutions() == False:
            # Create a mode with gtf program 
            mode_creation_program = "gtf"
            resolution_mode = self.create_mode(mode_creation_program, self.width, self.height, 60) # refresh rate is hardcoed as 60 
            # resolution[0] = modeline, resolution[1] = mode name with quotes, resolution[2] = mode name without quotes

            # Check if creating mode is succesfull or not 
            if resolution_mode == False:
                return False, "Couldn't create a resolution mode"

            create_command = f"xrandr --newmode {resolution_mode[0]}"
            add_command = f"xrandr --addmode {port_name} {resolution_mode[1]}" # this command requires mode name with quotes
            plug_command = f"xrandr --output {port_name} --{self.position} {main_port_name} --mode {resolution_mode[2]}" # this command requires mode name without quotes

            try: 
                # Create new mode to xrandr 
                subprocess.run(create_command.split()) # don't need to check
                # Add new mode to xrandr
                subprocess.run(add_command.split()) # don't need to check
            except Exception:
                return False, "Couldn't create a new resolution \nYou can try another resolution"
            
            # Add the new resolution to resolutions list
            resolution = resolution_mode[2]
            self.resolutions.append(resolution)

        else:
            # If the wanted resolution is already added
            resolution = f"{self.width}x{self.height}"
            plug_command = f"xrandr --output {port_name} --{self.position} {main_port_name} --mode {resolution}"

        try :
            # Plug the vd
            subprocess.run(plug_command.split(), check=True)
        except subprocess.CalledProcessError as e:
            return False, f"Failed to start the virtual display: \n{e}"

        self.active_resolution = resolution
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
    
    def check_resolutions(self):
        resolution = f"{str(self.width)}x{self.height}" # current resolution

        if resolution in self.resolutions:
            return True
        else:
            return False
    

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
    