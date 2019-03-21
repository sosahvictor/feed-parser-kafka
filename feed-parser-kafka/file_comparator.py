import difflib
import os
import re

def find_files(target_directory):
	files = os.listdir(target_directory)
	filtered_files = {}

	for target_file in files:
		suffix_index = target_file.rfind("_")
		filename = target_file[:suffix_index]
		files_list = []

		if filename in filtered_files:
			files_list = filtered_files[filename]

		files_list.append(target_directory + target_file);
		filtered_files[filename] = files_list

	return filtered_files

def diff_files(files):
	files_with_diff = []
	for target_file in files:
		list_of_files = files[target_file]
		list_of_files.sort()

		if len(list_of_files) > 1:
			file1 = open(list_of_files[0], "r").read().strip().splitlines()
			file2 = open(list_of_files[1], "r").read().strip().splitlines()

			diff_lines = difflib.unified_diff(file1, file2,fromfile=list_of_files[0], tofile=list_of_files[1], n=0)
			for line in diff_lines:
				for prefix in ('---', '+++', '@@'):
					if line.startswith(prefix):
						break
					elif list_of_files[1] not in files_with_diff:
						files_with_diff.append(list_of_files[1])

			print("Deleting old file " + list_of_files[0])
			os.remove(list_of_files[0])
		else:
			files_with_diff.append(list_of_files[0])

	print("Files with new feeds: ", files_with_diff)
	return files_with_diff

def exec_find_files(target_directory):
	files = find_files(target_directory)
	return diff_files(files)
