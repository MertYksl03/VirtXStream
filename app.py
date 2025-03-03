import gi
import atexit
import signal
import sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib  # type: ignore

from gui.main_window import MainWindow

from src.dummy import Dummy
from src.virtual_display import VirtualDisplay

import threading
import json
import os
import subprocess

class MyApp(Gtk.Application):
    # Global variables
    dummy_instance = None
    port_name = None
    main_port_name = None

    def __init__(self):
        super().__init__(application_id="org.gnome.X-Vnc")  # Add an application ID
        # This varibales are private variables
        self.main_window = None
        self.data = None                                    # App's config data stored in config.json             
        

    def do_activate(self):
        if self.initialize_app() == False:
            return
        
            # Register cleanup function for normal exit
        atexit.register(self.clean_up)

        # Register signal handlers for crashes or termination
        # signal.signal(signal.SIGTERM, self.handle_signal)
        # signal.signal(signal.SIGINT, self.handle_signal)

        self.main_window = MainWindow(self)
        self.add_window(self.main_window)
        self.main_window.show_all()

    # LOGIC FUNCTIONS

    def initialize_app(self):
        
        # First check the session type 
        session = self.get_session_type()
        if session != "Xorg":
            self.show_critical_error(f"You are on {session} session\nThis app only works on Xorg")
            return False

        # Read the configuration from config.json
        self.load_data()

        # These variables will be loaded from config.json
        try :
            self.file_path = self.data["user-settings"]["x"]["file_path"]
        except Exception as e:
            self.show_critical_error(str(e))
            return

        try :
            self.port_name = self.data["user-settings"]["x"]["default_port"]
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
        
        self.main_port_name = self.dummy_instance.main_port

        self.virtual_display_instance = VirtualDisplay(self.port_name)
        
        # if initialize is succesfull then return true
        return True
    
    def restore_defaults(self):
        self.data["user-settings"] = self.data["default"]

        self.save_user_settings()
        
        return self.initialize_app()

    def get_session_type(self):
        if os.getenv('WAYLAND_DISPLAY'):
            return 'Wayland'
        elif os.getenv('DISPLAY'):
            return 'Xorg'
        else:
            return 'Unknown'

    def clean_up(self):
        print("Cleaning up")
        # This function will be called when the program closes or crahes
        
        # Check the virtual display is connected or not
        if self.virtual_display_instance.status == True:
            # Unlug the virtual display
            self.virtual_display_instance.unplug_virtual_display()

        super().do_shutdown(self) # Call the parent class's shutdown method

    def handle_signal(self, signum, frame):
        self.clean_up()
        sys.exit(0)

    # UI FUNCTIONS

    def show_info_message(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self.main_window if self.main_window else None,
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
            transient_for=self.main_window if self.main_window else None,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Error",
        )
        dialog.format_secondary_text(message)  # Add detailed error message

        # Run the dialog and wait for user response
        response = dialog.run()

        # Destroy the dialog after the user responds
        dialog.destroy()

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
        status = self.dummy_instance.initialize(file_path, port_name)
        if status[0] == False:
            error_message = status[1]
            GLib.idle_add(self.show_error_message, error_message)
            return False # Return false, so user can enter a valid filepath
        else:
            self.data["user-settings"]["x"]["file_path"] = file_path
            self.data["user-settings"]["x"]["default_port"] = port_name

            # Write the new json file 
            return self.save_user_settings()
            
    
    def save_user_settings(self): # By writing into config.json file 
        try:
            with open("src/config.json", 'w') as json_file:
                json.dump(self.data, json_file, indent=4)  # indent=4 for pretty-printing
                return True
        except Exception as e:
            self.main_window.show_error_dialog(str(e))
            return False

    # FOR DEVELOPMENT 
    def print_dummy_variables(self):
        print("Portname is " + self.dummy_instance.port_name)
        print("Filepathh is " + self.dummy_instance.file_path)
        print("The status is  " + self.dummy_instance.check_status())


