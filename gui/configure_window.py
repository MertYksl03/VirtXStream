import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk #type: ignore

class ConfigWindow(Gtk.Window):
    def __init__(self, parent):
        Gtk.Window.__init__(self, title="Configuration Window")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.set_transient_for(parent)
        self.set_modal(True)

        # Create a grid to arrange widgets
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        self.add(grid)

        # File path entry
        self.file_path_entry = Gtk.Entry()
        self.file_path_entry.set_placeholder_text("Enter file path")
        grid.attach(Gtk.Label(label="File Path:"), 0, 0, 1, 1)
        grid.attach(self.file_path_entry, 1, 0, 1, 1)

        # Port name entry
        self.port_name_entry = Gtk.Entry()
        self.port_name_entry.set_placeholder_text("Enter port name")
        grid.attach(Gtk.Label(label="Port Name:"), 0, 1, 1, 1)
        grid.attach(self.port_name_entry, 1, 1, 1, 1)

        # Save button
        save_button = Gtk.Button(label="Save")
        save_button.connect("clicked", self.on_save_clicked)
        grid.attach(save_button, 1, 2, 1, 1)

    def on_save_clicked(self, widget):
        file_path = self.file_path_entry.get_text()
        port_name = self.port_name_entry.get_text()

        # Here you can save the configuration or do something with the values
        print(f"File Path: {file_path}")
        print(f"Port Name: {port_name}")

        # Close the configuration window
        self.destroy()