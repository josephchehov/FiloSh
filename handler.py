import os
import time
import shutil
from datetime import datetime, date
from pathlib import Path
from send2trash import send2trash

class command_handler:
    def __init__(self, output, started, bootup):
        self.output = output
        self.bootup = bootup
        self.logs = []
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
            "log": "logs all user input during session and saves as a file located in the current working directory unless otherwise specified || optional path",
            "history": "prints the run history of a specific command || requires a command (string)"
        }
        self.process_time = []
        self.began_session = started

    def recieve_command(self, raw, cmd, userin): #- converts command name to callable function
        raw_userin = userin
        self.start = time.perf_counter()
        self.parsed_userin = raw

        method = getattr(self, cmd, None)
        method()

        self.logs.append([raw_userin, datetime.now().strftime('%H:%M:%S')])

    def format_size(self, size):
            for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                if size <= 1024.0:
                    return "%3.1f %s" % (size, x)
                size /= 1024.0

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
        self.process_time.append(time.perf_counter() - self.start)
        return
    
    def write(self):
        self.output.append("")
        def calculate_file_size():
            fp = open(self.parsed_userin["file"], 'r') # calculating file size
            old_position = fp.tell()
            fp.seek(0, 2)
            size = fp.tell()
            fp.seek(old_position, 0)
            return size
        
        old = calculate_file_size()

        if self.parsed_userin["flag"] == "-over":
            with open(self.parsed_userin["file"], 'w') as f:
                f.truncate(0)
                f.write(self.parsed_userin["string"])
                self.output.append(f"<b>File contents overridden to</b>:")
                self.output.append(f"\n'{self.parsed_userin["string"]}'\n")
        else:
            with open(self.parsed_userin["file"], 'a+') as f:
                f.seek(0, 2)
                if f.tell() > 0: #- check newline
                    f.seek(f.tell()-1)
                    lchar = f.read(1)
                    if lchar != "\n":
                        f.write("\n")
                self.output.append(f"<b>Appended contents</b>:")
                self.output.append(f"\n'{self.parsed_userin["string"]}'\n")
                f.write(self.parsed_userin["string"] + '\n')

        difference = self.format_size(calculate_file_size() - old)
        if calculate_file_size() - old >= 0:
            difference = f'+{difference}'
        self.output.append(f"<b>{difference}</b>")
        self.output.append("")
        self.process_time.append(time.perf_counter() - self.start)
        return
    
    def copy(self):
        self.output.append("")
        try:
            shutil.copy(os.path.abspath(self.parsed_userin["file"]), self.parsed_userin["path"])
            self.output.append(f"File has been successfully copied to: {self.parsed_userin["path"]}\n")
            self.output.append(f"<b>Metadata and permissions preserved</b>")
            self.output.append("")
        except:
            self.output.append(f"A file with that name already exists within: {self.parsed_userin["path"]}")
        
        self.process_time.append(time.perf_counter() - self.start)
        return
    
    def move(self):
        self.output.append("")
        try:
            shutil.move(os.path.abspath(self.parsed_userin["file"]), self.parsed_userin["path"])
            self.output.append(f"File has been successfully copied to: {self.parsed_userin["path"]}\n")
        except:
            self.output.append(f"A file with that name already exists within: {self.parsed_userin["path"]}")
        
        self.process_time.append(time.perf_counter() - self.start)
        return
    
    def delete(self):
        self.output.append("")
        if len(self.parsed_userin) > 2:
            os.remove(self.parsed_userin["file"])
            self.output.append(f"'{self.parsed_userin["file"]}' has been permanantly deleted\n")
        else:
            send2trash(self.parsed_userin["file"])
            self.output.append(f"'{self.parsed_userin["file"]}' has been moved to the recycling bin\n")
        
        self.process_time.append(time.perf_counter() - self.start)
        return

    def log(self):
        now = datetime.now()
        fpath = f"filosh_{now.strftime('%Y-%m-%d_%H-%M-%S')}.log"
        self.output.append("")

        with open(fpath, 'a') as f:
            for process in self.logs:
                f.write(f"'{process[0]}'|{process[1]}\n")

        self.output.append(f"<b>Log file created</b>: '{fpath}'")
        self.output.append("")

        if len(self.parsed_userin) > 1:
            shutil.move(fpath, self.parsed_userin["path"])
            self.output.append(f"<b>Located</b>: '{self.parsed_userin["path"]}'")
        else:
            self.output.append(f"<b>Located</b>: '{os.getcwd()}'")

        self.output.append("")
        return
    
    def data(self):
        stats = os.stat(self.parsed_userin["file"])
        self.output.append("")

        metadata = {
            "size": self.format_size(stats.st_size),
            "created": datetime.fromtimestamp(stats.st_birthtime).strftime('%Y-%m-%d | %H:%M:%S'),
            "modified": datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d | %H:%M:%S'),
            "accessed": datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d | %H:%M:%S'),
            "path": os.path.abspath(self.parsed_userin["file"]),
            "extention": os.path.splitext(self.parsed_userin["file"])[1] or "none",
            "type": "file" if os.path.isfile(self.parsed_userin["file"]) else "directory",
            "permissions": f"read: {os.access(self.parsed_userin["file"], os.R_OK)} | write: {os.access(self.parsed_userin["file"], os.W_OK)} | execute: {os.access(self.parsed_userin["file"], os.X_OK)}"
        }

        for key, item in metadata.items():
            self.output.append(f"<b>{key}</b>: {item}")

        self.output.append("")
        self.process_time.append(time.perf_counter() - self.start)
        return
    
    def history(self):
        self.output.append("")
        inc = 1

        for log in self.logs:
            try:
                if log[0].index(self.parsed_userin["command"]) == 0:
                    self.output.append(f"<b>[{inc}]</b> '{log[0]}' | {log[1]}")
                    inc += 1
            except:
                continue

        if inc-1 == 0:
            self.output.append(f"No history of successfully running '{self.parsed_userin["command"]}' this session")
        else:
            self.output.append("")
            self.output.append(f"'{self.parsed_userin["command"]}' has been run a total of <b>{inc-1}</b> times this session")
        
        self.output.append("")
        self.process_time.append(time.perf_counter() - self.start)
        return