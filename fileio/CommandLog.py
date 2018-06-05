import os

command_location = "".join((os.getcwd(), r'\commands.txt'))



def store(commands, subset = None):

	####
	#BUG: save groups with quotations

	with open(command_location, 'a') as command_file:
		for pair in commands:
			command_file.write(' '.join(pair))
			if not subset:
				command_file.write(' *')
			else:
				for group in subset:
					command_file.write(' ')
					command_file.write(group)
			command_file.write('\n')