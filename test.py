import sys
from convertor import Convertor

input_file_path = sys.argv[1]

if not input_file_path:
	print('please provide input file path.')
	sys.exit()

convertor = Convertor(input_file_path)
convertor.encode()
# convertor.decode()
