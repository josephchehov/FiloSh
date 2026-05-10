import re
import os

class command_parser:
    def parse(self, raw):
        self.plain = raw
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
        self.commands = {
            "prdir": [[1], "flag"],
            "chdir": [[1], "path"],
            "data": [[1], "file"],
            "read": [[1,3], "file", "flag", "value"],
            "delete": [[1,2], "file", "flag"],
            "copy": [[2], "file", "path"],
            "move": [[2], "file", "path"],
            "write": [[3], "file", "string", "flag"],
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
        self.separate = re.findall(r'\[.*?\]|".*?"|-\w+|[\w./\\]+', self.plain)
        self.cmd = self.separate[0]
        self.command_ref = self.commands.get(self.separate[0])

        if self.command_ref == None: #- command not found
            return print(f"Unrecognized command '{self.separate[0]}'. Use help for a list of working commands.")
        if len(self.separate) == len(self.command_ref) and (len(self.separate)-1 in (self.command_ref[0])): #- process command type
            if len(self.separate) <= 1: #- No argument command found
                return self.separate[0]
            else: #- command word & arguments are formatted correctly
                for i in range(1, len(self.separate)):
                    if self.command_ref[i] == "flag":
                        self.checktype_flag(i)
                    elif self.command_ref[i] == "file":
                        self.checktype_file(i)
                    elif self.command_ref[i] == "path":
                        self.checktype_path(i)
                    elif self.command_ref[i] == "string":
                        self.checktype_string(i)
                    elif self.command_ref[i] == "command":
                        self.checktype_command(i)
                    else:
                        self.checktype_value(i)
        return self.plain

    def checktype_flag(self, index):
        if self.separate[index] in self.flags: #- flag exists
            if self.cmd in self.flags.get(self.separate[index]): #- flag matches command
                    return True
        return False
    
    def checktype_file(self, index):
        self.local_files = os.listdir(os.getcwd())
        if self.separate[index] in self.local_files: #- file found in current working directory
            return True
        return False
    
    def checktype_string(self, index):
        if self.separate[index].startswith('"') and self.separate[index].endswith('"'):
            content = self.separate[index][1:-1]
            if '"' not in content: #- correctly formatted string
                return True
        return False
    
    def checktype_command(self, index): #- implementing command entry validation later
        return

    def checktype_value(self, index):
        return self.separate[index].isdigit()
    
    def checktype_path(self, index):
        return os.path.exists(self.separate[index])