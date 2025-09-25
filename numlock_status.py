import gi
import evdev
import distro
from evdev import InputDevice, list_devices, ecodes
gi.require_version('Gtk', '3.0')

if distro.name() == "Debian GNU/Linux" or distro.like() == "debian" or distro.name() == "Simply Linux":
    gi.require_version('AyatanaAppIndicator3', '0.1')
else:
    gi.require_version('AppIndicator3',        '0.1')

from gi.repository import Gtk, AyatanaAppIndicator3 as AppIndicator3, GLib

def show_popup_message(message, title="Message", message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK):
    dialog = Gtk.MessageDialog(
        parent=None,  # No parent window (standalone)
        flags=0,
        message_type=message_type,
        buttons=buttons,
        text=message
    )
    dialog.set_title(title)
    dialog.set_position(Gtk.WindowPosition.CENTER)

    response = dialog.run()

    dialog.destroy()


class NumLockIndicator:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            "numlock-indicator",
            "",  # default icon
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )

        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())

        self.keyboard = self.find_keyboard()

        if not self.keyboard:
            show_popup_message("Keyboard not found!\nUser not in group 'input' and can't read '/dev/input/events*'? You can fix via 'sudo usermod -aG input $USER' and relogin.",
                               title="numlock-indicator", message_type=Gtk.MessageType.ERROR)
            SystemExit(1)

        # Check status on init
        self.update_status()

        GLib.timeout_add_seconds(1, self.update_status)

    def find_keyboard(self):
        devices = [InputDevice(path) for path in list_devices()]
        for device in devices:
            if ecodes.KEY_NUMLOCK in device.capabilities().get(ecodes.EV_KEY, []):
                return device
        return None

    def create_menu(self):
        menu = Gtk.Menu()

        # Exit item
        quit_item = Gtk.MenuItem.new_with_label("Exit")
        quit_item.connect("activate", Gtk.main_quit)
        menu.append(quit_item)

        menu.show_all()
        return menu

    def update_status(self):
        try:
            if self.keyboard:
                leds = self.keyboard.leds()

                numlock_on = ecodes.LED_NUML in leds

                if numlock_on:
                    self.indicator.set_icon_full("zoom-original", "NumLock ON")
                else:
                    self.indicator.set_icon_full("go-up", "NumLock OFF")

        except Exception as e:
            print(f"Error: {e}")
            SystemExit(1)

        return True  # Return True to continue loop


if __name__ == "__main__":
    indicator = NumLockIndicator()
    Gtk.main()
