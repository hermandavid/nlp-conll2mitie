#!/usr/bin/env python
# Simple utility to translate data from ConLL to format acceptable for MITIE

import os, os.path, argparse

from itertools import groupby

def _check_args(parser):
	''' Check correction of parsed arguments, raise error when inconsistency detected
		Args:
			parser(ArgumentParser): Instance of argument parser

		Return:
			parser.parse_args()
	'''
	# Parse arguments
	parsed_args = parser.parse_args();

	# Check if input data exists and is accessible for read
	source_data_path = parsed_args.source_data
	if not os.path.isfile(source_data_path) or not os.access(source_data_path, os.R_OK):
		parser.error("SOURCE_DATA must be readable file")

	# Return data when correct
	return parsed_args

def _parse_args():
	''' Parse arguments and call routines for crrection checking
		Return:
			_check_args()
	'''
	parser = argparse.ArgumentParser()

	# Argument for input file
	parser.add_argument('-s', required=True, action='store',
			dest='source_data', help='Input file containing data in ConLL format')

	# Return result of parser if correct
	return _check_args(parser);

def parse_conll_sentences(source_data_path):
	''' Read source_data and try to parse ConLL
		Args:
			source_data_path(str): Path to source_data file

		Return:
			ConLL lines grouped by sentence
	'''

	# Read lines into memory and strip heading and tailing whitechars
	with open(source_data_path, 'r') as s_fo:
		source_data_read = s_fo.readlines()
		source_data_read = [ l.strip() for l in source_data_read ]

	# Group sentences together
	source_data_sentences = []
	for key, group in groupby(source_data_read, lambda x: x != ''):
		if key: source_data_sentences.append(list(group))

	return source_data_sentences

def conll_to_mitie(source_data_sentences):
	''' Transform ConLL data format to format acceptable for MITIE, parser expects to have token
		on first position while NER tag on the last position
			Args:
				source_data_sentences(list): List of ConLL lines grouped by sentence

			Return:
				Format acceptable for MITIE
	'''

	mitie_sentences = []
	for s in source_data_sentences:
		conll_lines = [ _s.split('\t') for _s in s ]

		# Serialize data for MITIE
		sentence = { 'tags': [] }; sentence['tokens'] = [ l[0] for l in conll_lines]

		# Get named entities indexes
		tag_start = -1; tag_end = -1
		for index, conll_line in enumerate(conll_lines):
			conll_tag_entry = conll_line[-1]

			# We want only tagged entities
			if conll_tag_entry != 'O':
				conll_tag_entry_split = conll_tag_entry.split('-')
				conll_tag_entry_start = conll_tag_entry_split[0]

				if conll_tag_entry_start == 'B':
					# Save tag when found
					if tag_start >= 0 and tag_end >= 0:
						found_tag = { 'start': tag_start,
							'end': tag_end, 'name': conll_tag_entry_split[-1] }

						sentence['tags'].append(found_tag)

						# Reset tag range
						tag_start = -1; tag_end = -1
					else:
						# Save tag start when found new tag
						tag_start = index; tag_end = tag_start + 1
				elif conll_tag_entry_start == 'I' and (tag_start == -1 and tag_end == -1):

					# Same as BEGIN
					tag_start = index; tag_end = tag_start + 1
				else:
					# Increase tag range
					tag_end += 1
			else:

				# Save tag when found
				if tag_start >= 0 and tag_end >= 0:
					found_tag = { 'start': tag_start,
						'end': tag_end, 'name': conll_tag_entry_split[-1] }

					sentence['tags'].append(found_tag)

				# Reset tag range
				tag_start = -1; tag_end = -1

		# Add new parsed sentence
		mitie_sentences.append(sentence)

	# Return parsed sentences in MITIE acceptable format
	return mitie_sentences

# Run only if called directly, mostly for debugging
if __name__ == "__main__":
	# Get arguments
	args = _parse_args()

	# Group ConLL file by sentences
	grouped_conll = parse_conll_sentences(args.source_data)

	# Transform ConLL to MITIE
	mitie_format = conll_to_mitie(grouped_conll)

	# Print output to stdout
	print(mitie_format)
