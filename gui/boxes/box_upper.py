import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib  #type: ignore

from gui.configure_windows import ConfigWindow

# THE WIDGETS THAT UPDATES, THEIR REFERANCE MUST BE GLOBAL 

class BoxUpper:

    def __init__(self, app, parent_window):
        self.app = app
        self.dummy_instance = self.app.dummy_instance
        self.vd_instance = self.app.virtual_display_instance
        self.adb_instance = self.app.adb_instance
        self.vnc_instance = self.app.vnc_instance
        
        self.box_upper = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.parent_window = parent_window

        # The status that currently showen in the app(in the ui)
        self.status_dummy = self.dummy_instance.status
        self.status_vd = self.vd_instance.status
        self.status_adb = self.adb_instance.status
        self.status_vnc = self.vnc_instance.status
        
        # Create and add sub-boxes
        self.box_upper.pack_start(self.create_config_box(), True, True, 10)
        self.box_upper.pack_start(self.create_display_settings_box(), True, True, 10)
        self.box_upper.pack_start(self.create_adb_settings_box(), True, True, 10)
        self.box_upper.pack_start(self.create_vnc_box(), True, True, 10)


        # Update the boxes
        self.update_config_box(self.status_dummy)
        self.update_display_box(self.status_vd)
        self.update_adb_settings_box(self.status_adb)
        self.update_vnc_box(self.status_vnc)

    def get_box(self):
        return self.box_upper

    # Function to update the ui
    def update(self):
        # Get the new status of the instances
        new_status_dummy = self.dummy_instance.status
        new_status_vd = self.vd_instance.status
        new_status_adb = self.adb_instance.status
        new_status_vnc = self.vnc_instance.status

        # Check which box need an ui update
        if self.status_dummy != new_status_dummy:
            self.update_config_box(new_status_dummy)
            self.status_dummy = new_status_dummy
        
        if self.status_vd != new_status_vd:
            self.update_display_box(new_status_vd)
            self.status_vd = new_status_vd
        
        if  self.status_adb != new_status_adb:
            self.update_adb_settings_box(new_status_adb)
            self.status_adb = new_status_adb
        
        if self.status_vnc != new_status_vnc:
            self.update_vnc_box(new_status_vnc)
            self.status_vnc = new_status_vnc

        return True
    
    # FUNCTIONS THOSE ARE USED BY ALL BOXES SHOULD BE RIGHT BELOW THIS LINE

    # Shows the status of an operation by displaying an dialog
    def show_status_message(self, status):
        if status == None:
                self.parent_window.show_error_message("Error: Operation Failed")
                return
            
        if status[0] == True:
            self.parent_window.show_info_message(status[1])
        elif status[0] == False:
            self.parent_window.show_error_message(status[1])


    # This box holds the settings and status about dummy config
    def create_config_box(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_name("upper_box_boxes")

        # Title
        label_title = Gtk.Label(label="DUMMY CONFIG")
        box.pack_start(label_title, True, True, 10)

        # Status
        self.label_status_dmy = Gtk.Label()
        box.pack_start(self.label_status_dmy, True, True, 10)

        # Buttons
        button_configure = Gtk.Button(label="Configure")
        button_configure.connect("clicked", self.on_configure_clicked_dummy)
        box.pack_start(button_configure, False, False, 10)

        self.button_toggle_dummy = Gtk.Button(label="Enable")
        self.button_toggle_dummy.connect("clicked", self.on_toggle_clicked_dmy)
        self.button_toggle_dummy.set_name("button-enable")
        box.pack_start(self.button_toggle_dummy, False, False, 10)

        return box

    def on_configure_clicked_dummy(self, button):
        # Open the configuration window
        config_window = ConfigWindow(self.app, self.parent_window, 0)
        config_window.show_all()

    def on_toggle_clicked_dmy(self, button):
        status = None

        if self.status_dummy == 0 or self.status_dummy == -2:
            status = self.app.activate_dummy()

        else:
            status = self.app.deactivate_dummy()
        
        # Show the status by displaying a message
        self.show_status_message(status)

    # This function updates the ui elements of config box 
    def update_config_box(self, new_status):

        #TODO: Display the status message according to status from dummy instance

        if new_status == 1:
            status_message = "Activated"
        elif new_status == -1 or new_status == -2:
            status_message = "Reboot required"
        else:
            status_message = "Disabled"
        
        # Update status label
        GLib.idle_add(self.label_status_dmy.set_text, status_message)  

        # Enable/Disable the button based on status
        if new_status == 0 or new_status == -2:
            GLib.idle_add(self.button_toggle_dummy.set_label, "Enable")  # Change button text
            GLib.idle_add(self.button_toggle_dummy.set_name, "button-enable")  # Change button apperance
        else:
            GLib.idle_add(self.button_toggle_dummy.set_label, "Disable")  # Change button text
            GLib.idle_add(self.button_toggle_dummy.set_name, "button-disable")  # Change button apperance

    # This box shows the info about the virtual display and lets the user to configure it
    def create_display_settings_box(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_name("upper_box_boxes")

        label_title = Gtk.Label("VIRTUAL DISPLAY")
        box.pack_start(label_title, True, True, 10)

        # This label shows the status about the virtaul display(resolution etc.)
        self.label_status_vd = Gtk.Label()
        box.pack_start(self.label_status_vd, True, True, 10)

        button_configure = Gtk.Button(label="Configure")
        button_configure.connect("clicked", self.on_config_clicked_vd)
        box.pack_start(button_configure, False, False, 10)

        self.button_toggle_vd = Gtk.Button()
        self.button_toggle_vd.connect("clicked", self.on_toggle_clicked_vd)
        box.pack_start(self.button_toggle_vd, False, False, 10)

        return box

    def on_config_clicked_vd(self, button):
        # If the virtual display is enabled, dont let the user to configure it 
        if self.vd_instance.status == True:
            self.parent_window.show_error_message("To configure the virtual display you have to disable it")
            return
        # Open the configuration window
        config_window = ConfigWindow(self.app, self.parent_window, 1)
        config_window.show_all()

    def on_toggle_clicked_vd(self, button):
        status = None

        # Check the virtual-display status
        if self.status_vd == False:
            # Start the virtual display
            status = self.app.start_vd()
        else:
            # Stop the virtual display 
            status = self.app.stop_vd()

        self.show_status_message(status)
    
    # This function updates the ui elements of vd-box
    def update_display_box(self, new_status):
        active_resolution = self.vd_instance.active_resolution

        if new_status == False:
            status_message = "Disabled"
            GLib.idle_add(self.button_toggle_vd.set_label, "Enable")  # Change button text
            GLib.idle_add(self.button_toggle_vd.set_name, "button-enable")  # Change button apperance
            
        else:
            status_message = f"Resolution: {active_resolution}"
            GLib.idle_add(self.button_toggle_vd.set_label, "Disable")  # Change button text
            GLib.idle_add(self.button_toggle_vd.set_name, "button-disable")  # Change button apperance
        
        # Update status label
        GLib.idle_add(self.label_status_vd.set_text, status_message)  


    def create_adb_settings_box(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_name("upper_box_boxes")

        # User should see and know what this part about
        label_title = Gtk.Label("ADB SERVER")
        box.pack_start(label_title, True, True, 10)

        # The label about the status. This label will be dynamicly changes and displays the status of adb server
        self.label_status_adb = Gtk.Label()
        box.pack_start(self.label_status_adb, True, True, 10)
        
        # I think, i don't need configure button for adb
        # button_configure = Gtk.Button(label="Configure")
        # box.pack_start(button_configure, False, False, 10)
        
        self.button_toggle_adb = Gtk.Button()
        self.button_toggle_adb.connect("clicked", self.on_toggle_clicked_adb)
        box.pack_start(self.button_toggle_adb, False, False, 10)
        
        return box
    
    def on_toggle_clicked_adb(self, button):
        status = None

        if self.status_adb == False:
            # Start the adb server
            status = self.app.start_adb()
        else:
            # Kill the adb server
            status = self.app.stop_adb()

        self.show_status_message(status)
    
    def update_adb_settings_box(self, new_status):
        port = self.adb_instance.port

        if new_status == False:
            status_message = "Disabled"
            GLib.idle_add(self.button_toggle_adb.set_label, "Enable")  # Change button text
            GLib.idle_add(self.button_toggle_adb.set_name, "button-enable")  # Change button apperance
            
        else:
            status_message = f"Working at the port: {port}"
            GLib.idle_add(self.button_toggle_adb.set_label, "Disable")  # Change button text
            GLib.idle_add(self.button_toggle_adb.set_name, "button-disable")  # Change button apperance
        
        # Update status label
        GLib.idle_add(self.label_status_adb.set_text, status_message)  
    

    def create_vnc_box(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_name("upper_box_boxes")

        # User should see and know what this part about
        label_title = Gtk.Label("VNC SERVER")
        box.pack_start(label_title, True, True, 10)

        # The label about the status. This label will be dynamicly changes and displays the status
        self.label_status_vnc = Gtk.Label("Ready")
        box.pack_start(self.label_status_vnc, True, True, 10)
        
        self.button_configure_vnc = Gtk.Button(label="Configure")
        self.button_configure_vnc.connect("clicked", self.on_config_clicked_vnc)
        box.pack_start(self.button_configure_vnc, False, False, 10)

        self.button_toggle_vnc = Gtk.Button()
        self.button_toggle_vnc.connect("clicked", self.on_toggle_clicked_vnc)
        box.pack_start(self.button_toggle_vnc, False, False, 10)

        return box
    
    def update_vnc_box(self, new_status):

        if new_status == False:
            status_message = "Disabled"
            GLib.idle_add(self.button_toggle_vnc.set_label, "Enable")  # Change button text
            GLib.idle_add(self.button_toggle_vnc.set_name, "button-enable")  # Change button apperance
            
        else:
            status_message = "Working"
            GLib.idle_add(self.button_toggle_vnc.set_label, "Disable")  # Change button text
            GLib.idle_add(self.button_toggle_vnc.set_name, "button-disable")  # Change button apperance
        
        # Update status label
        GLib.idle_add(self.label_status_vnc.set_text, status_message)

    def on_toggle_clicked_vnc(self, button):
        status = None

        if self.status_vnc == False:
            # Start the vnc server
            status = self.app.start_vnc()
        else:
            # Kill the vnc server
            status = self.app.stop_vnc()

        self.show_status_message(status)

    def on_config_clicked_vnc(self, button):
        # If the vnc server is enabled, dont let the user to configure it 
        if self.vnc_instance.status == True:
            self.parent_window.show_error_message("To configure the VNC server you have to disable it")
            return
        # Open the configuration window
        config_window = ConfigWindow(self.app, self.parent_window, 3)
        config_window.show_all()