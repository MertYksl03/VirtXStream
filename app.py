import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib  # type: ignore

from gui.main_window import MainWindow
from gui.loading_window import LoadingWindow

import threading
import time

class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__()
        self.loading_window = None 


    def do_activate(self):
        # Show the loading screen
        self.loading_window = LoadingWindow()
        self.add_window(self.loading_window)
        self.loading_window.show_all()

        # Initialization in a separate thread
        threading.Thread(target=self.initialize_app, daemon=True).start()

    def initialize_app(self):
        time.sleep(5)
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
