import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib  # type: ignore

from gui.main_window import MainWindow

from src.dummy import Dummy

import threading
import json
import os

class MyApp(Gtk.Application):

    def __init__(self):
        super().__init__(application_id="org.gnome.X-Vnc")  # Add an application ID
        self.main_window = None
        self.data = None

    def do_activate(self):
        self.main_window = MainWindow(application=self)
        self.add_window(self.main_window)
        self.main_window.show_all()

        # Initialization in a separate thread
        threading.Thread(target=self.initialize_app, daemon=True).start()

    def initialize_app(self):
        # Read the configuration from config.json
        # GLib.idle_add(self.load_data)
        self.load_data()

        # These variables will be loaded from config.json
        file_path = self.data["x"]["file_path"]
        port_name = self.data["x"]["default_port"]

        # Initialize Dummy class
        dummy_instance = Dummy()
        if not dummy_instance.initialize(file_path, port_name):
            # Display error message and close the app
            error_message = "Failed to initialize Dummy class. The application will now close."
            GLib.idle_add(self.show_critical_error, error_message)
            return  # Stop further execution

        # Load additional data
        # self.load_data()
        
    def show_critical_error(self, message):
        """
        Show a critical error dialog and close the app when the user presses OK.
        """
        dialog = Gtk.MessageDialog(
            transient_for=self.main_window if self.main_window else None,
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
            self.quit()  # Close the program

    # NON-UI FUNCTIONS
    def load_data(self):
        try:
            # Path to the JSON file
            json_path = os.path.join(os.path.dirname(__file__), "src/config.json")

            # Load the JSON file
            with open(json_path, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.show_critical_error("Error: JSON file not found.")
            self.data = {}  # Fallback to an empty dictionary
        except json.JSONDecodeError:
            self.show_critical_error("Error: Invalid JSON format.")
            self.data = {}  # Fallback to an empty dictionary