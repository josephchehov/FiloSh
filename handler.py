import os
import time
from datetime import datetime
from pathlib import Path

class command_handler:
    def __init__(self, output, started):
        self.output = output
        #- help
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
            "delete": "deletes a file || optional flag",
            "|": "  -perm | permanantly deletes the attached file",
            "data": "prints metadata || requires a file",
            "log": "logs all user input and terminal output (during session) and saves to a file || optional path",
            "history": "prints the run history of a specific command || requires a command (string)"
        }
        #- time
        self.process_time = []
        self.began_session = started

    def recieve_command(self, raw, cmd): #- converts command name to callable function
        self.start = time.perf_counter()
        self.parsed_userin = raw
        method = getattr(self, cmd, None)
        method()

    def clear(self):
        self.output.clear()
        self.process_time.append(time.perf_counter() - self.start)
        return
    
    def list(self):
        self.output.append("\n")
        for file in os.listdir(os.getcwd()):
            if os.path.isfile(file):
                self.output.insertPlainText(f"{file}   ")
        self.output.append("")
        self.process_time.append(time.perf_counter() - self.start)
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
        self.process_time.append(time.perf_counter() - self.start)
        return
    
    def prdir(self):
        self.output.append("")
        if self.parsed_userin["flag"] == "-home":
            self.output.append(f"<b>Home directory</b>: '{str(Path.home())}'")
        else:
            self.output.append(f"<b>Current working directory</b>: '{os.getcwd()}'")
        self.output.append("")
        self.process_time.append(time.perf_counter() - self.start)
        return

    def chdir(self):
        self.output.append("")
        os.chdir(self.parsed_userin["path"])
        self.output.append(f"<b>Current working directory has changed to</b>: '{os.getcwd()}'")
        self.output.append("")
        self.process_time.append(time.perf_counter() - self.start)
        return
    
    def time(self):
        self.output.append("")
        average = 0
        def format(elapsed):
            if elapsed >= 3600:
                h = int(elapsed // 3600)
                m = int((elapsed % 3600) // 60)
                s = int(elapsed % 60)
                return f"{h}h {m}m {s}s"
            elif elapsed >= 60:
                m = int(elapsed // 60)
                s = int(elapsed % 60)
                return f"{m}m {s}s"
            elif elapsed >= 1:
                if self.parsed_userin["flag"] != "-acpt":
                    return f"{int(elapsed)}s"
                return f"{elapsed:.2f}s"
            elif elapsed >= 0.001:
                ms = elapsed * 1000
                return f"{ms:.2f}ms"
            elif elapsed >= 0.000001:
                us = elapsed * 1000000
                return f"{us:.2f}µ"
            else:
                ns = elapsed * 1000000000
                return f"{ns:.2f}ns"
        if self.parsed_userin["flag"] == "-acpt":
            for cmdtime in self.process_time:
                average += cmdtime
            if len(self.process_time) == 0:
                average = average
            else:
                average = average / len(self.process_time)
            self.output.append(f"<b>Average command processing time is</b>: {format(average)}")
            self.output.append(f"<b>Total commands run in session</b>: {len(self.process_time)}")
        elif self.parsed_userin["flag"] == "-sesh":
            self.output.append(f"<b>Session started</b>: {format(time.perf_counter() - self.began_session)} ago")
        else:
            current = datetime.now()
            self.output.append(f"<b>Current time</b>: {current.strftime('%H:%M:%S')} | {current.strftime('%I:%M:%S %p')}")
        self.output.append("")
        self.process_time.append(time.perf_counter() - self.start)
        return
    
    def read(self):
        self.output.append("")
        with open(self.parsed_userin["file"], 'r') as f:
            lines = f.readlines()
        if len(self.parsed_userin) > 2:
            if self.parsed_userin["flag"] == "-head":
                lines = lines[:int(self.parsed_userin["value"])]
            else:
                lines = lines[-int(self.parsed_userin["value"]):]
        for line in lines:
            self.output.append(line.strip())
        self.output.append("")
        return