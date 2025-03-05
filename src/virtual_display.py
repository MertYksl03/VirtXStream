import subprocess
import shutil

class VirtualDisplay:
    # Global variables
    status = None
    active_resolution = None                # The resolution that is currently actived
    resolution = None                       # The resolution that will be actived
    position = None

    def __init__(self):
        self.port_name = None          # The port that virtaul display is "connected" to (It is look like unnecessary but it is.)
        self.resolutions = []          
        self.status = False

    def plug_virtual_display(self, main_port_name, port_name):

        self.port_name = port_name

        plug_command =  f"xrandr --output {port_name} --{self.position} {main_port_name} --mode {self.resolution}"

        try :
            # Plug the vd
            subprocess.run(plug_command.split(), check=True)
        except subprocess.CalledProcessError as e:
            return False, f"Failed to start the virtual display: \n{e}"

        self.active_resolution = self.resolution
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
    

    