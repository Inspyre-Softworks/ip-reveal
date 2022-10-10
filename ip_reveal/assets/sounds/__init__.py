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
    from ip_reveal.config import args, LOG_DEVICE, PROG_NAME
    
    
    def __init__(self):
        """
        Initialize an "Alerts" class that contains sounds for alerts.
        """
        self.log_name = f'{self.PROG_NAME}.assets.sounds.Alerts'
        self.log = self.LOG_DEVICE.add_child(self.log_name)
        self.log.debug('Instantiating!')
        self.asset_fp = alerts.ALERT_AUDIO_FP
        self.log.debug(f"Using the following file for alert sounds: {self.asset_fp}.")
        self.o_pulse_fp = alerts.O_PULSE_FP
        self.sound = self.sa.WaveObject.from_wave_file(self.o_pulse_fp)
        self.log.debug("Loaded sound file.")
        
    def play(self):
        """
        
        Play the audible alert sound when called.
        
        Returns:
            None

        """
        log = self.LOG_DEVICE.add_child(f'{self.log_name}.play')
        log.debug('Received request to play alert sound.')
        self.sound.play()
        log.debug('Finished playing alert sound!')
