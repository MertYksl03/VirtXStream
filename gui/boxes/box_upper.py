import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib  #type: ignore

from gui.configure_window import ConfigWindow

# THE WIDGETS THAT UPDATES, THEIR REFERANCE MUST BE GLOBAL 

class BoxUpper:

    def __init__(self, app, parent_window):
        self.app = app
        self.box_upper = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.parent_window = parent_window
        # Create and add sub-boxes
        self.box_upper.pack_start(self.create_config_box(), True, True, 10)
        self.box_upper.pack_start(self.create_display_settings_box(), True, True, 10)
        self.box_upper.pack_start(self.create_adb_settings_box(), True, True, 10)
        self.box_upper.pack_start(self.create_vnc_settings_box(), True, True, 10)

    def get_box(self):
        return self.box_upper
    
    # FUNCTIONS THOSE ARE USED BY ALL BOXES SHOULD BE RIGHT BELOW THIS LINE

    # This box holds the settings and status about dummy config
    def create_config_box(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_name("upper_box_boxes")

        # Title
        label_title = Gtk.Label(label="DUMMY CONFIG")
        box.pack_start(label_title, True, True, 10)

        # Status
        self.label_status = Gtk.Label(label=self.app.dummy_instance.status)  # Store reference
        box.pack_start(self.label_status, True, True, 10)

        # Buttons
        button_configure = Gtk.Button(label="Configure")
        button_configure.connect("clicked", self.on_configure_clicked)
        box.pack_start(button_configure, False, False, 10)

        self.button_toggle_dummy = Gtk.Button(label="Enable")
        self.button_toggle_dummy.connect("clicked", self.on_toggle_clicked)
        self.button_toggle_dummy.set_name("button-enable")
        box.pack_start(self.button_toggle_dummy, False, False, 10)

        self.update_config_box()
        return box

    def on_configure_clicked(self, button):
        # Open the configuration window
        config_window = ConfigWindow(self.app, self.parent_window, "dummy")
        config_window.show_all()
        self.update_config_box()

    def on_toggle_clicked(self, button):
        if self.button_toggle_dummy.get_label() == "Enable":
            status = self.app.dummy_instance.activate_dummy_config() 

            if status == None:
                self.app.show_error_message("Failed to enable dummy config \nRun the program with sudo")
                return
            
            if status[0] == True:
                self.app.show_info_message(status[1])
            elif status[0] == False:
                self.app.show_error_message(status[1])
        else:

            status = self.app.dummy_instance.deactivate_dummy_config()

            if status == None:
                self.app.show_error_message("Failed to disable dummy config \nRun the program with sudo")
                return

            if status[0] == True:
                self.app.show_info_message(status[1])
            elif status[0] == False:
                self.app.show_error_message(status[1])

        self.update_config_box()

    # This function updates the ui elements
    def update_config_box(self):
        new_status = self.app.dummy_instance.status
        
        # Update status label
        GLib.idle_add(self.label_status.set_text, new_status)  

        # Enable/Disable the button based on status
        if new_status == "Activated":
            GLib.idle_add(self.button_toggle_dummy.set_label, "Disable")  # Change button text
            GLib.idle_add(self.button_toggle_dummy.set_name, "button-disable")  # Change button apperance
            
        else:
            GLib.idle_add(self.button_toggle_dummy.set_label, "Enable")  # Change button text
            GLib.idle_add(self.button_toggle_dummy.set_name, "button-enable")  # Change button apperance

    def create_display_settings_box(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_name("upper_box_boxes")

        label_title = Gtk.Label("VIRTUAL DISPLAY")
        box.pack_start(label_title, True, True, 10)

        # This label shows the status about the virtaul display(resolution etc.)
        label_status = Gtk.Label("Resolution : 1920x1080") # For now
        box.pack_start(label_status, True, True, 10)

        button_configure = Gtk.Button(label="Configure")
        box.pack_start(button_configure, False, False, 10)

        button_apply = Gtk.Button(label="Apply")
        box.pack_start(button_apply, False, False, 10)
        return box


    def create_adb_settings_box(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_name("upper_box_boxes")

        # User should see and know what this part about
        label_title = Gtk.Label("ADB SERVER")
        box.pack_start(label_title, True, True, 10)

        # The label about the status. This label will be dynamicly changes and displays the status of dummy config
        label_status = Gtk.Label("Ready")
        box.pack_start(label_status, True, True, 10)
        
        button_configure = Gtk.Button(label="Configure")
        box.pack_start(button_configure, False, False, 10)
        
        button_activate = Gtk.Button(label="Save")
        box.pack_start(button_activate, False, False, 10)
        return box


    def create_vnc_settings_box(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_name("upper_box_boxes")

        # User should see and know what this part about
        label_title = Gtk.Label("VNC SERVER")
        box.pack_start(label_title, True, True, 10)

        # The label about the status. This label will be dynamicly changes and displays the status of dummy config
        label_status = Gtk.Label("Ready")
        box.pack_start(label_status, True, True, 10)
        
        button_configure = Gtk.Button(label="Configure")
        box.pack_start(button_configure, False, False, 10)
        
        button_activate = Gtk.Button(label="Save")
        box.pack_start(button_activate, False, False, 10)
        
        return box