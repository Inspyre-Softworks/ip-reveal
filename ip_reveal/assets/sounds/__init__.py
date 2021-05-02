from ip_reveal.assets.sounds import alerts
from playsound import playsound


class Alerts(object):
    def __init__(self):
        """
        Initialize an "Alerts" class that contains sounds for alerts.
        """
        self.asset_fp = alerts.ALERT_AUDIO_FP
        self.o_pulse_fp = alerts.O_PULSE_FP
        
    def play(self):
        playsound(self.o_pulse_fp)
