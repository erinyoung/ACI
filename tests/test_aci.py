import pytest
import subprocess

def run_command(cmd):
    stdout = subprocess.PIPE
    stderr = subprocess.PIPE

    proc = subprocess.Popen(cmd, shell=True, stdout=stdout, stderr=stderr)
    _, err = proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(f"FAILED: {cmd}\n{err}")

def test_aci():
    """test aci"""
    # CHANGED: aci.aci -> aci.cli
    cmd = (
        "python -m aci.cli -b tests/data/test.bam -d tests/data/test.bed -o tests -t 1"
    )
    run_command(cmd)

def test_version():
    """test aci"""
    # CHANGED: aci.aci -> aci.cli
    cmd = "python -m aci.cli -v"
    run_command(cmd)

def test_help():
    """test aci"""
    # CHANGED: aci.aci -> aci.cli
    cmd = "python -m aci.cli -h"
    run_command(cmd)