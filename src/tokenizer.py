# @file tokenizer.py
# @author Joseph R Miles <me@josephrmiles.com>
# @date 2019-11-9
#
# This defines our Token and Tokenizer classes, used to perform the task of
# breaking the manuscript retreived from the input file into tokens that will
# be later parsed.

# Python standard lib imports
import re
from enum import Enum


class TokenType(Enum):
    NEWLINE = r"\n\r?"
    WHITESPACE = r"[ \t\f\v]+"
    BACKSLASH = r"\\"
    L_BRACE = r"{"
    R_BRACE = r"}"
    WORD = r"[^\s{}\\]+"
    NONE = r""

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, string):
        """ Checks if the input string matches the token type's pattern. If it
        does, True is returned along with the match object. Otherwise False and
        None are returned.
        """
        return re.fullmatch(self.pattern, string)


class Token():

    type = TokenType.NONE
    text = ""

    def __init__(self):
        pass

    def __str__(self):
        text = self.text.encode("unicode_escape").decode("utf8")
        return f"{self.type.name} \"{text}\""


class Tokenizer():
    """ A tokenizer object that parses input text into a list of tokens. """

    __source_text = None
    __tokens = []
    __cursor = 0

    def __init__(self, source_text):
        """ Initializes a new Tokenizer object. """
        self.__source_text = source_text

    def next_token(self):
        """ Fetches the next token from the source text. """

        token = Token()
        buffer = ""

        # While we still can read tokens
        while self.__cursor < len(self.__source_text):
            # Take the next character off the source text.
            buffer += self.__source_text[self.__cursor]

            # Find all token types that the buffer matches.
            matches = [ type for type in TokenType if type.match(buffer) is not None ]

            # If we don't have any matches and we already recognized the token,
            # exit so that we can finalize the token.
            if len(matches) is 0 and token.type is not TokenType.NONE:
                break

            # If we haven't recognized the token, or we no longer match the
            # previously recognized token type, update the token type to the
            # first of the matches we have recognized.
            #
            # note(jrm): This may not be the best idea in the world. Depending
            # on on the complexity of this language, we could run into a
            # situation where two token patterns have overlapping domains.
            # Arguably, this _shouldn't_ happen, but if it does, it creates a
            # small bug someone is bound to find and complain about.
            elif token.type is TokenType.NONE or token.type not in matches:
                token.type = matches[0]

            self.__cursor += 1

        # If we exited the loop without entering into the buffer, then we
        # reached the end of the source text and return None instead of a token
        # to indicate we can no longer fetch any more tokens.
        if len(buffer) is 0:
            return None

        # If the buffer isn't empty, finalize the token setting it's text to
        # the buffer, sans the last appended character. We can get away with
        # this since the last character is actually the character that
        # disqualified the token from being identifiable, therefore it is junk
        # information that we can remove.
        else:
            token.text = buffer[:-1]
            self.__tokens.append(token)

        return self.__tokens[-1]

    def tokens(self):
        """ Returns all tokens fetched so far. """
        return self.__tokens

