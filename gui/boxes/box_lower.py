import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk #type: ignore 

class BoxLower:
        def __init__(self):

            self.box_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

            # Using these empty labels as spacers
            spacer_left = Gtk.Label(" ")
            spacer_right = Gtk.Label(" ")

            box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            box_main.set_name("lower_box")
            
            status = Gtk.Label("DISCONNECTED")
            status.set_name("lower_box_status")
            box_main.pack_start(status, True, False, 0)


            # Grid for IP and other details
            grid = Gtk.Grid()
            grid.set_column_spacing(20)
            grid.set_row_spacing(20)
            box_main.pack_end(grid, True, True, 0)

            # Center the grid horizontally
            grid.set_halign(Gtk.Align.CENTER)

            # Add informational label at the top (row 0)
            info = """You can connect the VNC server with this ip """
            info = Gtk.Label(label=info)
            grid.attach(info, 0, 0, 2, 1)  # Span across 2 columns

            # Add IP label and value (row 1)
            label1 = Gtk.Label(label="Ip: ")
            label2 = Gtk.Label(label="127.0.0.1:5900")
            label2.set_selectable(True)  # Allow text selection
            grid.attach(label1, 0, 1, 1, 1)  # Attach label1 at (0, 1)
            grid.attach(label2, 1, 1, 1, 1)  # Attach label2 at (1, 1)


            self.box_outer.pack_start(spacer_left, True, True, 0)
            self.box_outer.pack_start(box_main, True, True, 0)
            self.box_outer.pack_start(spacer_right, True, True, 0)

        def get_box(self):
            return self.box_outer