
import argparse

argument_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
argument_parser.add_argument(
    "--version",
    "-v",
    help="Show version of MCSL-Sync",
    action="store_true",
    default=False,
)
argument_parser.add_argument(
    "--core-list",
    "-cl",
    help="Show available core list",
    action="store_true",
    default=False,
)
argument_parser.add_argument(
    "--update-default",
    "-ud",
    help="Update default core list",
    action="store_true",
    default=False,
)
argument_parser.add_argument(
    "--init",
    "-i",
    help="Init MCSL-Sync configuration",
    action="store_true",
    default=False,
)
argument_parser.add_argument(
    "--server",
    "-s",
    help="Run MCSL-Sync API server",
    action="store_true",
    default=False,
)