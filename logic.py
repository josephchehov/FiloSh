import os
import time

## creates a command logging object every new session that will locally store
## the command info & session number on a text document.

class Logging:
    def __init__(self):
        self.command = ""
        self.timestamp = 0
        self.runtime = 0

## everytime a command is called, it will create a Command object that will have details about it
## this class is also responsible for command processing methods, which includes file searching

class Command:
    def __init__(self):
        self.command = ""
        self.argument = ""

## once the gui class is initialized and created, it will start receiving calls from the default
## shell object 'terminal', which will take inputs from the user, to which the shell will then
## validate it, processing the command in the Command class by creating its own object, then it will
## log it upon successful exit of output. Though I might choose to find a way for the logging class to
## accept command objects since that will make things easier.

class Shell:
    def __init__(self):
        self.home_directory = os.path.expanduser("~")
    def get_current_working_directory(self):
        return os.getcwd()
    def get_home_directory(self):
        return self.home_directory

def get_runtime(start, end):
    elapsed = abs(start - end) * 1000
    if elapsed >= 1000: ## >= 1 second
        return f"{(elapsed/1000):.3f}s"
    else:
        return f"{(elapsed):.3f}ms"
    

terminal = Shell()
userin = ""
while userin != "exit":
    userin = input(f"{terminal.home_directory}~: ")
    start = time.perf_counter()
    if userin == "dir -w": # working directory
        print(f"[---| Run Successful in {get_runtime(start, time.perf_counter())} |---]\nCurrent working directory is: {terminal.get_current_working_directory()}\n[---| Output Finished |---]")
    if userin == "dir -h": # home directory
        print(f"[---| Run Successful in {get_runtime(start, time.perf_counter())} |---]\nHome directory is: {terminal.get_home_directory()}\n[---| Output Finished |---]")