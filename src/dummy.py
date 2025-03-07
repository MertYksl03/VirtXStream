import os
import sys
import subprocess

from utils.file_manager import FileManager

class Dummy:
    # Global variables
    file_path = None        # Holds the file path of Xorg config files
    port_name = None        # Holds the name of the display port (virtual display)
    main_port = None        # Holds the name of the main display port 
    status = None           # Holds the status 

    def __init__(self):
        # Private variables
        self.__nvidia_conf = None
        self.__dummy_data = None
        
        self.is_dummy_activated = False

    def initialize(self,file_path, port_name, main_port):
        self.file_path = file_path
        self.port_name = port_name
        self.main_port = main_port

        # Read the files 
        self.__nvidia_conf = FileManager.read_file(file_path + "10-nvidia.conf")
        if self.__nvidia_conf == False:
            return False, "Couldn't read nvidia config file. \nFile path might be wrong"
        
        dummy_template = FileManager.read_file("dummy_template.txt")
        
        if dummy_template == False:
            return False, "Couldn't read dummy_template.txt \nFile path might be wrong" 

        # Create the dummy config data
        self.__dummy_data = self.__nvidia_conf + "\n" + dummy_template.replace("*****", port_name)

        # Check the dummmy is activated if it is then is_dummy_acitaved = True
        self.is_dummy_activated = self.check_dummy_activated()

        self.status = self.check_status()

        # If everything is ok then return True, meaning the initialize is succesfull
        return True, " "

    def check_dummy_activated(self):
        file_path = self.file_path + "10-dummy.conf"
        # Check if the file existed and the content of the file is same as it should be
        if FileManager.is_file_existed(file_path) and FileManager.read_file(file_path) == self.__dummy_data:
            return True
        else: 
            return False
        
    # I am thinking about this function should return what user will see in the gui like "Acitaveted", "Reboot required", "Disabled". 
    # For now it returns the message string but ıdk maybe for later this will be return the status code like 0 = disabled, 1 = reboot required, 
    # 2 = activated etc.
    def check_status(self):
        result =  subprocess.run(['xrandr'], stdout=subprocess.PIPE, text=True)
        output = result.stdout

        is_port_shown_connected = False
        for line in output.splitlines():
            if " connected " in line and self.port_name in line: 
                is_port_shown_connected = True
        is_dummy_activated = self.check_dummy_activated()

        if is_dummy_activated and is_port_shown_connected:
            return "Activated"
        elif is_dummy_activated and not is_port_shown_connected:
            return "Reboot required"
        elif not is_dummy_activated and is_port_shown_connected:
            return "Reboot required"
        else:
            return "Disabled"
        
    def update_status(self):
        self.status = self.check_status()

    # These two functions return the status of the operation and error or succes message. 
    # index 0 is status 
    # index 1 is the message 

    def activate_dummy_config(self):
        config_file_name = "10-dummy.conf"

        # Dont do a thing if the dummy is already activated
        if self.check_dummy_activated():
            self.update_status()    # I know this is a stupid idea, but I can't come up with another one.
            return False, "Dummy is already activated"
        
        # Create, write the dummy-config and check its content
        if FileManager.write_file(self.file_path + config_file_name, self.__dummy_data) == True and self.check_dummy_activated() == True:
            self.update_status()
            return True, "Dummy config activated"
        else:
            self.update_status()
            return False, "Couldn't create a dummy config \n"
        

    # This function deletes the dummy config
    def deactivate_dummy_config(self):
        file_path =  self.file_path + "10-dummy.conf"

        # Check if the config is already deleted
        if not FileManager.is_file_existed(file_path):
            self.update_status()
            return False, "Dummy is already disabled"
        else:
            # Delete the file
            try: 
                os.remove(file_path)
                self.update_status()
                return True, "Dummy config deleted succesfully"
            except:
                self.update_status()
                return False, "Couldn't delete the dummy config"


    # FOR DEVELOPMENT
    def print_variables(self):
        print("Portname is " + self.port_name)
        print("Filepathh is " + self.file_path)
        print("The status is  " + self.check_status())