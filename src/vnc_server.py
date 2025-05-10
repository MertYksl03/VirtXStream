import subprocess
import psutil
import socket
import threading

class VNCServer:
    resolution = None
    is_just_allow_usb = None
    port = None
    process = None
    local_ip = None
    status = None           # Holds the status of the vnc server
    is_connected = None     # Holds if a viewer is connected or not

    def __init__(self, resolution, just_usb, port):
        self.resolution = resolution
        self.is_just_allow_usb = just_usb
        self.port = port
        
        self.process = self.find_x11vnc_process()
        self.local_ip = self.get_local_ip()

        if self.process != None:
            self.status = True

        self.status = False
        self.is_connected = False

    def start_x11vnc(self):
        if self.process is None:
            # vnc_command = f"x11vnc --clip {self.resolution} -viewonly -repeat -rfbwait 3000 -once -rfbport {self.port}"
            vnc_command = f"x11vnc --clip {self.resolution} -viewonly -repeat -once -rfbport {self.port}" 
            if self.is_just_allow_usb == True:
                vnc_command += " -allow 127.0.0.1" # This may change
                
            try:
                self.process = subprocess.Popen(
                    vnc_command.split(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                )
            except FileNotFoundError:
                self.status = False
                return False, "Error: x11vnc not found"
            except Exception as e:
                self.status = False
                return False, f"Error: {e}"
            
        self.status = True
        return True, "VNC server is running"
    

    def stop_x11vnc(self):
        if self.process is not None:
            self.process.terminate()
            self.process.wait()
            self.process = None

            self.status = False
            return True, "VNC server killed successfully"
        
        return False, "VNC server is running"
    
    def find_x11vnc_process(self):
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'x11vnc' in proc.info['name'] or (
                    proc.info['cmdline'] and 'x11vnc' in proc.info['cmdline'][0]
                ):
                    return proc  # Return the process object
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    def get_local_ip(self):
        try:
            # Connect to a non-routable address; no data is actually sent
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Google's DNS server
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            return f"Error: {e}"
