# FiloSh
Python3-based file management shell


## Commands
Reference guide for up to date command info and examples
*ver 1.0*

##### Argument classifiers
>
> **flag** -- parameter used to specify settings for a command. It uses a dash ('-') followed by an 4-letter abbreviation for its action, (ex. -abbv)
>
> **file** -- a simplified form of a path classifier just for files (local) based on its name and extention, (ex. example.txt)
>
> **path** -- the exact location of a file or directory within the computers file system, (ex. c:\Users\Name\Desktop\Directory1)
>
> **command** -- the full name of a command, (ex. help)
>
> **string** -- string input that encapsulated between double quotations, (ex. "this is string input")
>
> **value** -- a positive integer, (ex. 1)

<br>

'**help**' - outputs information on all commands and their compatible flags (if they have any)

'**clear**' - clears the terminal

'**time**' - outputs elapsed time | requires 1 of 3 arguments of type ***flag***
- *-sesh* ~ session (since terminal booted up)
- *-base* ~ local time
- *-acpt* ~ average command processing time
```
c:\Users\Name\Desktop\Filosh$: time -sesh

Session started: 1m 2s ago
```
<br>

'**log**' - saves successfully run command logs (in this session) to a new file in the current directory unless otherwise specified | allows 1 optional argument of type ***path***
```
c:\Users\Name\Desktop\Filosh$: log c:\Users\Name\Desktop\Logs

Log file saved at: 'c:\Users\Name\Desktop\Logs'
```
<br>

'**prdir**' - outputs the specified directory | requires 1 of 2 arguments of type ***flag***
- *-home* ~ home
- *-work* ~ working
```
c:\Users\Name\Desktop\Filosh$: prdir -home

Home Directory: 'c:\Users\Name'
```
<br>

'**chdir**' - changes the current working directory to the specified path | requires 1 argument of type ***path***
```
c:\Users\Name\Desktop\Filosh$: chdir c:\Users\Name\Desktop

Current working directory has changed to: 'c:\Users\Name\Desktop
```
<br>

'**list**' - lists all files in the <u>current</u> working directory
```
c:\Users\Name\Desktop\Filosh$: list

example.txt  desktop.ini  file.lnk  file2.lnk
```
<br>

'**read**' - outputs all contents in a file unless specified | requires 1 argument of type ***file*** & allows 1 of 2 optional arguments of type ***flag*** paired with a ***value***
- *-head #* ~ the first # lines of a file
- *-tail #* ~ the last # lines of a file
```
c:\Users\Name\Desktop\Filosh$: read example.txt -head 3

this is line 1!
this is line 2!
this is line 3!
```
> ##### example.txt
>
> this is line 1! <br>
> this is line 2! <br>
> this is line 3! <br>
> this is line 4! <br>

<br>

'**write**' - applies string input to a file & outputs file & size change | requires 1 argument of type ***file***, 1 argument of type ***string*** & 1 of 2 arguments of type ***flag***
- *-appd* ~ appends string input to a newline at the end of the file
- *-over* ~ overrides the file contents to string input only
```
c:\Users\Name\Desktop\Filosh$: write example.txt "file overriden"

File contents overriden to:

'file overriden'
-56.0 bytes
```
> ##### example.txt
> file overriden

<br>

------ OTHER COMMANDS IN PROGRESS ------
