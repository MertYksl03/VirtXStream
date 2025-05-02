import subprocess
import os
import time

class ADBServer:
    status = None          # Status of the adb server
    port = None            # Port that vnc server will running on. 

    def __init__(self):
        self.status = self.check_status()
        self.port = 5900 # For now it's hardcoded

    def start_server(self):
        try:
            start_command = "adb start-server"
            subprocess.run(start_command.split(), check=True)
            forward_command = f"adb reverse tcp:{self.port} tcp:{self.port}"
            subprocess.run(forward_command.split(), check=True)
        except subprocess.CalledProcessError as e:
            return False, f"Failed to start ADB server: \n{e}"

        self.status = True
        return True, f"ADB server is enabled at port: {self.port}"


    def kill_server(self):
        try:
            kill_command = "adb kill-server"
            subprocess.run(kill_command.split(), check=True)
        except subprocess.CalledProcessError:
            return False, "Failed to kill the ADB server\nTo manually kill it try command: adb kill-server"
    
        self.status = False
        return True, "ADB server is killed successfully"
    
    
    def check_status(self):
        try:
            check_command = "adb reverse --list"
            result = subprocess.run(check_command.split(), check=True, capture_output=True, text=True)

            if str(self.port) in result.stdout:
                return True
            else:
                return False
        except subprocess.CalledProcessError:
                return False
