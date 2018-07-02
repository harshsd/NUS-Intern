#Codes for reading and writing signals and entropies for better usage

def read_file(file_name):
	'''Reads a file as an array and returns it.
	Args:
	file_name: Name of file. change Directory by os.chdir() if not in same directory
	Returns:
	Vector with values as in file'''

	f = open(file_name , 'r')
	vec = []
	for line in f:
		for word in line.split():
			vec.append(float(word))
	f.close()
	return vec


def write_to_file(file_name,vector_output):
	'''Writes a vector to a file with each value on a new line.
	Args:
	file_name: Name of file. change Directory by os.chdir() if not in same directory
	vector_output: The vector to be written to the file'''
	
	file = open (file_name,'a+')
	M = len(vector_output)
	for i in range (0,M):
		file.write(str(vector_output[i]))
		file.write('\n')
	file.close()    