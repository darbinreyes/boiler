import os

def walk(dir):
	for root, dirs, files in os.walk(dir):

def main():
	walk()

if __name__ == "__main__":
	main()