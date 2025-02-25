import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk #type: ignore

from src.dummy import Dummy

WIDTH = 1200
HEIGHT = 900

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, title = "X-vnc")
        self.set_default_size(WIDTH, HEIGHT)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Load external CSS
        provider = Gtk.CssProvider()
        provider.load_from_path("styles/style.css")  # Load the CSS file

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        box_outer = Gtk.Box()
        self.add(box_outer)

        button_activate = Gtk.Button(label="Dummy", halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER)
        button_activate.set_size_request(500, 150)
        button_activate.connect("clicked", self.on_click_activate)
        box_outer.add(button_activate) 


        button_deactivate = Gtk.Button(label="Dactivate", halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER)
        button_deactivate.set_size_request(500, 150)
        button_deactivate.connect("clicked", self.on_click_deactivate)
        box_outer.add(button_deactivate) 

    def on_click_activate(self, button):
        # status = Dummy.activate_dummy_config()
        self.show_error_dialog("asdsda")

    def on_click_deactivate(self, button):
        print()
      
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
    
        
