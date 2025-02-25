import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk #type: ignore

from gui.configure_window import ConfigWindow
# from src.dummy import Dummy

WIDTH = 1280
HEIGHT = 720

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, title = "X-vnc")
        self.set_default_size(WIDTH, HEIGHT)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)

        # Load external CSS
        provider = Gtk.CssProvider()
        provider.load_from_path("styles/style.css")  # Load the CSS file

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # The two main boxes
        box_upper = Gtk.Box()
        self.add(box_upper)

        # box_lower = Gtk.Box()
        # self.attach(box_lower)

        # message = "Hello this is a message"
        # label = Gtk.Label(label=message)
        # box_upper.add(label)

        button = Gtk.Button(label="Configure")
        button.connect("clicked", self.on_button_clicked)
        box_upper.add(button)

    def on_button_clicked(self, button):
        # Open the configuration window
        config_window = ConfigWindow(self)
        config_window.show_all()

    def show_error_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.run()
        dialog.destroy()
     
    
        
