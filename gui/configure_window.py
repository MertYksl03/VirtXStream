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

        # Store referance to app object
        self.app = app

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(False)  # Hide the close button
        self.set_titlebar(header_bar)  # Set the header bar as the window's title bar



        # Handle which configure window will be shown
        if which_config == "dummy":
            Gtk.Window.set_title(self, "Dummy Config Settings")
            self.add(self.create_window_dummy_config())

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
        self.port_name_entry.set_placeholder_text("Current port name: " + self.app.dummy_instance.port_name)
        grid.attach(self.port_name_entry, 1, 3, 1, 1)

        # Save button
        button_save = Gtk.Button(label="Save")
        button_save.connect("clicked", self.on_save_clicked) # Call the function on_config_saved from app object
        grid.attach(button_save, 1, 4, 1, 1)

        # Close button
        button_close = Gtk.Button(label="Close")
        button_close.connect("clicked", self.on_close_clicked)
        grid.attach(button_close, 0, 4, 1, 1)

        return grid
    
    def on_close_clicked(self, widget):
        self.destroy()

    def on_save_clicked(self, widget):

        file_path = self.file_path_entry.get_text().strip()
        port_name = self.port_name_entry.get_text().strip()

        # First check if the entries are not empty
        if not file_path or not port_name: 
            # show an error dialog to user
            self.show_error_dialog("Both fields are required\nYou need to fill the both fields")
            return 
        
        ports = self.app.dummy_instance.ports
        if ports:
            if not port_name in ports:
                self.show_error_dialog("Invalid port name \nAvaible ports: " + str(self.app.dummy_instance.ports))
                return
        
        # Add '/' to end of the filepath if the user didnt put it 
        if file_path[-1] != "/":
            file_path = file_path + "/"


        # Call the callback funtion with enterd values
        if self.app.on_config_saved:
            if self.app.on_config_saved(file_path, port_name) == True:
                # Close the configuration window
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