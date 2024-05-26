#!/usr/bin/env python3
"""

"""


import os
import subprocess
from urllib.parse import urljoin
import shutil

# from read_queue_list import urls as urls
from trip_report_done_list import urls as urls

def wget_save(url, name, output_dir):
	"""
	0	No problems occurred.

	1	Generic error code.

	2	Parse error---for instance, when parsing command-line options, the .wgetrc or .netrc...

	3	File I/O error.

	4	Network failure.

	5	SSL verification failure.

	6	Username/password authentication failure.

	7	Protocol errors.

	8	Server issued an error response.
	"""
	cwd = os.getcwd()
	os.chdir(output_dir)
	print(f"downloading {url} to {name}")
	name = name.replace(" ", "\\ ")
	args = ["wget","--output-document=" + "\"" + name + "\"", url]
	cmd = f"wget -q --output-document={name} {url}"
	#print(cmd)
	r = os.system(cmd)
	os.chdir(cwd)
	if r == 0 or r == 1024:
		return 0
	else:
		print(f"Subprocess error. Return Code: {r}")
		return 1


	# completed_subprocess = subprocess.run(args, capture_output=False, shell=False, cwd=output_dir, stderr=subprocess.PIPE)
	# r = completed_subprocess.returncode
	# if r == 0 or r == 1024:
	# 	return 0
	# else:
	# 	print(f"Subprocess error. Return Code: {r}")
	# 	print(completed_subprocess.stderr)
	# 	return 1


def get_pdf_link(output_file):
	pdf_url_prefix = "../../ewd"
	pdf_url_suffix = ".PDF"

	text = open(output_file, 'r', errors='replace').read()
	s = text.find(pdf_url_prefix)
	e = text.find(pdf_url_suffix)

	if s != -1 and e != -1:
		url = text[s+6:e+4]
		print(url)
		return url

	print("error: pdf url not found")
	exit(1)

def exists_and_non_empty(name):
	return os.path.isfile(name) and os.path.getsize(name) != 0

def main():
	pdf_base_url = "https://www.cs.utexas.edu/users/EWD/"
	output_dir = "trip-report-done"
	skip_if_exists = True
	dry = False
	html_link = 0
	title = 1
	save_as_html = 2
	tmp_html = "foo.html"
	output_file = os.path.join(output_dir, tmp_html)

	if dry:
		print("Dry run.")

	i = 0

	for u in urls:
		i = i + 1
		"""
		Download html
		Extract PDF relative URL
		Construct absolute URL from html and relative
		Construct output file name EWD + title
		Download PDF
		"""

		link = u[html_link].strip()
		base_name = u[title].strip()
		use_html = u[save_as_html]

		ext = ".pdf"

		tmp_name = base_name + ".pdf"

		if use_html:
			tmp_name = base_name + ".html"


		if skip_if_exists and exists_and_non_empty(tmp_name):
			print(f"{i} Skipping, existing file: {tmp_name}")
			continue

		if use_html: # want this EWD saved as html
			dl_link = link
			ext = ".html"
		elif link.lower().find("pdf") == -1:
			wget_save(link, tmp_html, output_dir) # save html version of the EWD, from which we can get the PDF link

			u = get_pdf_link(output_file).strip()
			dl_link = urljoin(pdf_base_url, u)
		else:
			dl_link = link # already have the PDF link

		if dry:
			continue

		name = base_name + ext

		if skip_if_exists and exists_and_non_empty(name):
			continue

		r = wget_save(dl_link, name, output_dir)

		if r != 0:
			print(f"Error: {i} -> {dl_link}")


	# clean up
	if os.path.exists(output_file):
		os.remove(output_file)


		# break

if __name__ == "__main__":
	main()