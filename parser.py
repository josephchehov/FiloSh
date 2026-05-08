import re

class command_parser:
    def parse(self, raw):
        self.parsed = raw
        self.flags = {
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
        self.content = ["string", "command"]
        self.commands = {
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
            "clear": [[0]],
            "list": [[0]],
            "help": [[0]],
            "time": [[1], "flag"]
        }
        
        self.split = self.split_string()
        return self.split


    def split_string(self):
        self.separate = re.findall(r'\[.*?\]|".*?"|-\w+|[\w./\\]+', self.parsed)
        self.size_ref = self.commands.get(self.separate[0])

        if self.size_ref == None: #- command not found
            return print(f"Unrecognized command '{self.separate[0]}'. Use help for a list of working commands.")
        if len(self.separate) == len(self.size_ref): #- process command type
            if len(self.separate) <= 1: #- No argument commands
                return self.separate[0]
            else:
                if self.separate[1] == "flag":
                    self.checktype_flag()
                elif self.separate[1] == "file":
                    self.checktype_file()
                elif self.separate[1] == "path":
                    self.checktype_path()
                elif self.separate[1] == "command":
                    self.checktype_command()
        return

    def checktype_flag(self):
        return
    
    def checktype_file(self):
        return
    
    def checktype_command(self):
        return
    
    def checktype_path(self):
        return