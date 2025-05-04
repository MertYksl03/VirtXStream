import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk #type: ignore

from gui.configure_windows import ConfigWindow
from gui.boxes.box_upper import BoxUpper
from gui.boxes.box_lower import BoxLower

import threading
import time

WIDTH = 1280
HEIGHT = 720

class MainWindow(Gtk.ApplicationWindow):
    # Global Variables
    # dummy_instance = None
    app = None

    def __init__(self, app):
        super().__init__(title = "X-vnc")
        self.set_default_size(WIDTH, HEIGHT)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.set_name("main-window") # name for css
        self.app = app

        # Load external CSS
        provider = Gtk.CssProvider()
        provider.load_from_path("styles/style.css")  # Load the CSS file

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Create a Header Bar 
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.set_title("X-Vnc")
        self.set_titlebar(header_bar)

        # A button to restrore the default settings 
        button_restore = Gtk.Button(label="Restore Defaults")
        button_restore.connect("clicked", self.on_restore_clicked)
        header_bar.pack_start(button_restore)

        # A help button with a link to this project's repo
        button_help = Gtk.LinkButton(uri="https://github.com/MertYksl03/X-Vnc-gui", label="Help")
        header_bar.pack_end(button_help)

        # A button with a link to my Github profile
        button_github = Gtk.LinkButton(uri="https://github.com/MertYksl03/", label="Github")
        header_bar.pack_end(button_github)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(box_outer)


        self.box_upper = BoxUpper(self.app, self)
        box_outer.pack_start(self.box_upper.get_box(), True, True, 0)


        self.box_lower = BoxLower().get_box()
        box_outer.pack_start(self.box_lower, True, True, 0)

        # Thread to monitor the UI
        self.monitor_thread = threading.Thread(target=self.monitor_ui_needed_update)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()


    def show_info_message(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self if self else None,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.run()
        dialog.destroy()
        
    def show_error_message(self, message):
        "Show a error message to the user"
        dialog = Gtk.MessageDialog(
            transient_for=self if self else None,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Error",
        )
        dialog.format_secondary_text(message)

        # Run the dialog and wait for user response
        response = dialog.run()

        # Destroy the dialog after the user responds
        dialog.destroy()

    def show_critical_error(self, message):
        """
        Show a critical error dialog and close the app when the user presses OK.
        """
        dialog = Gtk.MessageDialog(
            transient_for=self if self else None,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Critical Error",
        )
        dialog.format_secondary_text(message)  # Add detailed error message

        # Run the dialog and wait for user response
        response = dialog.run()

        # Destroy the dialog after the user responds
        dialog.destroy()

        # Close the application if the user presses OK
        if response == Gtk.ResponseType.OK:
            self.app.quit()  # Close the program

    def on_restore_clicked(self, button):
        if self.app.restore_defaults() == True:
            self.app.show_info_message("Restoring to default is succesful")


    # def show_error_dialog(self, message):
    #     dialog = Gtk.MessageDialog(
    #         transient_for=self,
    #         flags=0,
    #         message_type=Gtk.MessageType.ERROR,
    #         buttons=Gtk.ButtonsType.OK,
    #         text=message,
    #     )
    #     dialog.run()
    #     dialog.destroy()

    def monitor_ui_needed_update(self):
        # Checks every second if the ui needs an update
        # IDK if this is the best way to do this, but it works
        # If the ui needs an update, then update it
        while True:
            if self.app.ui_update_needed == True:
                # If the update is sucessful, then the app does not need an ui update
                if self.box_upper.update() == True: #and self.box_lower.update() == True:
                    self.app.ui_update_needed = False
                else:
                    self.app.show_error_message("Error: Could not update the UI")
            else:
                # If the update is not needed, then do nothing
                pass
            time.sleep(1)  # Sleep for a short time to avoid busy waiting

