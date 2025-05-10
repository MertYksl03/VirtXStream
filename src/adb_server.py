import subprocess


class ADBServer:
    status = None          # Status of the adb server
    port = None            # Port that vnc server will running on. 

    def __init__(self):
        self.status = self.check_status()
        self.port = 5900 # For now it's hardcoded

    def start_server(self):
        stderr = None
        try:
            # Check if adb is installed
            check_command = "adb version"
            result = subprocess.run(check_command.split(), check=True, capture_output=True, text=True)
            stderr = result.stderr
        except subprocess.CalledProcessError:
            return False, "ADB not found. Please install ADB and add it to your PATH."
        
        try:
            start_command = "adb start-server"
            subprocess.run(start_command.split(), check=True)
            forward_command = f"adb reverse tcp:{self.port} tcp:{self.port}"
            subprocess.Popen(
                forward_command.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
        except Exception as e:
            return False, f"An error occurred: {e}"

        # Check if the ADB server started successfully    
        if stderr:
            return False, f"Failed to start ADB server: \n{stderr}" 
    
        self.status = True
        return True, f"ADB server is enabled at port: {self.port}"


    def stop_server(self):
        try:
            kill_command = "adb kill-server"
            subprocess.run(kill_command.split(), check=True)
        except subprocess.CalledProcessError:
            return False, "Failed to kill the ADB server\nTo manually kill it try the command: adb kill-server"
    
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
