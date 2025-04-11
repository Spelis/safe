# SAFE: Slow As F\*\*k Editor

A really stupid text editor with a shell like environment to edit files just as if you're in a real shell. which in turn makes text editing really slow

# running:
* run `python -m venv .venv` to create a virtual environment
* run `source .venv/bin/activate` to activate the virtual environment
* run `pip install -r requirements.txt` to install the required packages
* run `python main.py` to start the editor

# changelog

## v2.0.0 - Big update and rewrite
* rewritten mostly from scratch.
* actually extensible
* multiple buffers!
* and more idk i got hyper focused and didnt pay attention to what i added

## v2.0.1 - Small update
* formatted stuff with `black` and `isort`
* fixed some stuff that wasnt working, like the cat command and save command.

## v2.0.2 - Small update (autocomplete update)
* more formatting
* added custom auto complete
* made cat command show all lines (before it stripped any empty lines after the last line with content)
* made the program not immediately throw an error on older versions of python. tested on py3.9.21

## v2.1.0 - Pretty big update (plugin update)
* Added back scripts (they're pretty useless not gonna lie)

    1. make file and start editing (maybe in safe ;) )
    2. put commands in like you would in the interactive editor
    3. run safe with the -s or --script attribute along with all the scripts you want to run
    4. enjoy

* Enhanced plugin support
* Added example plugins: Kanban and a template
* `ls` command (woah, revolutionary!)

## v2.1.1 - Small update (cd command and calculator module)
* NOTE: Calculator module is coming soon.
* moved ls to defmod/shell.py
* added cd command (might be a little broken hehe)

# legacy changelog

## v1.0.1:
* edit,insert,cat,clear commands added
* file opening
* shell like split with `shlex`

## v1.0.2:
* saving, save command
* save status in prompt
* better prompt

## v1.0.3:
* debug mode, debug command
* delete command
* filename setting, setfilename command
* exit command
* info command
* debug mode exception printing
* added readline module (history, along with other useful things for python inputs)

## v1.0.4:
* bare-bones scripting support

## v1.0.5:
* i moved the traceback import
* *\*cricket noises\**

## v1.0.6:
* planned relative timestamp
* *\*cricket noises\**

## v1.0.7:
* added config file
* added filesize

## v1.0.8:
* help command
* relative timestamp added from v1.0.6
* environment variables, variables
* exit warning if unsaved changes

## v1.0.9:
* removed help from readme file :)

## v1.1.0:
* *slight* windows support
* syntax highlighting 🥳🥳🥳
* slight plugin support?
* setfiletype command
* multicommand support (&& to split commands.)

## v1.1.1:
* better windows support
* command aliases (they didnt work well)
* nerd font support (v1.0.7 planning)

## v1.1.2:
* nerd fonts support is kinda also colored prompt as well?

## v1.1.3:
* ^C (ctrl+c) to quit (config file)
* better command aliases
* random color in nerd font prompt
* prints command when not recognized

## v1.1.4:
* added ctrl+c config documentation

## v1.1.5:
* added exec command (os.system)
* made NerdFontIcons setting enable icons only
* added CoolPrompt setting (requires ColorPrompt setting, for cooler prompt with colors)
* added ColorPrompt setting (for colors)
* added license (MIT)
* added filesize in different units
* added "cmd" variable type
* added poetry (a friend recommended it)
* added optional "cat" command index :)

## v1.1.6:
* added "new" command (yes, "new". it creates a new empty file.)
* added "open" command

## v1.1.7:
* added "ls" command (lists directory with optional path :) )
* made the ColorPrompt only use colors 1-15 :) (works better with terminal color themes along with pywal and similar)
* fixed cat command??

## v1.1.8:
* made the help command better
* removed poetry cause its shit
* also this is the first commit in 11 months
* might also stop making commits align with version numbers
