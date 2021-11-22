

class NetworkTools(IPReveal):
    def __init__(self):
        super().__init__()

        self.hostname = None
        """ Won't have a value until `.get_hostname` is run """


    def get_hostname(self):
        """
        get_hostname

        Fetch the system's apparent hostname and return it to the caller

        Returns:
            str: The system's apparent hostname contained within a string.
        """

        # Prepare the logger

        _debug = _log.debug

        # Fetch the hostname from platform.node
        self.hostname = node()
        _debug(f'Checked hostname and found it is: {hostname}')

        # Return this to the caller
        return hostname
