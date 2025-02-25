import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk #type: ignore

class LoadingWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Loading...")
        self.set_default_size(300, 100)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        # Add a spinner (spinner does not show up on my computer but can be shown in other's)
        self.spinner = Gtk.Spinner()
        self.spinner.start()

        # Add a label
        label = Gtk.Label(label="Initializing, please wait...")

        # Arrange widgets in a box
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)
        box.pack_start(self.spinner, True, True, 0)
        box.pack_start(label, True, True, 0)
        self.spinner.start()

        self.add(box)
    