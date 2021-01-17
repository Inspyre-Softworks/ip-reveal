from argparse import ArgumentParser
from inspy_logger import LEVELS as LOG_LEVELS


class Reader(object):

    def __init__(self):
        """

        Instantiate an argument parser.

        """

        self.parser = ArgumentParser("ip-reveal",
                                     description="Monitors your external IP address.",
                                     allow_abbrev=True,
                                     add_help=True)

        self.parser.add_argument('-l', '--log-level',
                                 nargs='?',
                                 choices=LOG_LEVELS,
                                 default='info'
                                 )

        # Argument to mute sounds
        self.parser.add_argument('-m', '--mute-all',
                                 action='store_true',
                                 required=False,
                                 help="Starts the program with all program audio muted.",
                                 default=False
                                 )

        self.sub_parsers = self.parser.add_subparsers(
            dest='subcommands', help='The sub-commands for IP Reveal')

        ext_ip_parse = self.sub_parsers.add_parser('get-external',
                                                   help='Return the external IP to the command-line and nothing else.')

        ext_ip_parse.add_argument('-p', '--popup',
                                  help='Return information in a GUI popup window.',
                                  action='store_true',
                                  required=False,
                                  default=False
                                  )

        host_parse = self.sub_parsers.add_parser(
            'get-host', help='Return the hostname to the command-line and nothing else.')

        host_parse.add_argument('-p', '--popup',
                                help='Return information in a GUI popup window.',
                                action='store_true',
                                required=False,
                                default=False
                                )

        local_parse = self.sub_parsers.add_parser('get-local',
                                                  help='Return the local IP-Address to the command-line and nothing '
                                                       'else.')

        local_parse.add_argument('-p', '--popup',
                                 help='Return information in a GUI popup window.',
                                 action='store_true',
                                 required=False,
                                 default=False
                                 )

        network_parse = self.sub_parsers.add_parser('get-network-info',
                                                    help='Return all three: hostname, local ip, and '
                                                         'external ip to the commandline')
        network_parse.add_argument('-p', '--popup',
                                   help='Return information in a GUI popup window.',
                                   action='store_true',
                                   required=False,
                                   default=False
                                   )

        doc_parse_gh = self.sub_parsers.add_parser('get-github',
                                                   help="Return the link to IP Reveal's Github repo")

        doc_parse_gh.add_argument('-p', '--popup',
                                  help='Return information in a GUI popup window.',
                                  action='store_true',
                                  required=False,
                                  default=False
                                  )

        self.parsed = self.parser.parse_args()
