import subprocess
import argparse
import sys
import os


import CLI

#print(__file__)     #this file's directory
#print(os.getcwd())  #the directory this file was called from

def main(args = None):
	#main parser and the parent to allow splitting on the first argument
	cli_parser = argparse.ArgumentParser(description="Allows automatic captured processing of multiple organized images through Gmic's command line interface")
	command_parser = cli_parser.add_subparsers(dest="command")
	commands = {}
	
	#initialize directory
	init_parser    = command_parser.add_parser("init", 
						description = "initialize directory for tracking, capturing, and processing operations on a set of images")
	commands["init"] = CLI.init
	
	#capture commands
	capture_parser = command_parser.add_parser("capture", 
						description = "captures a series of commands on a set of images")
	capture_parser.add_argument("-n", type = int, 
						help = "the amount of commands to capture. Omit to capture all commands.  Must be entered first to allow maximum flexibility in allowed folder/group names")
	capture_parser.add_argument("groups", nargs = argparse.REMAINDER, 
						help = "list of all groups this is applied to.  Omit to affect all images.")
	commands["capture"] = CLI.capture
	
	#inspect uncaptured commands
	inspect_parser = command_parser.add_parser("inspect", 
						description = "inspect a series of actions not captured yet from the gmic logfile")
	commands["inspect"] = CLI.inspect
	
	#flush unneeded commands
	flush_parser   = command_parser.add_parser("flush", 
						description = "flush a series of commands from the gmic logfile")
	flush_parser.add_argument("num_actions", nargs = "?", default = 0, type = int, 
						help = "amount of commands to remove from gmic logfile, starting with the oldest")
	flush_parser.add_argument("-a" , action = "store_true", 
						help = "flush all commands from logfile.  Cannot specify with a given amount simultaneously")
	commands["flush"] = CLI.flush
	
	#apply commands to image(s)
	apply_parser   = command_parser.add_parser("apply", description = "apply set of commands to one or more images")
	apply_parser.add_argument("-f", "-filename",
						help = "specifies file name, if -n is applied, this is the file to start from")
						
	## should these be an exlusive group? ##
	## should the user choose if specifying an image that has to be searched for? ##
	
	apply_parser.add_argument("-n", "-num_images", type=int, 
						help = "number of images to apply, in order alphabetically, including the path to file")
	apply_parser.add_argument("-a", "-all", action = "store_true", 
						help = "applies to all images in directory")
	apply_parser.add_argument("groups", nargs = argparse.REMAINDER, 
						help = "groups to apply command chain to")
	commands["apply"] = CLI.apply
	
	#walk input directory
	walk_parser    = command_parser.add_parser("walk", description = "walk the input directory and set the group names from it")
	commands["walk"] = CLI.walk
	
	if args:
		input = cli_parser.parse_args(args)
	else:
		input = cli_parser.parse_args()
	print(input)
	
	commands[input.command](input)
	
if __name__ == "__main__":
	main()


		