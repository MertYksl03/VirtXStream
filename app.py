import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib  # type: ignore

from gui.main_window import MainWindow

from src.dummy import Dummy

import threading
import json
import os
import subprocess

class MyApp(Gtk.Application):
    # Global variables
    dummy_instance = None

    def __init__(self):
        super().__init__(application_id="org.gnome.X-Vnc")  # Add an application ID
        # This varibales are private variables
        self.main_window = None
        self.data = None                                    # App's config data stored in config.json             
        

    def do_activate(self):
        self.initialize_app()
        
        self.main_window = MainWindow(self)
        self.add_window(self.main_window)
        self.main_window.show_all()


    def initialize_app(self):
        # Read the configuration from config.json
        self.load_data()

        # These variables will be loaded from config.json
        try :
            self.file_path = self.data["default"]["x"]["file_path"]
        except Exception as e:
            self.show_critical_error(str(e))
            return

        try :
            self.port_name = self.data["default"]["x"]["default_port"]
        except Exception as e:
            self.show_critical_error(str(e))
            return

        # Initialize Dummy class
        self.dummy_instance = Dummy()
        status = self.dummy_instance.initialize(self.file_path, self.port_name)
        if status[0] == False:
            # Display error message and close the app
            # error_message = "Failed to initialize Dummy class. The application will now close."
            error_message = status[1]
            GLib.idle_add(self.show_critical_error, error_message)
            return  # Stop further execution
        
        # self.print_dummy_variables()
        


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


    def on_config_saved(self, file_path, port_name):
        return self.dummy_instance.initialize(file_path, port_name)
    
    # FOR DEVELOPMENT 
    def print_dummy_variables(self):
        print("Portname is " + self.dummy_instance.port_name)
        print("Filepathh is " + self.dummy_instance.file_path)
        print("The status is  " + self.dummy_instance.check_status())


