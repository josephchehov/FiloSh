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
        self.receivable = {}

        return self.process()

    def process(self):
        self.separate = re.findall(r'\[.*?\]|".*?"|-\w+|[\w./\\]+', self.plain)
        self.cmd = self.separate[0]
        self.command_ref = self.commands.get(self.separate[0])
        self.control = 0

        if self.command_ref == None: #- command not found
            return
        if len(self.separate) == len(self.command_ref) and (len(self.separate)-1 in (self.command_ref[0])): #- process command type
            if len(self.command_ref) <= 1: #- Command requires no arguments
                return {
                    "cmd": self.cmd
                }
            else: #- command requires atleast 1 argument
                self.receivable["cmd"] = self.cmd
                for i in range(1, len(self.separate)):
                    if self.command_ref[i] == "flag":
                        if self.checktype_flag(i):
                            self.receivable["flag"] = self.separate[i]
                            self.control += 1
                    elif self.command_ref[i] == "file":
                        if self.checktype_file(i):
                            self.receivable["file"] = self.separate[i]
                            self.control += 1
                    elif self.command_ref[i] == "path":
                        if self.checktype_path(i):
                            self.receivable["path"] = self.separate[i]
                            self.control += 1
                    elif self.command_ref[i] == "string":
                        if self.checktype_string(i):
                            self.separate[i] = self.separate[i].replace('"',"")
                            self.receivable["string"] = self.separate[i]
                            self.control += 1
                    elif self.command_ref[i] == "command":
                        if self.checktype_command(i):
                            self.receivable["command"] = self.separate[i]
                            self.control += 1
                    else:
                        if self.checktype_value(i):
                            self.receivable["value"] = self.separate[i]
                            self.control += 1
            if self.control == len(self.command_ref)-1:
                return self.receivable
            else:
                self.receivable = {}
        return

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