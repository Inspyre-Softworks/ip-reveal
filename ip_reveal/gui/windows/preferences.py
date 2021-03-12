import PySimpleGUIQt as gui


class Window(object):
    
    def __layout__(self):
        _ = [
                [gui.Text("Refresh interval: "), ]
                ]
    
    def __init__(self):
        """

        .. versionadded:: 1.0.1

        """
        self.active = False
