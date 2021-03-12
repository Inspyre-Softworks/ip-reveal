import PySimpleGUI as Gui

from threading import Thread
from ip_reveal.assets.ui_elements.icons import tp_github
from ip_reveal.assets.ui_elements.icons.alerts import icons_alert_shield

try:
    import simpleaudio
except ModuleNotFoundError as e:
    print("No audio package found!")
    audio_avail = False
else:
    from ip_reveal.assets.sounds import Alerts
    
    audio_avail = True

from .errors import InvalidProjInfoRequestError

GUI = Gui

if audio_avail:
    bell = Alerts()
    mute = False
else:
    bell = None
    mute = True


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


def net_info(info):
    """

    Produce and display a popup window giving a user some quick info.

    Args:
        info (str): A string containing the information to be given to the user.

    Returns:
        None

    NOTE:
        This function does not change/format the string provided in the 'info' parameter.

    """
    GUI.PopupOK(info, title='Network Information')


def proj_info(req_info):
    choices = ['github', 'rtd', 'issue']
    icon=None
    link=None
    gh_icon = tp_github
    if req_info not in choices:
        raise InvalidProjInfoRequestError(choices=choices, made_choice=req_info)
    if req_info.lower() == 'github':
        icon = gh_icon
        req_info = 'Github'
        link="https://github.com/Inspyre-Softworks/ip-reveal"
    GUI.Popup(link, title=f"{req_info} - Project Information", icon=icon)
