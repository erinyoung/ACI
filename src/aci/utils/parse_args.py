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
    
    # --- Input / Output ---
    parser.add_argument(
        "-b",
        "--bam",
        nargs="+",
        required=True,
        type=str,
        help="(required) input bam file(s). Supports wildcards or space-separated lists.",
    )
    parser.add_argument(
        "-d", 
        "--bed", 
        required=True, 
        type=str, 
        help="(required) amplicon bedfile (4-column format)"
    )
    parser.add_argument(
        "-o",
        "--out",
        required=False,
        type=str,
        help="directory for results (default: aci)",
        default="aci",
    )

    # --- Performance / System ---
    parser.add_argument(
        "-t",
        "--threads",
        required=False,
        type=int,
        help="specifies number of threads to use for sorting and counting (default: 4)",
        default=4,
    )
    parser.add_argument(
        "--tmpdir",
        required=False,
        type=str,
        help="custom directory for temporary files (default: system tmp)",
        default=None,
    )

    # --- QC Thresholds ---
    parser.add_argument(
        "--fail-threshold",
        required=False,
        type=int,
        default=10,
        help="Minimum depth to consider an amplicon 'passed' (default: 10)",
    )
    parser.add_argument(
        "--fail-percentage",
        required=False,
        type=float,
        default=50,
        help="Percentage of samples that must fail for an amplicon to be flagged (default: 50)",
    )

    # --- Logging / Meta ---
    parser.add_argument(
        "-log",
        "--loglevel",
        required=False,
        type=str,
        help="logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) (default: INFO)",
        default="INFO",
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