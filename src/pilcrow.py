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

# Python standard lib imports
import sys, argparse, os

# Pilcrow lib imports
from tokenizer import Tokenizer


PILCROW = "¶"


class Pilcrow():
    """ A Pilcrow application instance. """

    __handlers = {}

    def __init__(self):
        """ Initializes a new Pilcrow object. """
        pass

    def register(self, handler):
        """ Registers a new handler function with this Pilcrow object. """
        self.__handlers[handler.__name__] = handler

    def handle(self, file_contents, output_format):
        """ Takes the given file contents and invokes the handler appropriate
        for the target output format. """
        return self.__handlers[output_format](file_contents)


pilcrow = Pilcrow()

@pilcrow.register
def txt(file_contents):
    return file_contents


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("input")
    parser.add_argument("-o", "--output", dest="output", nargs="?")

    args = parser.parse_args(sys.argv[1:])


    manuscript = None

    with open(args.input, "r") as in_file:
        manuscript = in_file.read()


    def tokenize(string):
        tokenizer = Tokenizer(string)

        token = tokenizer.next_token()

        while token is not None:
            token = tokenizer.next_token()


    tokenize(manuscript)


    out_filepath = None

    # If the user didn't specify an output file, we'll just infer the output
    # filename from the given input filename.
    if args.output:
        out_filepath = args.output

    else:
        f = os.path.basename(args.input)
        # todo(jrm): Later we will get the output file extension from the user,
        # but for now we'll just stick with outputting .txt files.
        out_filepath = os.path.splitext(f)[0] + ".txt"


    output_format = os.path.splitext(out_filepath)[1][1:]

    with open(out_filepath, "w") as out_file:
        out_file.write(pilcrow.handle(manuscript, output_format))
