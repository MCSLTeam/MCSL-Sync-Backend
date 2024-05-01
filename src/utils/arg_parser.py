
import argparse

argument_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
argument_parser.add_argument(
    "-v",
    "--version",
    help="Show version of MCSL-Sync",
    action="store_true",
    default=False,
)
argument_parser.add_argument(
    "-cl",
    "--core-list",
    help="Show available core list",
    action="store_true",
    default=False,
)
argument_parser.add_argument(
    "-u",
    "--update",
    help="Update core list",
    action="store_true",
    default=False,
)
argument_parser.add_argument(
    "-i",
    "--init",
    help="Init MCSL-Sync configuration",
    action="store_true",
    default=False,
)
argument_parser.add_argument(
    "-s",
    "--server",
    help="Run MCSL-Sync API server",
    action="store_true",
    default=False,
)
argument_parser.add_argument(
    "-o",
    "--optimize",
    help="Optimize Database",
    action="store_true",
    default=False,
)
argument_parser.add_argument(
    "-n",
    "--add-node",
    help="Add a MCSL-Sync-Nodeside Client",
    type=str,
    default=None,
)