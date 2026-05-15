import os
import random
import sys

class command_handler:
    def __init__(self, output):
        self.output = output

    def recieve_command(self, raw, cmd):
        self.parsed_userin = raw
        method = getattr(self, cmd, None)
        method()

    def clear(self):
        self.output.clear()
        return