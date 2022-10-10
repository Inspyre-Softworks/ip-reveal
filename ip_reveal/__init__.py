import socket
import sys
from platform import node
from socket import gaierror
from urllib.error import URLError
from ip_reveal.config import PARSED_ARGS, CMD_ALIASES, LOG_DEVICE

from inspy_logger import LEVELS as LOG_LEVELS, getLogger
from inspy_logger import InspyLogger
from inspyred_print import Color, Format
from requests import get
from requests.exceptions import ConnectionError
from urllib3.exceptions import MaxRetryError
from threading import Thread

from ip_reveal.assets.ui_elements.backgrounds import NEON_DARK_FP
from ip_reveal.assets.ui_elements.icons import app_main_24x24
from ip_reveal.assets.ui_elements.icons import app_quit_50x50_fp
from ip_reveal.assets.ui_elements.icons import app_refresh_50x50_fp
from ip_reveal.assets.ui_elements.icons import app_copy_32x32 as copy_icon

from ip_reveal.gui.menus import top_menu_layout, rc_menu_layout
from ip_reveal.gui.windows.about import AboutWindow
from ip_reveal.gui.windows.preferences import PreferencesWindow

from ip_reveal import config

# import ip_reveal.timers as timer
import humanize
from inspyre_toolbox.live_timer import Timer
from ip_reveal.tools import commify

import PySimpleGUIQt as Qt
import pyperclip

quit_icon = app_quit_50x50_fp
refresh_icon = app_refresh_50x50_fp

end = Format().end_mod
color = Color()
red = color.red

update_window_timer = None

timer = Timer()
timer.start()

cached_ext_ip = None
ip_hist = []

inet_down = False
log_device = None
args = config.args

config = config.CONFIG


def get_hostname():
    """
    get_hostname

    Fetch the system's apparent hostname and return it to the caller

    Returns:
        str: The system's apparent hostname contained within a string.
    """

    # Prepare the logger
    _log = getLogger(f'{log_name}.get_hostname')
    _debug = _log.debug

    # Fetch the hostname from platform.node
    hostname = node()
    _debug(f'Checked hostname and found it is: {hostname}')

    # Return this to the caller
    return hostname


def push_notification(old_ip, new_ip):
    """
    
    Push a notification through the GUI with a sound.
    
    
    Args:
        old_ip (str):
            The IP that was held previously.
        
        new_ip (str):
            The new - currently held - IP address
            

    Returns:
        None

    """
    from ip_reveal.popups import ip_change_notify

    ip_change_notify(old_ip, new_ip)


def get_external():
    """
    get_external

    Fetch the system's apparent hostname and return it to the caller in the form of a string.

    Returns:
        str: The system's apparent external IP-Address in the form of a string.
    """
    global cached_ext_ip, inet_down, ip_hist

    # Prepare the logger
    _log = getLogger(f'{log_name}.get_external')
    _debug = _log.debug

    # Try contacting IPIFY.org with a basic request and read the returned text.
    #
    # If we are unable to connect to this outside service, it's likely that Internet connection has dropped. There
    # are - however, instances where this service is down, and for these reasons we want to have at least one
    # alternative to control for failure on a Singular -free- AI API.

    # Fetch the external IP-Address from IPIFY.org
    try:
        external = get('https://api.ipify.org').text
        _debug(f'Checked external IP and found it is: {external}')

    # Catch the "ConnectionError" exception that is raised when the "requests" package is unable to reach
    # "IPIFY.org", simply reporting this occurred (if the logger is listening) before (maybe first; attempt connection
    # to another service?)
    except (ConnectionError, MaxRetryError, gaierror, URLError) as e:
        if not inet_down:
            _log.warning("Unable to establish an internet connection.")
            inet_down = True
        external = None

    if external is None:
        return False

    if not cached_ext_ip:
        cached_ext_ip = external
        if cached_ext_ip != external:
            push_notification(cached_ext_ip, external)
            cached_ext_ip = external

    if len(ip_hist) == 0:
        _debug("Added first IP to history list.")
        ip_hist.append(external)
        _debug(f"IP History: {ip_hist}")

    # Return the text result we get from the API to the caller.
    return external


def get_internal():
    """
    get_internal

    Fetch the system's local IP-Address and return it to the caller in the form of a string.

    Returns:
        str: The system's local IP-Address contained within a string.
    """

    # Set up a logger
    _log = getLogger(f'{log_name}.get_internal')

    # Alias the debug entry call
    _debug = _log.debug

    # Start a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Attempt a connection to an arbitrary host
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))

        # Fetch our IP from this socket's metadata
        IP = s.getsockname()[0]

    # Should we raise an exception we won't bother handling it, we'll just return the loopback address to the caller.
    except Exception:
        IP = '127.0.0.1'

    # No matter the result, let's remember to close the socket.
    finally:
        s.close()

    # Announce that we've found an IP
    _debug(f'Checked internal IP and found: {IP}')

    # Return a string containing the result to the caller.
    return IP


def update_window(values=None):
    global log_device, args
    from ip_reveal.popups import ip_change_notify
    """

    A function that handles the following processes for updating the IP Reveal window:

      * Updating all relevant fields
      * Resetting accumulators
      * Incrementing refresh stats (if opted in)
      * Fetching the information for external and internal IP addresses
      * Calls a refresh on the timer.

    NOTE:
        It is not advisable to utilize this function in a loop without limiting how often it's run. You could end up
        DoSing yourself or others.

    Returns:
        None

    """
    global acc, refresh_num, timer, cached_ext_ip, ip_hist

    # Start the logger for this operation
    _log = getLogger(f'{log_name}.update_window')

    # If set to do so; spit out some debug data
    u_debug = _log.debug
    u_debug('TIMEOUT - Refreshing window...')
    u_debug(f'acc = {str(acc)}')

    # Reset the frame accumulator
    acc = 0

    # Spit out some more useful info, if allowed.
    u_debug(f'Reset acc accumulator new value: {acc}')
    u_debug('Incrementing refresh count...')

    # For stats purposes only; increment our count of window refreshes.
    refresh_num += 1

    # Grab our fresh data for diplaying to the window
    ip = get_external()

    if not ip:
        ip = "Offline"

    local_ip = get_internal()
    hostname = get_hostname()

    # Call a 'refresh()' on our timer object. This will start another cycle to keep track of. This allows the timer
    # routine to always track the time since last data fetching
    #timer.reset()
    timer = Timer()
    timer.start()

    t_color = "red" if ip == "Offline" else "green"
    # Update the relevant fields with our fresh data
    window['PUBLIC_OUT'].update(ip, text_color=t_color)
    window['LOCAL_OUT'].update(local_ip)
    window['HOSTNAME_OUT'].update(hostname)
    window['TIME_SINCE_Q_OUT'].update("Just now...")

    # Make some notes in the debug log that might be useful
    u_debug(f'Updated window with new values: {values}')
    u_debug(f'This was refresh number {refresh_num}')

    if ip != cached_ext_ip:
        ip_change_notify(cached_ext_ip, ip, args.mute_all)
        cached_ext_ip = ip
        ip_hist.append(ip)


def safe_exit(win, exit_reason):
    _log = getLogger(f'{log_name}.safe_exit')

    tmp_hist = []
    for ip in ip_hist:
        if ip not in tmp_hist:
            tmp_hist.append(ip)

    _log.info(f"During operation you switched IP addresses {len(ip_hist) - 1} times.")
    _log.info(f"Held IP addresses: {tmp_hist}")
    _log.info(f"Exiting safely. Reason: {exit_reason}")
    _log.info(f"The IP address was refreshed {refresh_num} times")
    _log.info(f"Window underwent {total_acc} cycles")
    print(timer.start_time)

    win.close()
    sys.exit()


# Set up a name for our logging device
log_name = "IPReveal"

# Declare a variable named 'acc' for our accumulator and set it at int(0)
acc = 0

# For statistics tracking; declare a variable called 'refresh_num' and start it at 0
refresh_num = 0

# ...and one that will hold our total cycle count
total_acc = 0

# Set up a placeholder variable for our window object
window = None

# Set up two variables that will act as caches for the external and internal IPs
cached_ext_ip = None
cached_int_ip = None

acc2 = 0


def main():
    """
    
    This is the main function to run the IP-Reveal program
    
    Returns:
        None

    """
    global total_acc, acc, refresh_num, window, log_device, argsNew
    from ip_reveal.popups import ip_change_notify


    # Timer text
    t_text = "Just now..."

    # Qt.theme('DarkBlue3')

    # Start the logging device
    log = LOG_DEVICE.add_child(log_name)
    debug = log.debug

    # Announce that we did that
    debug('Started my logger!')
    log = getLogger(log_name + '.Main')
    # Alias the log.debug signature for ease-of-use
    debug = log.debug
    print(args.subcommands)
    # See if we got one of the subcommands assigned.
    if args.subcommands in CMD_ALIASES.get_public:
        print(get_external())
        exit()
    elif args.subcommands in CMD_ALIASES.get_host:
        print(get_hostname())
        exit()
    elif args.subcommands in CMD_ALIASES.get_local:
        print(get_internal())
        exit()
    elif args.subcommands in CMD_ALIASES.get_all:
        print(f"{get_hostname()}@({get_internal()}|{get_external()})")
        exit()
    elif args.subcommands in CMD_ALIASES.test_audio:
        from ip_reveal.assets.sounds import run_audio_test
        run_audio_test(args.countdown, args.full, args.log_level)
        exit()

    status_bar_layout = [

    ]

    bg_color = "340245"
    size = (220, 50)
    alpha = 1
    if alpha >= 1:
        text_background_color = "pink"
    else:
        text_background_color = "white"

    layout = [
        [Qt.Menu(top_menu_layout)],
        [
            Qt.Text(
                'Public IP:', background_color=text_background_color, text_color="black",
                relief=Qt.RELIEF_GROOVE,
                size_px=size, auto_size_text=True, justification='center',
            ),
            Qt.Text(
                get_external(), relief=Qt.RELIEF_SUNKEN, key='PUBLIC_OUT',
                background_color=text_background_color,
                text_color="black", size_px=size, auto_size_text=True, justification='center'
            ),
            Qt.Button(
                '',
                tooltip='Copy the IP to clipboard.',
                enable_events=True,
                image_data=copy_icon,
                key='PUBLIC_COPY',
                size_px=size,
                button_color=("#000000", "#000000")
            )
        ],

        [
            Qt.Text(
                'Local IP:', background_color=text_background_color, text_color="black",
                relief=Qt.RELIEF_GROOVE,
                size_px=size, auto_size_text=True, justification='center'
            ),
            Qt.Text(
                get_internal(), key='LOCAL_OUT', relief=Qt.RELIEF_SUNKEN,
                background_color=text_background_color,
                text_color="black", size_px=size, auto_size_text=True, justification='center'
            ),
            Qt.Button(
                '',
                tooltip='Copy the IP to clipboard.',
                enable_events=True,
                image_data=copy_icon,
                key='LOCAL_COPY',
                size_px=size,
                button_color=("#000000", "#000000")
            )
        ],
        [
            Qt.Text(
                'Hostname:', background_color=text_background_color, text_color="black",
                relief=Qt.RELIEF_GROOVE,
                size_px=size, auto_size_text=True, justification='center'
            ),
            Qt.Text(
                get_hostname(), key='HOSTNAME_OUT', relief=Qt.RELIEF_SUNKEN,
                background_color=text_background_color,
                text_color="black", size_px=size, auto_size_text=True, justification='center'
            ),
            Qt.Button(
                '',
                tooltip="Copy the hostname to clipboard.",
                enable_events=True,
                image_data=copy_icon,
                key='HOSTNAME_COPY',
                size_px=size,
                button_color=(None, "#000000")

            )
        ],
        [
            Qt.Text(
                f"Last checked", background_color=text_background_color, text_color="black",
                relief=Qt.RELIEF_GROOVE, size_px=size, auto_size_text=True, justification='center'
            ),
            Qt.Text(
                t_text, key="TIME_SINCE_Q_OUT", relief=Qt.RELIEF_SUNKEN, background_color=text_background_color,
                text_color="black", size_px=size, auto_size_text=True, justification='center'
            )
        ],
        [
            Qt.Button(
                '', key='MAIN_CLOSE_BUTTON',
                image_filename=app_quit_50x50_fp,
                image_size=(50, 50),
                button_color=(None, "#ff0000"),
                tooltip="Quit IP Reveal"
            ),
            Qt.Button(
                '', key='MAIN_REFRESH_BUTTON',
                image_filename=app_refresh_50x50_fp,
                image_size=(50, 50),
                button_color=(None, "#ff0000"),
                tooltip="Refresh"
            )
        ],
    ]

    print(layout)

    # Assemble the above widget into a window.
    window = Qt.Window(
        'IP-Reveal by Inspyre Softworks', layout=layout,
        background_image=NEON_DARK_FP,
        icon=app_main_24x24,
        size=(300, 400),
        alpha_channel=alpha,
        grab_anywhere=True,
        background_color="white"
    )

    # Start our main GUI loop.
    while True:
        event, values = window.read(timeout=100)

        # Set up a child logger that will log window events.
        w_log = getLogger(log_name + '.MainWindow')
        w_debug = w_log.debug

        # Increment the cycle count
        acc += 1
        total_acc += 1

        t = int(timer.get_elapsed(seconds=True))
        t_text = humanize.naturaldelta(t)

        window['TIME_SINCE_Q_OUT'].update(f"{t_text} ago...")

        if 'USER' in config.parser.sections():
            section = 'USER'
        else:
            section = 'DEFAULTS'

        # If the accumulator is at 325 counts, alert the user, update the window, and reset the accumulator
        if t >= int(config.parser[section].getint('refresh_interval')):
            w_debug('Calling function to update the window...')

            try:
                update_window()
            except ImportError:
                log.warning('Failed to update the window...')

            # window['TIME_SINCE_Q_OUT'].update('Refreshing...')
            # update_win = Thread(target=update_window)
            #
            # update_win.start()
            w_debug('Updated window!')

        # If the 'Close' button is pressed: we exit.
        if event is None or event == 'MAIN_CLOSE_BUTTON':
            e_reason = f"It seems the user closed the window, received {values}"
            if event == 'MAIN_CLOSE_BUTTON':
                e_reason = 'The close button was pressed'
            safe_exit(window, exit_reason=e_reason)

            w_log.info("User initiated closing")

            break

        # Check for top-menu events
        if event == 'About':
            about_window = AboutWindow()
            about_window.run()
        if event == 'Preferences':
            pref_window = PreferencesWindow()
            pref_window.run()
            pref_window.window.close()

        if event == 'MAIN_REFRESH_BUTTON':
            w_debug('Calling a refresh on the window')
            update_window()
            w_debug('All seems well!')

        if event.endswith('COPY'):
            wcopy = event.split('_')[0]
            pyperclip.copy(window[f'{wcopy}_OUT'].DisplayText)
            w_log.debug(f'Copied {wcopy} to clipboard')


if __name__ == '__main__':
    main()
