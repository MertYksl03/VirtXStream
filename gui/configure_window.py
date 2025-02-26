import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk #type: ignore

class ConfigWindow(Gtk.Window):
    def __init__(self, parent, on_save_callback, get_ports_callback):
        Gtk.Window.__init__(self, title="Configuration Window")
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.set_transient_for(parent)
        self.set_modal(True)

        # Store the callback function
        self.get_ports_callback = get_ports_callback
        self.on_save_callback = on_save_callback

        # Create a grid to arrange widgets
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        self.add(grid)

        # Info about file path
        info_file_path_string = """Enter the file path to your Xorg config files"""
        self.info_file_path_label = Gtk.Label()
        self.info_file_path_label.set_label(info_file_path_string)
        grid.attach(self.info_file_path_label, 0, 0, 2, 1)  # Span across 2 columns

        # File path entry
        grid.attach(Gtk.Label(label="File Path:"), 0, 1, 1, 1)
        self.file_path_entry = Gtk.Entry()
        self.file_path_entry.set_placeholder_text("Enter file path")
        grid.attach(self.file_path_entry, 1, 1, 1, 1)

        # Info about port name
        info_port_name_string = "Enter the port name that you want to connect your virtual display"
        self.info_port_name_label = Gtk.Label()
        self.info_port_name_label.set_label(info_port_name_string)
        grid.attach(self.info_port_name_label, 0, 2, 2, 1)  # Span across 2 columns

        # Port name entry
        grid.attach(Gtk.Label(label="Port Name:"), 0, 3, 1, 1)
        self.port_name_entry = Gtk.Entry()
        self.port_name_entry.set_placeholder_text("Enter port name")
        grid.attach(self.port_name_entry, 1, 3, 1, 1)

        # Save button
        save_button = Gtk.Button(label="Save")
        save_button.connect("clicked", self.on_save_clicked)
        grid.attach(save_button, 1, 4, 1, 1)

    def on_save_clicked(self, widget):
        file_path = self.file_path_entry.get_text().strip()
        port_name = self.port_name_entry.get_text().strip()

        # First check if the entries are not empty
        if not file_path or not port_name: 
            # show an error dialog to user
            self.show_error_dialog("Both fields are required\n" + "You need to fill the both fields")
            return 
        
        if self.get_ports_callback:
            ports = self.get_ports_callback()
            if not port_name in ports:
                self.show_error_dialog("Invalid port name \n" + "Avaible ports: " + str(ports))
                return
        
        # Add '/' to end of the filepath if the user didnt put it 
        if file_path[-1] != "/":
            file_path = file_path + "/"


        # call the callback funtion with enterd values
        if self.on_save_callback:
            self.on_save_callback(file_path, port_name)

        # Close the configuration window
        self.destroy()

    def show_error_dialog(self, message):
        # Create an error dialog
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=Gtk.DialogFlags.MODAL,
            type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            message_format=message
        )
        dialog.set_title("Error")
        dialog.run()  # Show the dialog and wait for user response
        dialog.destroy()  # Close the dialog