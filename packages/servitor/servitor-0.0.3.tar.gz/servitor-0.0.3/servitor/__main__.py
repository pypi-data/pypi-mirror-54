import servitor
import threading
import sys
import argparse

def readbyte(b):
	try:
		return b.decode("utf-8")
	except:
		return str(b)

def file_loop(ser):
	wfile = open(ser, "wb")
	rfile = open(ser, "rb")

	def loop():
		while 1:
			s = rfile.read(1)
			sys.stdout.write(readbyte(s))

	thr = threading.Thread(target=loop)
	thr.start()

	while 1:
		s = input()
		wfile.write(s.encode("utf-8"))

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
