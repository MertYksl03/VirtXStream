import os
import sys
import subprocess

from utils.file_manager import FileManager

class Dummy:
    # dummy_activated = False
    __config_changed = False
    # __config_files_dir = "/usr/share/X11/xorg.conf.d/"
    __config_files_dir = "testfiles/"
    
    # Read the Nvidia config file
    __nvidia_conf = FileManager.read_file(__config_files_dir + "10-nvidia.conf")
    if __nvidia_conf == None:
        sys.exit(2)
        
    # Read the dummy template file
    __dummy_template = FileManager.read_file("dummy_template.txt")
    if __dummy_template == None:
        sys.exit(2)
    
    if FileManager.is_file_existed(__config_files_dir + "10-dummy.conf"):
        dummy_activated = True
    else:
        dummy_activated = False

    def initialize():
        #TODO
        print("allah")

    @staticmethod
    def check_dummy_activated():
        file_path = Dummy.__config_files_dir + "10-dummy.conf"
        if FileManager.is_file_existed(file_path):
            # check the data in the dummy ??? (maybe)
            Dummy.dummy_activated = True
        else: 
            Dummy.dummy_activated = False
   
    # def check_config_files():
    #     if Dummy.__config_changed:
    #         print("CONFIG FILE CHANGED")
    #         print("TO MAKE IT ACTIVATED PLEASE LOG OUT AND RELOGIN")
    #         print("OR REBOOT YOUR PC")
    #         # TODO: maybe this will but for now it doesn't
    #         # while True:
    #         #     user_input = input("Do you want to log out? (y / n): ")
    #         #     if user_input.lower() == "y" or user_input == "":
    #         #         print("Logging out...")
    #         #         Dummy.__config_changed = False
    #         #         os.system("pkill -u $USER")
    #         #     else:
    #         #         return

    @staticmethod
    def activate_dummy_config():
    
        # Get the port name from user
        port_name = Dummy.get_port_name()

        # Combine configurations
        virtual_monitor_config = Dummy.__nvidia_conf + "\n" + Dummy.__dummy_template.replace("*****", port_name) # Change the *s to a valid port name that user entered
        # print(virtual_monitor_config)
        file_path = Dummy.__config_files_dir + "10-dummy.conf"
        if FileManager.is_file_existed(file_path):
            return "Dummy is already activated"
        else :
            if FileManager.write_file(Dummy.__config_files_dir + "10-dummy.conf", virtual_monitor_config):
                # Double check if the dummy is activated 
                if Dummy.check_dummy_activated and FileManager.read_file(Dummy.__config_files_dir + "10-dummy.conf") == virtual_monitor_config:
                    Dummy.__config_changed = True
                    return True
            else:
                    return False
    
    # This function deletes the dummy config
    @staticmethod
    def deactive_dummy_config():
        file_path = Dummy.__config_files_dir + "10-dummy.conf"
        if not FileManager.is_file_existed(file_path):
            return "Dummy is allready deleted"
        else:
            try: 
                os.remove(file_path)
                Dummy.__config_changed = True
                return True
            except Exception as e:
                return f"Cant delete the Dummy config {e}"

    @staticmethod
    def get_port_name(): # This method probably will be changed when Gui gets developed
        # Run the xrandr command and capture the output
        result = subprocess.run(['xrandr'], stdout=subprocess.PIPE, text=True)
        output = result.stdout

        # Extract valid port names (lines that start with a port name)
        ports = []
        for line in output.splitlines():
            if " connected" in line or " disconnected" in line:
                port = line.split()[0]  # The first word is the port name
                ports.append(port)
        
        # FOR DEVELOPMENT PURPOSES 
        return ports[1] # index 1 is the port HDMI-1-0


        
        # while True:
        #     print("Enter the port name you want to connect your virtual monitor")
        #     print(f"Available Ports: {ports}")
        #     port_name = input("Enter the port name(For default hit enter [HDMI-1-0]): ").strip() # to trim the whitepspaceses
            
        #     # For development purposes 
        #     if not port_name:
        #         port_name = "HDMI-1-0" # default port
        #         return port_name
            
        #     #check the port name is valid or not 
        #     if port_name in ports:
        #         return port_name
        #     else: 
        #         print("INVALID PORT NAME")