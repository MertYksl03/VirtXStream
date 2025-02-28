import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk #type: ignore

from gui.configure_window import ConfigWindow


class BoxUpper:

    def __init__(self, ports, on_config_saved_callback, parent_window):
        
        self.ports = ports
        self.on_config_saved_callback = on_config_saved_callback
        self.box_upper = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.parent_window = parent_window
        # Create and add sub-boxes
        self.box_upper.pack_start(self.create_config_box(), True, True, 10)
        self.box_upper.pack_start(self.create_display_settings_box(), True, True, 10)
        self.box_upper.pack_start(self.create_adb_settings_box(), True, True, 10)
        self.box_upper.pack_start(self.create_vnc_settings_box(), True, True, 10)

    def get_box(self):
        return self.box_upper

    # This box holds the settings and status about dummy config
    def create_config_box(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_name("upper_box_boxes")

        # Title
        label_title = Gtk.Label(label="DUMMY CONFIG")
        box.pack_start(label_title, True, True, 10)

        # Status
        label_status = Gtk.Label(label="Ready")
        box.pack_start(label_status, True, True, 10)

        # Buttons
        button_configure = Gtk.Button(label="Configure")
        button_configure.connect("clicked", self.on_configure_clicked)
        box.pack_start(button_configure, False, False, 10)

        button_save = Gtk.Button(label="Save")
        button_save.connect("clicked", self.on_save_clicked)
        box.pack_start(button_save, False, False, 10)

        return box

    def on_configure_clicked(self, button):
        # Open the configuration window
        config_window = ConfigWindow(self.on_config_saved_callback, self.ports, self.parent_window)
        config_window.show_all()

    def on_save_clicked(self, button):
        # Handle save logic
        print("Save button clicked")


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