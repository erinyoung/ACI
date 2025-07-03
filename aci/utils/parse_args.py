"""Command-line argument parsing for the ACI analysis pipeline."""

import argparse


def get_parser(version):
    """
    Construct the argument parser.

    Args:
        version (str): Version string to show with --version.

    Returns:
        argparse.ArgumentParser: The argument parser object.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--bam",
        nargs="+",
        required=True,
        type=str,
        help="(required) input bam file(s)",
    )
    parser.add_argument(
        "-d", "--bed", required=True, type=str, help="(required) amplicon bedfile"
    )
    parser.add_argument(
        "-o",
        "--out",
        required=False,
        type=str,
        help="directory for results",
        default="aci",
    )
    parser.add_argument(
        "-log",
        "--loglevel",
        required=False,
        type=str,
        help="logging level",
        default="INFO",
    )
    parser.add_argument(
        "-t",
        "--threads",
        required=False,
        type=int,
        help="specifies number of threads to use",
        default=4,
    )
    parser.add_argument(
        "-v",
        "--version",
        help="print version and exit",
        action="version",
        version=version,
    )

    return parser


def parse_args(version):
    """
    Parse command-line arguments.

    Args:
        version (str): Version string to show with --version.

    Returns:
        argparse.Namespace: Parsed arguments.
    """

    parser = get_parser(version)
    return parser.parse_args()
