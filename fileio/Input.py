import os

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