import subprocess, os

print(__file__)#this file's directory
print(os.getcwd())#the directory this file was called from

def open_log(): pass

def filter_commands(input):
	commands = []
	for line in input:
		statements = str.split(line)
		if len(statements)==6:
			if statements[1] == 'Command:' and statements[4][-8:] != '_preview':
				commands.append(statements[-2:])
	return commands

if __name__ == "__main__":
	#subprocess.call(["gmic","x_shadebobs"])
	if os.name is 'nt':
		gmic_log = "".join( (os.environ['HOME'], r'\AppData\Roaming\gmic\gmic_qt_log')) 
	print(gmic_log)
	commands = []
	with open(gmic_log, 'r') as f:
		print(filter_commands(line for line in f))
			# statements = str.split(line)
			# if len(statements)==6:
				# if statements[1] == 'Command:' and statements[4][-8:] != '_preview':
					# print(statements[-2:])
	pass