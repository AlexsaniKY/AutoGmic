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

	for k, v in sets_dict.items():
		print(k + ": ")
		for i in sorted(v):
			print("\t" + i)

if __name__ == "__main__":
	#subprocess.call(["gmic","x_shadebobs"])
	if 'capture' in sys.argv:
		capture()
	else:
		walk_input_directory()
		