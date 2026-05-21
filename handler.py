import os
import random
import sys

class command_handler:
    def __init__(self, output):
        self.output = output
        self.assistance = {
            "clear": "clears terminal",
            "list": "lists all files in the current working directory",
            "time": "prints elapsed time || requires a flag",
            "$": "  -sesh | session time since bootup",
            "$$": "  -base | local clock time",
            "$$$": "  -acpt | average command processing time (session only)",
            "prdir": "prints full directory path || requires a flag",
            "!": "  -work | working",
            "!!": "  -home | home",
            "chdir": "changes current working directory || requires a path",
            "read": "outputs file contents || requires a file, can also have a flag",
            "^": "  -head | top 'x' lines of a file | requires an accompanying value",
            "^^": "  -tail | bottom 'x' lines of a file | requires an accompanying value",
            "write": "adds content to a file and outputs changes || requires a file, content (string), and a flag",
            "&": "  -appd | adds content to the end of the file (newline)",
            "&&": "  -over | overrides file content to user content",
            "move": "moves a file to a different location || requires a file and a path",
            "copy": "copies a file to a different location || requires a file and a path",
            "delete": "deletes a file || optional flag,",
            "^": "  -perm | permanantly deletes the attached file",
            "data": "prints metadata || requires a file",
            "log": "logs all user input and terminal output (during session) and saves to a file || optional path",
            "history": "prints the run history of a specific command || requires a command (string)"
        }

    def recieve_command(self, raw, cmd): #- converts command name to callable function
        self.parsed_userin = raw
        method = getattr(self, cmd, None)
        method()

    def clear(self):
        self.output.clear()
        return
    
    def list(self):
        self.output.insertPlainText("\n\n")
        for file in os.listdir(os.getcwd()):
            if os.path.isfile(file):
                self.output.insertPlainText(f"{file}   ")
        self.output.insertPlainText("\n")
        return
    
    def help(self):
        self.output.append("")
        self.output.append("<h3 style='margin: 0; padding: 0;'>Command Help</h3>")
        self.output.append("")
        for key, value in self.assistance.items():
            if key.isalnum():
                self.output.append(f"\n<b>{key}</b>: {value}")
            else: #- argument
                self.output.append(f"{value}")
        self.output.append("")
        self.output.append("<h3 style='margin: 0; padding: 0;'>EXAMPLES LOCATED IN THE README</h3>")
        self.output.append("")
        return