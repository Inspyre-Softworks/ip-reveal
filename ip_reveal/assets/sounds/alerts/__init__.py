from pathlib import Path

ALERT_AUDIO_FP = str(Path(__file__).parent.absolute())
"""
The absolute filepath (as a string) containing all 'alert' sounds.
"""

O_PULSE_FP = f"{ALERT_AUDIO_FP}/o-pulse-alert.wav"
"""
The absolute filepath (as a string) of the alert sound-file; 'o_pulse'
"""
