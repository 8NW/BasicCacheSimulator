import argparse, re, random, math

parser = argparse.ArgumentParser(description='A cache simulator')

parser.add_argument('input_file', nargs=1, help='the file that contains the memory trace')
parser.add_argument('cache_lines', nargs=1, help='the number of lines the cache')



args = parser.parse_args()

cache_lines = int(args.cache_lines[0])
input_file = args.input_file[0]

cache = {}

if math.log(cache_lines, 2) != int(math.log(cache_lines, 2)):
	raise ValueError('Cache lines is not a power of two')

line_bits = int(math.log(cache_lines))
offset_bits = 2
tag_bits = line_bits - offset_bits

total_refs = 0
misses = 0

with open(input_file) as f:
	input_data = f.read()
	input_lines = input_data.split('\n')

	for input_line in input_lines:

		input_line = input_line.lstrip()
		input_parts = re.compile('+').split(input_line)
		#print input_parts
		address_type = input_parts[0]
		input_parts = input_parts[1].split(',')

		address = input_parts[0]
		address_size = input_parts[1]
		
		address_bits = "{:032b}".format(int(address, 16))
		tag = address_bits[:tag_bits]
		line = address_bits[tag_bits:-offset_bits]

		cache_line = cache.get(line, None)

		if not cache_line:
			misses += 1
			cache[line] = {}
			cache['tag'] = tag
			cache_line['count'] = 1

		else: 
			if tag == cache[line]['tag']:
				cache[line]['count'] += 1
			else:
				misses += 1
				cache[line]['tag'] = tag
				cache[line]['count'] = 1

		total_refs += 1
			

	print 'Miss rate was: ' + str(misses*100.0/total_refs) + '% out of ' + str(total_refs) + ' references.'




	