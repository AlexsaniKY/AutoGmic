import subprocess
import sys
import os
from pathlib import Path

#print(__file__)     #this file's directory
#print(os.getcwd())  #the directory this file was called from

def open_log(): 
	if os.name is 'nt':
		gmic_log = "".join( (os.environ['HOME'], r'\AppData\Roaming\gmic\gmic_qt_log'))
	return open(gmic_log, 'r')

def filter_commands(input):
	commands = []
	for line in input:
		statements = str.split(line)
		if len(statements)==6:
			if statements[1] == 'Command:' and statements[4][-8:] != '_preview':
				commands.append(statements[-2:])
	return commands
	
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
	directories = {}
	sets = {}
	#each folder is a key in sets, and its subdirectories are saved in directories
	for path, names, files in os.walk("".join((os.getcwd(), r'\input'))):
		this_folder = path.split("\\")[-1]
		if names:
			directories[this_folder] = names
		sets[this_folder] = files
	#NEEDS TO ITERATE BACKWARDS
	for parent, subfolders in directories.items():
		sets[parent].extend(sets[subfolders])
	print(directories)
	print(sets)

if __name__ == "__main__":
	#subprocess.call(["gmic","x_shadebobs"])
	if 'capture' in sys.argv:
		capture()
	else:
		walk_input_directory()
		