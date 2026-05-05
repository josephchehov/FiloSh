import re

class command_parser:
    def parse(self, raw):
        parsed = raw
        flags = {
            "-home": ["prdir"],
            "-work": ["prdir"],
            "-head": ["read"],
            "-tail": ["read"],
            "-perm": ["delete"],
            "-appd": ["write"],
            "-over": ["write"],
            "-sesh": ["time"],
            "-base": ["time"],
            "-acpt": ["time"]
        }
        content = ["string", "command"]
        commands = {
            "prdir": [[1], "flag"],
            "chdir": [[1], "path"],
            "data": [[1], "file"],
            "read": [[1,3], "file", "flag", "value"],
            "delete": [[1,2], "file", "flag"],
            "copy": [[2], "file", "path"],
            "move": [[2], "file", "path"],
            "write": [[3], "file", "content", "flag"],
            "log": [[0,1], "path"],
            "history": [[1], "command"],
            "clear": None,
            "list": None,
            "help": None,
            "time": [[1], "flag"]
        }
        return parsed