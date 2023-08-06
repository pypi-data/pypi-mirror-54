import rubicon
import threading
import sys
import argparse

def file_loop(ser):
	wfile = open(ser, "w")
	rfile = open(ser, "r")

	def loop():
		while 1:
			s = rfile.read(1)
			print(s)

	thr = threading.Thread(target=loop)
	thr.start()

	while 1:
		s = input()
		wfile.write(s)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("args", type=str, nargs="*", help="targets")
	pargs = parser.parse_args()

	args = pargs.args

	if len(args) == 0:
		print("usage: rubicon PATH")
		sys.exit(0)

	ser = args[0]

	file_loop(ser)
