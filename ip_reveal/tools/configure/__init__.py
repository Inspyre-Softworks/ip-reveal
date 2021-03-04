class Settings(object):
    def __init__(self):
        pass
    
    @property
    def privacy_defaults(self):
        """

        Returns:

        """
        _ = {
                "no_phone_home": False,
                
                "stats"        : {
                        "collect": True,
                        "send"   : False,
                        },
                
                "gui"          : {
                        "grab_anywhere": True,
                        "theme"        : "rapture"
                        }
                
                "gui.advanced":
                }
        
        return _
