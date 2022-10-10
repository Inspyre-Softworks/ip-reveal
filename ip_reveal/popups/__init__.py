import PySimpleGUI as Gui
from ip_reveal.assets.ui_elements.icons.alerts import icons_alert_shield
from threading import Thread
from pypattyrn.behavioral.null import Null
from ip_reveal.config import args, LOG_DEVICE, PROG_NAME

GUI = Gui

LOG_NAME = f'{PROG_NAME}.gui.popups'

log = LOG_DEVICE.add_child(LOG_NAME)


audio_engine = None


try:
    import simpleaudio
    log.debug('Found audio engine')
    audio_engine = True
except ModuleNotFoundError:
    log.warning('No simpleaudio module found. Please install the simpleaudio package if you are wish to have audio '
                'notifications')
    log.warning('Forcing audio into mute state.')
    args.mute_all = True


log.debug('Checking to see if alerts are muted.')
if args.mute_all or not audio_engine:
    if not audio_engine:
        log.warning('No audio engine available please install simpleaudio if you wish to hear notifications.')
    else:
        log.warning('Alerts are muted!')
    bell = Null()
else:
    log.debug('Alerts are not muted. Loading alert class!')

    from ip_reveal.assets.sounds import Alerts
    bell = Alerts()
    log.debug('Alert class loaded!')


def notify(msg, duration=7000, alpha=.8, location=(750, 450), icon=icons_alert_shield):
    """
    
    Start the process that notifies the end-user of something important.
    
    Args:
        msg (str):
            The message you'd like delivered as a notification to the end-user
        
        duration (int):
            The time (in milliseconds) that the notification's popup should be visible.
        
        alpha (float|int):
            The alpha value for the notification popup. (Defaults to .8)
            
        location (tuple):
            The x,y pixel location on the screen where you'd like the popup notification to spawn. (Defaults to
            tuple(750, 450))
        icon:

    Returns:
        None

    """
    log = LOG_DEVICE.add_child(f'{LOG_NAME}.notify')

    log.debug('Received request to send notification to the desktop environment')

    log.debug('Playing alert bell.')
    bell.play()
    log.debug('Alert sound commenced.')
    log.debug('Sending visual alert.')

    log.debug('Notified')


def ip_change_notify(old, new, muted=False, log_device=None):
    """

    Play and alert sound and produce a notification in the center of the screen alerting the user that their external IP
    address has changed

    Args:

        old (str): The old IP Address, as recorded.

        new (str): The new IP Address that the machine now has, as recorded.
        
        muted (bool): Is the sound for the program muted? If bool(True); does not produce noise with notification.
        

    Returns:
        None

    """
    log = LOG_DEVICE.add_child(f'{LOG_NAME}.ip-change-notify')
    log.debug('IP change notification requested.')
    message = f'Your external IP address has changed from {old} to {new}'

    log.debug(f'Notification message {message}')

    notif = Thread(target=notify, args=(message,), daemon=True)

    log.debug(f'Build notification thread: {notif.getName()}')

    notif.start()
    GUI.popup_notify(
        message, display_duration_in_ms=duration, alpha=alpha,
        location=location, icon=icon
        )
    log.debug('Notification sent! ')
