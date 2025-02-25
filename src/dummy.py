import os
import sys
import subprocess

from utils.file_manager import FileManager

class Dummy:

    def __init__(self):
        self.__file_path = None
        self.__port_name = None
        self.__nvidia_conf = None
        self.__dummy_data = None
        self.__ports = []
        
        self.is_dummy_activated = False

    def initialize(self, file_path, port_name):
        self.__file_path = file_path
        self.__ports = self.get_ports()

        # TODO: I don't know what to do when the pprt is not valid
        # if not self.check_port_is_valid(self.__ports, self.__port_name):
            # sys.exit(2)
            
        
        self.__port_name = port_name

        # Read the files 
        self.__nvidia_conf = FileManager.read_file(file_path + "10-nvidia.conf")
        if self.__nvidia_conf == False:
            return False
        
        dummy_template = FileManager.read_file("dummy_template.txt")
        
        if dummy_template == False:
            return False

        # Create the dummy config data
        self.__dummy_data = self.__nvidia_conf + "\n" + dummy_template.replace("*****", port_name)

        # Check the dummmy is activated if it is then is_dummy_acitaved = True
        self.is_dummy_activated = self.check_dummy_activated()

        # If everything is ok then return True, meaning the initialize is succesfull
        return True

    def check_dummy_activated(self):
        file_path = self.__file_path + "10-dummy.conf"
        # Check if the file existed and the content of the file is same as it should be
        if FileManager.is_file_existed(file_path) and FileManager.read_file(file_path) == self.__dummy_data:
            return True
        else: 
            return False

    def activate_dummy_config(self):
        config_file_name = "10-dummy.conf"
        # Dont do a thing if the dummy is already activated
        if self.check_dummy_activated():
            return False
        
        # Create, write the dummy-config and check its content
        if FileManager.write_file(self.__file_path + config_file_name, self.__dummy_data) and self.check_dummy_activated():
            return True
        else :
            return False

    # This function deletes the dummy config
    def deactive_dummy_config(self):
        file_path =  self.__file_path + "10-dummy.conf"

        # Check if the config is already deleted
        if not FileManager.is_file_existed(file_path):
            return True # The file is deleted
        else:
            # Delete the file
            try: 
                os.remove(file_path)
                return True
            except:
                return False

    def get_ports(self):         
        # Run the xrandr command and capture the output
        result = subprocess.run(['xrandr'], stdout=subprocess.PIPE, text=True)
        output = result.stdout

        # Extract valid port names (lines that start with a port name)
        ports = []
        for line in output.splitlines():
            if " connected" in line or " disconnected" in line:
                port = line.split()[0]  # The first word is the port name
                ports.append(port)
        
        return ports
    
    def check_port_is_valid(self, ports, port_name):
        if port_name in ports:
            return True
        else:
            return False
