import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk #type: ignore 

class BoxLower:
        def __init__(self, app, parent_window):
            self.app = app
            self.parent_window = parent_window

            self.vnc_instance = self.app.vnc_instance
            self.adb_instance = self.app.adb_instance

            self.status_vnc = self.vnc_instance.status
            self.is_connected = self.vnc_instance.is_connected
            self.port = self.vnc_instance.port
            self.local_ip = self.vnc_instance.local_ip
            self.just_usb = self.vnc_instance.is_just_allow_usb

            self.local_host = "127.0.0.1"
            
            self.status_adb = self.adb_instance.status

            self.box_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

            # Using these empty labels as spacers
            spacer_left = Gtk.Label(" ")
            spacer_right = Gtk.Label(" ")

            
            
            # Create the main box
            self.box_ip = self.create_box_ip()
            box_main = self.create_main_box()


            self.box_outer.pack_start(spacer_left, True, True, 0)
            self.box_outer.pack_start(box_main, True, True, 0)
            self.box_outer.pack_start(spacer_right, True, True, 0)

            # Update the main box
            self.update_main_box()

        def get_box(self):
            return self.box_outer
        
        def update(self):
            self.status_vnc = self.vnc_instance.status
            self.is_connected = self.vnc_instance.is_connected
            self.port = self.vnc_instance.port
            self.local_ip = self.vnc_instance.local_ip
            self.just_usb = self.vnc_instance.is_just_allow_usb
            self.status_adb = self.adb_instance.status

            # Update the main box
            self.update_main_box()
            return True

        def create_main_box(self):
            # Function to create the main box

            box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

            
            self.label_status = Gtk.Label()
            self.label_status.set_name("label-status") # name for css

            box_main.pack_start(self.label_status, True, True, 0)

            
            box_main.pack_start(self.box_ip, True, True, 0)

            
            return box_main
        
        def update_main_box(self):
            
            if self.status_vnc == False:
                self.label_status.set_label("VNC server is not running")
                self.label_status.set_name("label-status-error")
                self.box_ip.hide()
            else:
                if self.is_connected == False:
                    self.label_status.set_label("DISCONNECTED")
                    self.label_status.set_name("label-status-disconnected")
                    self.box_ip.show_all()
                else:
                    self.label_status.set_label("CONNECTED")
                    self.label_status.set_name("label-status-connected")
                    self.box_ip.hide()

            # Update the box with the IP address and port
            self.update_box_ip()


        def create_box_ip(self):
            # Function to create the box with the IP address and port
            box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            box_outer.set_margin_top(5)
            box_outer.set_margin_bottom(5)

            label_info = Gtk.Label("You can connect to the VNC server using a VNC viewer.\n The IP address and port are shown below.")


            box_ip = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

            label_ip = Gtk.Label("IP: ")

            self.label_ip = Gtk.Label()
            self.label_ip.set_selectable(True)

            box_ip.pack_start(label_ip, True, True, 0)
            box_ip.pack_start(self.label_ip, True, True, 0)

            box_outer.pack_start(label_info, True, True, 0)
            box_outer.pack_start(box_ip, True, True, 0)

            return box_outer
        
        def update_box_ip(self):
            # Function to update the box with the IP address and port
            if self.status_adb == True:
                if self.just_usb == True:
                    string_ip = f"{self.local_host}:{self.port} (USB)"
                    self.label_ip.set_label(string_ip)
                else:
                    string_ip = f"{self.local_ip}:{self.port} (WiFi) or {self.local_host}:{self.port} (USB)"
                    self.label_ip.set_label(string_ip)
            else:
                string_ip = f"{self.local_ip}:{self.port} (WiFi)"
                self.label_ip.set_label(string_ip)
            


