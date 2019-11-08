# @file pilcrow.py
# @author Joseph R Miles <me@josephrmiles.com>
# @date 2019-11-8
#
# This is the entry point for the Pilcrow application.
#
# Pilcrow is a single-input, multi-output markup format. Inspired by LaTex,
# Pollen, and Pandoc, Pilcrow aims to be a straight-forward and simple to use
# formatting language and markup system that gives authors maximum control over
# their document design. Write once, display everywhere.

import sys, argparse

PILCROW = "¶"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("input")

    args = parser.parse_args(sys.argv[1:])

    if args.input:
        manuscript = None

        with open(args.input, "r") as in_file:
            manuscript = in_file.read()

        print(manuscript)
