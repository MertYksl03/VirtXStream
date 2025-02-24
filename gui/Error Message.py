import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk #type: ignore

def on_button_clicked(button):
    try:
        # Code that might raise an exception
        result = 10 / 0  # Example: Division by zero
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, show an error dialog to the user
        dialog = Gtk.MessageDialog(
            parent=None,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Error",
        )
        dialog.format_secondary_text(str(e))
        dialog.run()
        dialog.destroy()

# Create a simple GTK window with a button
window = Gtk.Window(title="Error Handling Example")
button = Gtk.Button(label="Click Me")
button.connect("clicked", on_button_clicked)
window.add(button)
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()