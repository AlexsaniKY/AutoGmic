import subprocess
import argparse
import sys
import os
from pathlib import Path

#print(__file__)     #this file's directory
#print(os.getcwd())  #the directory this file was called from

class GmicLog:
	@staticmethod
	def get_commands():
		commands = []
		with open_log() as f:
			commands = filter_commands(line for line in f)
		return commands
		
	@staticmethod
	def remove_commands(num_commands):
		if num_commands <= 0:
			raise ValueError
		stored_lines = []
		removed_lines = []
		with open_log('r+') as f:
			for l in f:
				if num_commands > 0:
					removed_lines.append(l)
					if is_command(l):
						num_commands -= 1
				else:
					stored_lines.append(l)
			f.seek(0)
			f.write(''.join(stored_lines))
			f.truncate()
		return removed_lines
		
	@staticmethod
	def clear_commands():
		removed_lines = []
		with open_log('r+') as f:
			for l in f:
				removed_lines.append(l)
			f.seek(0)
			f.truncate()
		return removed_lines
		
def log_location():
	if os.name is 'nt':
		return "".join( (os.environ['HOME'], r'\AppData\Roaming\gmic\gmic_qt_log'))

def open_log(mode = 'r'): 
	return open(log_location(), mode)

def filter_commands(input):
	commands = []
	for line in input:
		if is_command(line):
			commands.append(str.split(line)[-2:])
	return commands
	
def is_command(line):
	statements = str.split(line)
	if len(statements)==6:
		if statements[1] == 'Command:' and statements[4][-8:] != '_preview':
			return True
	
def capture(subset = None):
	commands = []
	with open_log() as f:
		commands = filter_commands(line for line in f)
	
	commands_path = "".join((os.getcwd(), r'\commands.txt'))
	with open(commands_path, 'a') as command_file:
		for pair in commands:
			command_file.write(' '.join(pair))
			command_file.write(' ')
			if subset is None:
				command_file.write("*")
			else:
				command_file.write(subset)
			command_file.write('\n')
			
def store_commands(commands, subset = None):

	####
	#BUG: save groups with quotations
	commands_path = "".join((os.getcwd(), r'\commands.txt'))
	with open(commands_path, 'a') as command_file:
		for pair in commands:
			command_file.write(' '.join(pair))
			if not subset:
				command_file.write(' *')
			else:
				for group in subset:
					command_file.write(' ')
					command_file.write(group)
			command_file.write('\n')
			
def set_subsets(subset_dict):
	subsets_registry_path = "".join((os.getcwd(), r'\subset_registry'))
	with open(subsets_registry_path, 'w') as reg_file:
		for sub in subset_dict:
			if sub is not '*':
				reg_file.write(sub)
				reg_file.write('\n')

	for sub,files in subset_dict.items():
		store_subset(sub, files)
		
def store_subset(subset, file_names):
	if subset == '*':
		subset = '_all'
	#store subset filenames
	dir = "".join((os.getcwd(), '\\subsets\\'))
	if not os.path.exists(dir):
		os.makedirs(dir)
	new_subset_path = "".join((dir, subset))
	with open(new_subset_path, 'w+') as subset_file:
		for file in file_names:
			subset_file.write(file)
			subset_file.write("\n")
			
def add_subset(subset, file_names):
	#register subset
	subsets_registry_path = "".join((os.getcwd(), r'\subsets.txt'))
	with open(subsets_registry_path, 'a') as reg_file:
		reg_file.write(subset)
		reg_file.write('\n')
	
	#store subset filenames
	new_subset_path = "".join((os.getcwd(), r'\subsets\\', subset))
	with open(new_subset_path, 'a') as subset_file:
		for file in file_names:
			subset_file.write(file)
			subset_file.write("\n")
			
def walk_input_directory():
	#directories = {}
	sets_dict = {"*": set()}
	#each folder is a key in sets, and its subdirectories are saved in directories
	parent_dir = "".join((os.getcwd(), r'\input'))
	print(parent_dir)
	for path, names, files in os.walk("".join((os.getcwd(), r'\input')), topdown = False):
		#set the folder name to the lowest folder we are searching
		this_folder = os.path.split(path)[-1]
		
		#don't store the parent input folder as a named set
		if path == parent_dir:
			this_folder = "*"
			
		#if there are files in the folder, store them in the set
		if files:		
			#initialize
			if this_folder not in sets_dict:
				sets_dict[this_folder] = set()
			
			for f in files:
				if f == 'Thumbs.db':
					continue
				#save each file by relative path to the parent folder
				f_name = os.path.join(path, f)[len(parent_dir):]
				#add for this folder's set
				sets_dict[this_folder].add(f_name)
				#add to universal set, may be redundant 
				#but won't be costly enough to need to separate the logic
				sets_dict["*"].add(f_name)
				
		#if there are subdirectories, merge their sets into this one
		if names:
			# make sure we have a set to store into
			if this_folder not in sets_dict:
				sets_dict[this_folder] = set()
			#store the subdirectory sets in this set, ignoring empty subdirectories
			for directory in names:
				if directory in sets_dict:
					sets_dict[this_folder].update(sets_dict[directory])
		#if this and all lower subdirectories were empty,
		#don't save the folder's contents
		if not sets_dict[this_folder]:
			del sets_dict[this_folder]

	return sets_dict
	
def command_init(command):
	pass
	
def command_capture(command):
	num = command.n
	groups = command.groups
	coms = GmicLog.get_commands()
	if num:
		coms = coms[:num]
	store_commands(coms, groups)
	if num:
		GmicLog.remove_commands(num)
	else:
		GmicLog.clear_commands()
	print(coms)
	print(groups)
	
def command_inspect(command):
	coms = GmicLog.get_commands()
	for i, c in enumerate(coms, 1):
		print(str(i) + ": " + " ".join(c))

	
def command_flush(command):
	if (not command.num_actions) and (not command.a):
		print("please specify either an amount or the all flag -a")
		return
	if command.num_actions and command.a:
		print("Syntax Error: cannot specify both a value and -a")
		return
	if command.a:
		GmicLog.clear_commands()
	else:
		GmicLog.remove_commands(command.num_actions)
	
	
def command_apply(command):
	#############################
	#TODO read subsets from files
	subset_dict = walk_input_directory()
	
	imageset = set()
	if command.groups:
		for g in command.groups:
			if g in subset_dict:
				imageset.update(subset_dict[g])
			else:
				print("Error: specified group not found: " + g)
				return
	else:
		imageset = subset_dict["*"]
	images = sorted(imageset)
	comms = []
	args = []
	groups = []
	
	cwd = os.getcwd()
	input_folder = "".join((cwd, '\\input'))
	output_folder = "".join((cwd, '\\output'))
	commands_path = "".join((cwd, '\\commands.txt'))
	with open(commands_path, 'r') as command_file:
		for line in command_file:
			if line.rstrip() == "":
				continue
			l = line.split(' ')
			c, a, *g = l
			#strip whitespace (newlines)
			g[-1] = g[-1].rstrip()
			comms.append(c)
			args.append(a)
			groups.append(g)

	statements = []
	for i in images:
		s = ["gmic", "-i", "".join((input_folder, i))]
		for index in range(len(comms)):
			for g in groups[index]:
				if g not in subset_dict:
					print("Group: " + g + " not recognized")
				else:
					if i in subset_dict[g]:
						s.append(comms[index])
						s.append(args[index])
		s.append("-o")
		s.append("".join((output_folder, i)))
		statements.append(s)
		
	for path, _, _ in os.walk(input_folder):
		in_f = path.split(input_folder)[-1]
		out_f = "".join((output_folder, in_f))
		if not os.path.exists(out_f):
			os.makedirs(out_f)
	for s in statements:
		subprocess.call(s, shell = True)

	
	
def command_walk(command):
	set_subsets(walk_input_directory())
	

if __name__ == "__main__":
	#main parser and the parent to allow splitting on the first argument
	cli_parser = argparse.ArgumentParser(description="Allows automatic captured processing of multiple organized images through Gmic's command line interface")
	command_parser = cli_parser.add_subparsers(dest="command")
	commands = {}
	
	#initialize directory
	init_parser    = command_parser.add_parser("init", 
						description = "initialize directory for tracking, capturing, and processing operations on a set of images")
	commands["init"] = command_init
	
	#capture commands
	capture_parser = command_parser.add_parser("capture", 
						description = "captures a series of commands on a set of images")
	capture_parser.add_argument("-n", type = int, 
						help = "the amount of commands to capture. Omit to capture all commands.  Must be entered first to allow maximum flexibility in allowed folder/group names")
	capture_parser.add_argument("groups", nargs = argparse.REMAINDER, 
						help = "list of all groups this is applied to.  Omit to affect all images.")
	commands["capture"] = command_capture
	
	#inspect uncaptured commands
	inspect_parser = command_parser.add_parser("inspect", 
						description = "inspect a series of actions not captured yet from the gmic logfile")
	commands["inspect"] = command_inspect
	
	#flush unneeded commands
	flush_parser   = command_parser.add_parser("flush", 
						description = "flush a series of commands from the gmic logfile")
	flush_parser.add_argument("num_actions", nargs = "?", default = 0, type = int, 
						help = "amount of commands to remove from gmic logfile, starting with the oldest")
	flush_parser.add_argument("-a" , action = "store_true", 
						help = "flush all commands from logfile.  Cannot specify with a given amount simultaneously")
	commands["flush"] = command_flush
	
	#apply commands to image(s)
	apply_parser   = command_parser.add_parser("apply", description = "apply set of commands to one or more images")
	apply_parser.add_argument("groups", nargs = argparse.REMAINDER, help = "groups to apply command chain to")
	commands["apply"] = command_apply
	
	#walk input directory
	walk_parser    = command_parser.add_parser("walk", description = "walk the input directory and set the group names from it")
	commands["walk"] = command_walk
	
	input = cli_parser.parse_args()
	print(input)
	
	commands[input.command](input)


		