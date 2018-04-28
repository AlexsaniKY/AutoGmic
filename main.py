import subprocess, os

print(__file__)#this file's directory
print(os.getcwd())#the directory this file was called from

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

if __name__ == "__main__":
	#subprocess.call(["gmic","x_shadebobs"])
	commands = []
	with open_log() as f:
		print(filter_commands(line for line in f))
