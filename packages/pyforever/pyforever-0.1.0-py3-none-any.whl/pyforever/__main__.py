#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import warnings
import subprocess

import watchgod


def run_script(args):
    # clear screen
    os.system("cls") if os.name == "nt" else os.system("clear")

    # run script and wait
    p = subprocess.Popen(args, shell=True)
    p.wait()


def main():
    if len(sys.argv) == 1:
        warnings.warn("No arguments supplied")
        exit(1)

    args = ["python"] + sys.argv[1:]

    # initial run
    run_script(args)

    # re-run the script if the current directory changes
    for changes in watchgod.watch("."):
        run_script(args)


if __name__ == "__main__":
    main()
