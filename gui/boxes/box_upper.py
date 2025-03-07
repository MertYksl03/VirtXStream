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

    # Shows the status of an operation by displaying an dialog
    def show_status_message(self, status):
        if status == None:
                self.app.show_error_message("Error: Operation Failed")
                return
            
        if status[0] == True:
            self.app.show_info_message(status[1])
        elif status[0] == False:
            self.app.show_error_message(status[1])


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
        self.button_toggle_dummy.connect("clicked", self.on_toggle_clicked)
        self.button_toggle_dummy.set_name("button-enable")
        box.pack_start(self.button_toggle_dummy, False, False, 10)

        self.update_config_box()
        return box

    def on_configure_clicked_dummy(self, button):
        # Open the configuration window
        config_window = ConfigWindow(self.app, self.parent_window, 0)
        config_window.show_all()
        self.update_config_box()

    def on_toggle_clicked(self, button):
        status = None

        if self.button_toggle_dummy.get_label() == "Enable":
            status = self.dummy_instance.activate_dummy_config() 

        else:

            status = self.dummy_instance.deactivate_dummy_config()
        
        # Show the status by displaying a message
        self.show_status_message(status)
        # Update the UI
        self.update_config_box()

    # This function updates the ui elements of config box 
    def update_config_box(self):
        new_status = f"{self.dummy_instance.status}"
        
        # Update status label
        GLib.idle_add(self.label_status_dmy.set_text, new_status)  

        # Enable/Disable the button based on status
        if new_status == "Activated":
            GLib.idle_add(self.button_toggle_dummy.set_label, "Disable")  # Change button text
            GLib.idle_add(self.button_toggle_dummy.set_name, "button-disable")  # Change button apperance
            
        else:
            GLib.idle_add(self.button_toggle_dummy.set_label, "Enable")  # Change button text
            GLib.idle_add(self.button_toggle_dummy.set_name, "button-enable")  # Change button apperance

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

        # update the box to get info
        self.update_display_box()
        return box

    def on_config_clicked_vd(self, button):
        # If the virtual display is enabled, dont let the user to configure it 
        if self.vd_instance.status == True:
            self.app.show_error_message("To configure the virtual display you have to disable it")
            return
        # Open the configuration window
        config_window = ConfigWindow(self.app, self.parent_window, 1)
        config_window.show_all()
        self.update_display_box()

    def on_toggle_clicked_vd(self, button):
        status = None

        # Check the virtual-display status
        if self.button_toggle_vd.get_label() == "Enable":
            # Plug the virtual display
            status = self.vd_instance.plug_virtual_display(self.app.main_port_name, self.app.port_name)
        else:
            # Unplug the virtual display 
            status = self.vd_instance.unplug_virtual_display()

        self.update_display_box()
        self.show_status_message(status)
    
    # This function updates the ui elements of vd-box
    def update_display_box(self):
        active_status = self.vd_instance.active_resolution

        if active_status == None:
            new_status = "Disabled"
        else:
            new_status = f"Resolution: {active_status}"
        
        # Update status label
        GLib.idle_add(self.label_status_vd.set_text, new_status)  

        # Enable/Disable the button based on status
        if new_status == "Disabled":
            GLib.idle_add(self.button_toggle_vd.set_label, "Enable")  # Change button text
            GLib.idle_add(self.button_toggle_vd.set_name, "button-enable")  # Change button apperance
            
        else:
            GLib.idle_add(self.button_toggle_vd.set_label, "Disable")  # Change button text
            GLib.idle_add(self.button_toggle_vd.set_name, "button-disable")  # Change button apperance


    def create_adb_settings_box(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_name("upper_box_boxes")

        # User should see and know what this part about
        label_title = Gtk.Label("ADB SERVER")
        box.pack_start(label_title, True, True, 10)

        # The label about the status. This label will be dynamicly changes and displays the status of dummy config
        label_status_dmy = Gtk.Label("Ready")
        box.pack_start(label_status_dmy, True, True, 10)
        
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
        label_status_dmy = Gtk.Label("Ready")
        box.pack_start(label_status_dmy, True, True, 10)
        
        button_configure = Gtk.Button(label="Configure")
        box.pack_start(button_configure, False, False, 10)
        
        button_activate = Gtk.Button(label="Save")
        box.pack_start(button_activate, False, False, 10)
        
        return box