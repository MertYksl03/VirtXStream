import os
import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk #type: ignore

from app import MyApp

# Check if the user has sudo privileges
def check_sudo():
    if os.geteuid() != 0:
        print("Error: This program requires sudo privileges to run.")
        sys.exit(1)
    else:
        return True

def main():
    app = MyApp()
    app.run(None)
    
if __name__ == "__main__":
    main()
 