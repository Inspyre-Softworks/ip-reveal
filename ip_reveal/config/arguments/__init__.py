from argparse import ArgumentParser

from inspy_logger import LEVELS



class ArgParser(ArgumentParser):

    def __init__(self, **kwargs):
        """

        Instantiate an argument parser.

        """
        super().__init__()

        self.add_argument("--no-alerts", required=False, action='store_true', default=False,
                          help="If you use this flag it will set")

        self.add_argument('--mode', required=False, help='Not used')

        self.add_argument('--port', required=False, action='store', default=None, help='Not used')
        
        self.add_argument('-l', '--log-level',
                          action='store',
                          help="The level at which you'd like the logger to output.",
                          choices=LEVELS)

        # Argument to mute sounds
        self.add_argument('-m', '--mute-all',
                          action='store_true',
                          required=False,
                          help="Starts the program with all program audio muted.",
                          default=False
                        )

        sub_parsers = self.add_subparsers(dest='subcommands', help='The sub-commands for IP Reveal')

        ext_ip_parse = sub_parsers.add_parser('get-external',
                                              help='Return the external IP to the command-line and nothing else.')
        host_parse = sub_parsers.add_parser('get-host',
                                            help='Return the hostname to the command-line and nothing else.')
        local_parse = sub_parsers.add_parser('get-local',
                                             help='Return the local IP-Address to the command-line and nothing else.')


def parse():
    """

    The main driver for the arguments package, this will call on the ArgParser class and parse our arguments for us

    Returns:
        ArgsParser (object): A parsed ArgParser object which will have the namespace for the program's options.

    """

    # Instantiate our argument parser
    parser = ArgParser()

    return parser.parse_args()
