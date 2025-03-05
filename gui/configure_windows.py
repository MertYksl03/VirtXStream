import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk #type: ignore

class ConfigWindow(Gtk.Window):
    def __init__(self, app, parent, which_config):
        Gtk.Window.__init__(self, title="Configuration Window")
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.set_transient_for(parent)
        self.set_modal(True)

        # Store the referance of app object
        self.app = app

        # Initialize vd_resolution and vd_position
        self.vd_resolution = None
        self.vd_position = None
        # Get the resolutions from app object
        self.vd_resolutions = self.app.resolutions

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(False)  # Hide the close button
        self.set_titlebar(header_bar)  # Set the header bar as the window's title bar



        # Handle which configure window will be shown
        # 0 = dummy, 1 = virtual-display, 2 = adb-server, 3 = Vnc-server
        if which_config == 0:
            Gtk.Window.set_title(self, "Dummy Config Settings")
            self.add(self.create_window_dummy_config())
        elif which_config == 1:
            Gtk.Window.set_title(self, "Virtual Display Settings")
            self.add(self.create_window_vd_config(resolutions=self.vd_resolutions))
        elif which_config == 2:
            Gtk.Window.set_title(self, "ADB Server Settings")
            # Add stuff here
        elif which_config == 3:
            Gtk.Window.set_title(self, "VNC Server Settings")
            # Add stuff here

    def create_window_dummy_config(self):
        # Create a grid to arrange widgets
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)

        # Info about file path
        info_file_path_string = """Enter the file path to your Xorg config files"""
        info_file_path_label = Gtk.Label()
        info_file_path_label.set_label(info_file_path_string)
        grid.attach(info_file_path_label, 0, 0, 2, 1)  # Span across 2 columns

        # File path entry
        grid.attach(Gtk.Label(label="File Path:"), 0, 1, 1, 1)
        self.file_path_entry = Gtk.Entry()
        self.file_path_entry.set_placeholder_text("Current file path: " + self.app.dummy_instance.file_path)
        grid.attach(self.file_path_entry, 1, 1, 1, 1)

        # Info about port name
        info_port_name_string = "Enter the port name that you want to connect your virtual display"
        info_port_name_label = Gtk.Label()
        info_port_name_label.set_label(info_port_name_string)
        grid.attach(info_port_name_label, 0, 2, 2, 1)  # Span across 2 columns

        # Port name entry
        grid.attach(Gtk.Label(label="Port Name:"), 0, 3, 1, 1)
        self.port_name_entry = Gtk.Entry()
        self.port_name_entry.set_placeholder_text("Current port name: " + self.app.port_name)
        grid.attach(self.port_name_entry, 1, 3, 1, 1)

        # Save button
        button_save = Gtk.Button(label="Save")
        button_save.connect("clicked", self.on_save_clicked_dmy) # Call the function on_config_saved from app object
        grid.attach(button_save, 1, 4, 1, 1)

        # Close button
        button_close = Gtk.Button(label="Close")
        button_close.connect("clicked", self.on_close_clicked)
        grid.attach(button_close, 0, 4, 1, 1)

        return grid
    
    def on_close_clicked(self, widget):
        self.destroy()

    def on_save_clicked_dmy(self, widget):

        file_path = self.file_path_entry.get_text().strip()
        port_name = self.port_name_entry.get_text().strip()

        # First check if the entries are not empty
        if not file_path or not port_name: 
            # show an error dialog to user
            self.show_error_dialog("Both fields are required\nYou need to fill the both fields")
            return 
        
        ports = self.app.ports
        if ports:
            if not port_name in ports:
                self.show_error_dialog("Invalid port name \nAvaible ports: " + str(ports))
                return
        
        # Add '/' to end of the filepath if the user didnt put it 
        if file_path[-1] != "/":
            file_path = file_path + "/"


        # Call the callback funtion with enterd values
        if self.app.on_config_saved_dmy:
            if self.app.on_config_saved_dmy(file_path, port_name) == True:
                # Close the configuration window
                self.destroy()
    

    def create_window_vd_config(self, resolutions):
       # Create a grid to arrange widgets
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)

        # Can add a info: all the widget's relative height attributes are aligned 

        # Info about the resolution
        info_resolution_string = "Select resolution for virtual display"
        info_resolution = Gtk.Label()
        info_resolution.set_label(info_resolution_string)
        grid.attach(info_resolution, 0, 0, 4, 1)  # Span across 4 columns

        # Info about current resolution
        info_current_res_string = f"Current Resolution: {self.app.virtual_display_instance.resolution}"
        info_current_res = Gtk.Label()
        info_current_res.set_label(info_current_res_string)
        grid.attach(info_current_res, 0, 1, 4, 1)  # Span across 4 columns

        # Resolution buttons
        vbox_resolutions = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        swin = Gtk.ScrolledWindow()
        swin.add_with_viewport(vbox_resolutions)
        swin.set_min_content_height(300)
        grid.attach(swin, 0, 2, 4, 1)

        # Variable to store the first radio button (used for grouping)
        first_radio = None

        # Dynamically create radio buttons based on the resolutions array
        for resolution in resolutions:
            radio = Gtk.RadioButton.new_with_label_from_widget(first_radio, resolution)
            if first_radio is None:
                first_radio = radio  # Set the first radio button for grouping
            vbox_resolutions.pack_start(radio, False, False, 0)
            radio.connect("toggled", self.on_resolution_buttons_toggle_vd, resolution)

        info_position_string = "Select the position for virtual display"
        info_position = Gtk.Label()
        info_position.set_label(info_position_string)
        grid.attach(info_position, 0, 3, 4, 1)  # Span across 4 columns


        # Buttons for position
        # Create a radio button group
        button_left = Gtk.RadioButton.new_with_label(None, "Left")
        button_left.connect("toggled", self.on_position_buttons_toggled_vd, "left-of")
        grid.attach(button_left, 0, 4, 1, 1)  # Column 0, Row 3

        button_below = Gtk.RadioButton.new_with_label_from_widget(button_left, "Below")
        button_below.connect("toggled", self.on_position_buttons_toggled_vd, "below")
        grid.attach(button_below, 1, 4, 1, 1)  # Column 1, Row 3

        button_above = Gtk.RadioButton.new_with_label_from_widget(button_left, "Above")
        button_above.connect("toggled", self.on_position_buttons_toggled_vd, "above")
        grid.attach(button_above, 2, 4, 1, 1)  # Column 2, Row 3

        button_right = Gtk.RadioButton.new_with_label_from_widget(button_left, "Right")
        button_right.connect("toggled", self.on_position_buttons_toggled_vd, "right-of")
        grid.attach(button_right, 3, 4, 1, 1)  # Column 3, Row 3

        # Save button
        button_save = Gtk.Button(label="Save")
        button_save.connect("clicked", self.on_save_clicked_vd)
        grid.attach(button_save, 2, 5, 2, 2)  # Span across 2 columns, Row 4

        # Close button
        button_close = Gtk.Button(label="Close")
        button_close.connect("clicked", self.on_close_clicked)
        grid.attach(button_close, 0, 5, 2, 2)  # Span across 2 columns, Row 4

        return grid
    
    def on_resolution_buttons_toggle_vd(self, button, resolution):
        if button.get_active():
            self.vd_resolution = resolution

    def on_position_buttons_toggled_vd(self, button, name):
        if button.get_active():
            self.vd_position = name

    def on_save_clicked_vd(self, button):
        resolution = self.vd_resolution
        position = self.vd_position

        # Check did user select a resolution
        if not resolution: 
            # show an error dialog to user
            self.show_error_dialog("Please select a resolution")
            return 
        
        if not position:
            # show an error dialog to user
            self.show_error_dialog("Please select a position")
            return     
        
        self.app.on_config_save_vd(resolution, position)
        self.destroy()
        
    def show_error_dialog(self, message):
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=Gtk.DialogFlags.MODAL,
            type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            message_format=message
        )
        dialog.set_title("Error")
        dialog.run()
        dialog.destroy()