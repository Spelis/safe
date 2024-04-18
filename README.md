# SAFE: Slow As F\*\*k Editor

A really stupid text editor with a shell like environment to edit files just as if you're in a real shell. which in turn makes text editing really slow or really fast depending on what you use it for, but will be slow to use most of the time

### added syntax highlighting!!! 🥳🥳🥳
---
syntax highlighting was surprisingly easy to add thanks to Pygments!

# requirements:
## Pygments:
`pip install pygments`

## readline:
### windows:
___
`pip install pyreadline`
### linux (and maybe macos):
___
`pip install readline`

# config:
the configuration file for safe can be found at ~/.config/safe.ini

## SHELL:
### Bool: NerdFontIcons:
enables a different promp along with nerd fonts :)
### Bool: CtrlCQuit:
kinda broken, Use Control+C to quit 

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
