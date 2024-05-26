#!/usr/bin/env python3

"""
	USAGE:
	Copy from Safari Bookmarks.html, the desired folder of bookmarks

	Paste into read-*-list.html, wrapped in html and body tag

	Example data

	URL of transcribed EWD
	https://www.cs.utexas.edu/users/EWD/transcriptions/EWD10xx/EWD1044.html

	URL of the PDF
	https://www.cs.utexas.edu/users/EWD/ewd10xx/EWD1044.PDF

	URL of PDF as link in HTML
	<a href="../../ewd10xx/EWD1044.PDF"

"""

import xml.etree.ElementTree as ET

def to_python_array(output_file_name, lines):
	file = open(output_file_name, 'w')
	i = 0
	lines_len = len(lines)
	start_s = "arr = ["
	print(start_s, sep=' ', end='\n', file=file)

	for l in lines:
		if i != lines_len - 1:
			print(l + ',', end='\n', file=file)
		else:
			print(l, end='\n', file=file)
		i = i + 1

	end_s = "]"
	print(end_s, end='', file=file)

def iter_a_tags(input_file_name):
	tree = ET.parse(input_file_name)
	root = tree.getroot()

	lines = []

	for c in root.iter('A'):
		h = c.attrib['HREF']
		# tuple, html link, title, save_as_html
		s = f"(\"{h}\", \"{c.text.replace("\"","\\\"")}\", False)"
		lines.append(s)

	return lines

def main():
	input_file_name = "trip-report-done-list.html"
	output_file_name = "trip_report_done_list.py"
	lines = iter_a_tags(input_file_name)
	to_python_array(output_file_name, lines)

if __name__ == "__main__":
	main()

