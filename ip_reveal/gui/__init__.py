from logging import getLogger

log = getLogger("gui.__init__")

try:
    log.debug("Trying to start GUI")
    import PySimpleGUIQt as Qt
except ImportError:
    log.warning("Loading GUI failed. Falling back on CLI")
    Qt = False
