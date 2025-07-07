import pytest
import sys
from aci.utils.parse_args import get_parser, parse_args


def test_required_args():
    version = "1.2.3"
    parser = get_parser(version)
    args = parser.parse_args(["-b", "file1.bam", "-d", "amplicons.bed"])
    assert args.bam == ["file1.bam"]
    assert args.bed == "amplicons.bed"
    assert args.out == "aci"  # default
    assert args.loglevel == "INFO"  # default
    assert args.threads == 4  # default


def test_all_args():
    version = "1.2.3"
    parser = get_parser(version)
    args = parser.parse_args(
        [
            "-b",
            "file1.bam",
            "file2.bam",
            "-d",
            "amplicons.bed",
            "-o",
            "results_dir",
            "-log",
            "DEBUG",
            "-t",
            "8",
        ]
    )
    assert args.bam == ["file1.bam", "file2.bam"]
    assert args.bed == "amplicons.bed"
    assert args.out == "results_dir"
    assert args.loglevel == "DEBUG"
    assert args.threads == 8


def test_version_flag(capsys):
    version = "1.2.3"
    parser = get_parser(version)
    with pytest.raises(SystemExit) as e:
        parser.parse_args(["--version"])
    out, _ = capsys.readouterr()
    assert version in out
    assert e.value.code == 0


def test_missing_required_args():
    version = "1.2.3"
    parser = get_parser(version)
    with pytest.raises(SystemExit):
        parser.parse_args([])  # no args
    with pytest.raises(SystemExit):
        parser.parse_args(["-b", "file1.bam"])  # missing -d
    with pytest.raises(SystemExit):
        parser.parse_args(["-d", "amplicons.bed"])  # missing -b
