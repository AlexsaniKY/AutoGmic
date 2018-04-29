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
			
	# subsets_path = "".join((os.getcwd(), r'\subsets.txt'))
	# with open(subsets_path, 'a'):
		# if(subset is None):
		

if __name__ == "__main__":
	#subprocess.call(["gmic","x_shadebobs"])
	if 'capture' in sys.argv:
		capture()
		