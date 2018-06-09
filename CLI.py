from fileio import Groups
from fileio import GmicLog
from fileio import Input

from glob import glob
from collections import deque


def init(command):
	pass
	

def capture(command):
	num = command.n
	groups = command.groups
	coms = GmicLog.get_commands()
	if num:
		coms = coms[:num]
	CommandLog.store(coms, groups)
	if num:
		GmicLog.remove_commands(num)
	else:
		GmicLog.clear_commands()
	print(coms)
	print(groups)
	

def inspect(command):
	coms = GmicLog.get_commands()
	if not coms:
		print("No commands to inspect.")
		return
	for i, c in enumerate(coms, 1):
		print(str(i) + ": " + " ".join(c))


def flush(command):
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
	

def apply(command):

	# build imageset based on groups supplied
	# position start based on supplied filename
	# truncate if rolling not allowed, rotate if rolling
	# truncate if maximum number is supplied
	#
	# get commands, groups from command file
	# 
	if not (command.f or command.a or command.n):
		print("must specify filename, n quantity or all flag")
		return

	#############################
	#TODO read subsets from files
	subset_dict = walk_input_directory()
	cwd = os.getcwd()
	input_folder = "".join((cwd, '\\input'))
	output_folder = "".join((cwd, '\\output'))
	commands_path = "".join((cwd, '\\commands.txt'))
	
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
		
	##TODO##
	#restructure this logic
	########
	if command.f:
		file = ""
		if not os.path.isfile(input_folder + command.f):
			f_candidates = glob("".join((input_folder, "\\**\\", command.f)), recursive= True)
			print(f_candidates)
			if f_candidates:
				file = f_candidates[0][len(input_folder):]
				if len(f_candidates)>1:
					print("selected " + f_candidates[0][len(input_folder):])
			else:
				print("could not find file specified")
				return
		else:
			file = command.f
			
	if file: 
		if not command.n:
			#if file is specified but not n, only process one file
			images = [file]
		else:
			#file and n are both specified, start at file through n images
			images = sorted(imageset)
			if file in images:
				index = images.index(file)
				images = deque(images)
				images.rotate(-index)
			else:
				print("could not find file specified")
				return	
	else:
		images = sorted(imageset)
	
	comms = []
	args = []
	groups = []
	
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

	for index, s in enumerate(statements):
		if index == command.n:
			return
		subprocess.call(s, shell = True)


def walk(command):
	Groups.set_subsets(Input.walk_input_directory())
