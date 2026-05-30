# FiloSh
Python3-based file management shell


## Commands
Reference guide for up to date command info and examples
*ver 1.0*

>
> *flag* ~ a parameter used to specify settings for a command. It uses a dash ('-') followed by an 4-letter abbreviation for its action, (ex. -abbv)
>
> *file* ~ a simplified form of a path classifier just for files (local) based on its name and extention, (ex. example.txt)
>
> *path* ~ the exact location of a file or directory within the computers file system, (ex. c:\Users\Name\Desktop\Directory1)
>
> *command* ~ the full name of a command, (ex. help)
>
> *string* ~ string input that encapsulated between double quotations, (ex. "this is string input")
>
> *value* a positive integer, (ex. 1) 

**help** - outputs information on all commands, including their arguments (if they have any)

**clear** - clears the terminal

**prdir** - outputs the specified directory | requires 1 of 2 arguments of type ***flag***
- *-home* home
- *-work* working
```
c:\Users\Name\Desktop\Filosh$: prdir -home

Home Directory: 'c:\Users\Name'
```

**chdir** - changes the current working directory to the specified path | requires 1 argument of type ***path***
```
c:\Users\Name\Desktop\Filosh$: chdir c:\Users\Name\Desktop

Current working directory has changed to: 'c:\Users\Name\Desktop
```

**list** - lists all files in the <u>current</u> working directory
```
c:\Users\Name\Desktop\Filosh$: list

example.txt  desktop.ini  file.lnk  file2.lnk
```

**read** - outputs all contents in a file unless specified | requires 1 argument of type ***file*** & allows 1 of 2 option arguments of type ***flag*** paired with a ***value***
- '-head #' ~ the first # lines of a file
- '-tail #' ~ the last # lines of a file
```
c:\Users\Name\Desktop\Filosh$: read example.txt -head 3

this is line 1!
this is line 2!
this is line 3!
```
> ##### 'example.txt' contents
>
> this is line 1!
>
> this is line 2!
>
> this is line 3!
>
> this is line 4!

**write** - applies string input to a file & outputs file & size change | requires 1 argument of type ***file***, 1 argument of type ***string*** & 1 of 2 arguments of type ***flag***
- '-appd' ~ appends string input to a newline at the end of the file
- '-over' ~ overrides the file contents to string input only
```
c:\Users\Name\Desktop\Filosh$: write example.txt "file overriden"

File contents overriden to:

'file overriden'
- 56.0 bytes
```
> ##### 'example.txt' contents
> file overriden

------ OTHER COMMANDS IN PROGRESS ------
