import PySimpleGUI as Gui
from ip_reveal.assets.ui_elements.icons.alerts import icons_alert_shield
from ip_reveal.assets.sounds import Alerts
from threading import Thread

GUI = Gui

bell = Alerts()
mute = None


def notify(msg, duration=7000, alpha=.8, location=(750, 450), icon=icons_alert_shield):
    if not mute:
        bell.play()

    GUI.popup_notify(msg, display_duration_in_ms=duration, alpha=alpha,
                     location=location, icon=icon)


def ip_change_notify(old, new, muted):
    """

    Play and alert sound and produce a notification in the center of the screen alerting the user that their external IP
    address has changed

    Args:

        old (str): The old IP Address, as recorded

        new (str): The new IP Address that the machine now has, as recorded

    Returns:
        None

    """
    global mute

    mute = muted

    message = f'Your external IP address has changed from {old} to {new}'
    notif = Thread(target=notify, args=(message,))
    notif.start()
