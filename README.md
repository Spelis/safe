# SAFE: Slow As F\*\*k Editor

A really stupid text editor with a shell like environment to edit files just as if you're in a real shell. which in turn makes text editing really slow

# running:
* run `python -m venv .venv` to create a virtual environment
* run `source .venv/bin/activate` to activate the virtual environment
* run `pip install -r requirements.txt` to install the required packages
* run `python main.py` to start the editor

# config:
the configuration file for safe can be found at ~/.config/safe.ini

## SHELL:
### Bool: NerdFontIcons:
enables nerd fonts
### Bool: CtrlCQuit:
kinda broken, Use Control+C to quit 
### Bool: CoolPrompt:
uses nerd font icons to create a cool prompt (requires ColorPrompt setting to be true)
### Bool: ColorPrompt:
uses ansi escape codes to put colors in your prompt

## ALIAS:
### String: *any:
sets an alias for a command with the format: alias_name = underlying_command

# changelog

## v.1.0.1:
* edit,insert,cat,clear commands added
* file opening
* shell like split with `shlex`

## v.1.0.2:
* saving, save command
* save status in prompt
* better prompt

## v.1.0.3:
* debug mode, debug command
* delete command
* filename setting, setfilename command
* exit command
* info command
* debug mode exception printing
* added readline module (history, along with other useful things for python inputs)

## v.1.0.4:
* bare-bones scripting support

## v.1.0.5:
* i moved the traceback import
* *\*cricket noises\**

## v.1.0.6:
* planned relative timestamp
* *\*cricket noises\**

## v.1.0.7:
* added config file
* added filesize

## v.1.0.8:
* help command
* relative timestamp added from v.1.0.6
* environment variables, variables
* exit warning if unsaved changes

## v.1.0.9:
* removed help from readme file :)

## v.1.1.0:
* *slight* windows support
* syntax highlighting 🥳🥳🥳
* slight plugin support?
* setfiletype command
* multicommand support (&& to split commands.)

## v.1.1.1:
* better windows support
* command aliases (they didnt work well)
* nerd font support (v.1.0.7 planning)

## v.1.1.2:
* nerd fonts support is kinda also colored prompt as well?

## v.1.1.3:
* ^C (ctrl+c) to quit (config file)
* better command aliases
* random color in nerd font prompt
* prints command when not recognized

## v.1.1.4:
* added ctrl+c config documentation

## v.1.1.5:
* added exec command (os.system)
* made NerdFontIcons setting enable icons only
* added CoolPrompt setting (requires ColorPrompt setting, for cooler prompt with colors)
* added ColorPrompt setting (for colors)
* added license (MIT)
* added filesize in different units
* added "cmd" variable type
* added poetry (a friend recommended it)
* added optional "cat" command index :)

## v.1.1.6:
* added "new" command (yes, "new". it creates a new empty file.)
* added "open" command

## v.1.1.7:
* added "ls" command (lists directory with optional path :) )
* made the ColorPrompt only use colors 1-15 :) (works better with terminal color themes along with pywal and similar)
* fixed cat command??

## v.1.1.8:
* made the help command better
* removed poetry cause its shit
* also this is the first commit in 11 months
* might also stop making commits align with version numbers
