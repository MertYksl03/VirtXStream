import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib  # type: ignore

from gui.main_window import MainWindow
from gui.loading_window import LoadingWindow

from src.dummy import Dummy

import threading
import time
import os
import json

class MyApp(Gtk.Application):

    def __init__(self):
        super().__init__(application_id="org.gnome.X-Vnc")  # Add an application ID
        self.loading_window = None
        self.main_window = None

    def do_activate(self):
        # Show the loading screen
        self.loading_window = LoadingWindow()
        self.add_window(self.loading_window)
        self.loading_window.show_all()

        # Initialization in a separate thread
        threading.Thread(target=self.initialize_app, daemon=True).start()

    def initialize_app(self):
        # Read the configuration from config.json
        # These variables will be loaded from config.json
        file_path = "testfiles/"
        port_name = "HDMI-1-0"

        # Initialize Dummy class
        dummy_instance = Dummy()
        if not dummy_instance.initialize(file_path, port_name):
            # Display error message and close the app
            error_message = "Failed to initialize Dummy class. The application will now close."
            GLib.idle_add(self.show_critical_error, error_message)
            return  # Stop further execution

        # Load additional data
        # self.load_data()
    

        # Show the main window after initialization
        GLib.idle_add(self.show_main_window)

    def show_main_window(self):
        # Close the loading screen
        if self.loading_window:
            self.loading_window.destroy()
            self.loading_window = None  # Remove reference

        # Now show the main window
        self.main_window = MainWindow(application=self)
        self.add_window(self.main_window)
        self.main_window.show_all()


    def load_data(self):
        # TODO: Load data from json file
        print()

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