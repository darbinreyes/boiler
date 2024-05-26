import os

def exception_bail(ex):
	print(f"Exception: {ex}")
	exit()

def fix_name(file_name):
	#print(f"{file_name}")
	head, tail0 = os.path.splitext(file_name)
	tail1 = tail0.replace("L", "").lower()

	try:
		os.rename(file_name, head + tail1)
	except Exception as ex:
		exception_bail(ex)

	#print(file_name)
	#print(head+tail1)



def walk_error(os_error):
	print(f"Exception: {os_error}")

def walk_noop(arg):
	pass

def walk(top, topdown=True, onerror=None, followlinks=False, func=walk_noop):
	for root, dirs, files in os.walk(top):
		for file_name in files:
			abs_path = os.path.join(root, file_name)
			abs_path = os.path.abspath(abs_path)
			func(abs_path)

def main():
	walk("done", topdown=True, onerror=walk_error, followlinks=False, func=fix_name)

if __name__ == "__main__":
	main()