from ip_reveal.assets.sounds import alerts


def run_audio_test(countdown=3, full=False, log_level='debug'):
    """
    
    Run a left-right channel audio-test to ensure 'simpleaudio' is working correctly.
    
    Returns:
        None

    """
    from inspy_logger import InspyLogger
    
    isl = InspyLogger('IP-Reveal.assets.sounds.run_audio_test', log_level)
    log = isl.device.start()
    
    log.debug('Importing "simpleaudio"...')
    
    from simpleaudio.functionchecks import LeftRightCheck as LRC, run_all
    
    log.debug('Done!')
    log.debug('Determining test type....')
    log.debug(f'Full test: | {full}')
    log.debug(f'Countdown: | {countdown}')
    
    if not full:
        LRC.run(countdown=countdown)
    else:
        run_all(countdown=countdown)
    

class Alerts(object):
    
    import simpleaudio as sa
    from ip_reveal.config import args
    
    def __init__(self):
        """
        Initialize an "Alerts" class that contains sounds for alerts.
        """
        self.asset_fp = alerts.ALERT_AUDIO_FP
        self.o_pulse_fp = alerts.O_PULSE_FP
        self.sound = self.sa.WaveObject.from_wave_file(self.o_pulse_fp)
        
        
        
    def play(self):
        self.sound.play()
