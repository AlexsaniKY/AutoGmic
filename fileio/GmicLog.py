class GmicLog:
	@staticmethod
	def get_commands():
		with GmicLog.open() as f:
			commands = GmicLog.filter_commands(line for line in f)
			return commands
		
	@staticmethod
	def remove_commands(num_commands):
		if num_commands <= 0:
			raise ValueError
		stored_lines = []
		removed_lines = []
		with GmicLog.open('r+') as f:
			for l in f:
				if num_commands > 0:
					removed_lines.append(l)
					if GmicLog.is_command(l):
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
		with GmicLog.open('r+') as f:
			for l in f:
				removed_lines.append(l)
			f.seek(0)
			f.truncate()
		return removed_lines
	
	@staticmethod
	def location():
		if os.name is 'nt':
			return "".join( (os.environ['HOME'], r'\AppData\Roaming\gmic\gmic_qt_log'))
	
	@staticmethod
	def open(mode = 'r'): 
		return open(GmicLog.location(), mode)

	@staticmethod
	def filter_commands(input):
		commands = []
		for line in input:
			if GmicLog.is_command(line):
				commands.append(str.split(line)[-2:])
		return commands
	
	@staticmethod
	def is_command(line):
		statements = str.split(line)
		if len(statements)==6:
			if statements[1] == 'Command:' and statements[4][-8:] != '_preview':
				return True