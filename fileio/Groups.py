import os

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