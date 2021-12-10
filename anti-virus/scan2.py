import hashlib
import re
import os
import sys

mal = []
dirs = []
warn = 0
# scan_dirs = []
# -s scan
# -sf scan file
# -mh add mal hashes
# -ms add mal signatures
# -w print warnings
def main_scan(): 
	scan_db = open("scan_db")
	dirs = scan_db.read().split("\n")

	hlp = '''-?\tPrint this help and quit
-s\tScan from scan_db
-sf\tScan specified file or directory (Ex: -sf /some/dir/file.ex)
-mh\tAdd malware hashes (Ex: -mh SomeMD5HashHere AnotherOne ...)
-ms\tAdd malware signatures (Ex: -ms SomeSigInHexFormat AnotherOne ...)
-w\tPrint warnings'''

	if('-?' in sys.argv or len(sys.argv) <= 1):
		print(hlp)
		return

	sigs = []
	hashes = []
	single = ""
	scan = 0

	mode = -1

	global warn

	for i in range(1, len(sys.argv)):
		if(sys.argv[i] == '-s'):
			scan = 1
			mode = 0
			continue
		if(sys.argv[i] == '-mh'):
			mode = 1
			continue
		if(sys.argv[i] == '-ms'):
			mode = 2
			continue

		if(sys.argv[i] == '-sf'):
			mode = 3
			scan = 2
			continue

		if(sys.argv[i] == '-w'):
			mode = 4
			warn = 1
			continue

		if(mode == -1):
			print("Bad Arguments!")
			print(hlp)
			return

		if(mode == 1):
			hashes.append(sys.argv[i])
			continue
		if(mode == 2):
			sigs.append(sys.argv[i])
			continue
		if(mode == 3):
			single = sys.argv[i]
			continue

	f = open("hash_db", 'a')
	for h in hashes:
		f.write("\n"+h)
	f.close()

	f = open("regx_db", 'a')
	for s in sigs:
		f.write("\n"+s)
	f.close()

	if(scan == 1):
		for i in dirs:
			scan_file(i)
		print_mal()

	if(scan == 2):
		if(single == ""):
			print("No File Given\n")
		scan_file(single)
		print_mal()
	
	return mal
	
def scan_file(file):
	f_allow = open("file_allow", 'r')
	allows = f_allow.read().split("\n")
	if(file in allows):
		return
	if(os.path.isfile(file)):
		hash_scan(file)
		regx_scan(file)
		return
	if(os.path.isdir(file)):
		dir_scan = os.scandir(file)
		for e in dir_scan:
			scan_file(e.path)
		return
	if(warn):
		print("INFO: Bad Path: " + file)

def regx_scan(file):
	global warn
	f = open(file, 'rb')
	b = f.read().hex()
	regx_db = open("regx_db", 'r')
	regxs = regx_db.read().split("\n")
	for i in regxs:
		rx = re.search(i, b)
		if(rx):
			mal.append(file)
			if(warn):
				print("\033[31;6;7mWARNING:\033[0;0m FILE:", file, "MATCHED REGEX:", rx[0][0:32]+"...("+str(len(rx[0])-32)+")" if len(rx[0])>32 else rx[0])
			return
	

def hash_scan(file):
	global warn
	md5 = hash_file(file)
	md5_allow = open("md5_allow", 'r')
	allows = md5_allow.read().split("\n")
	if(md5 in allows):
		return
	hash_db = open("hash_db")
	hashes = hash_db.read().split("\n")
	for h in hashes:
		if md5 in h:
			mal.append(file)
			if(warn):
				print("\033[31;6;7mWARNING:\033[0;0m FILE:", file, "MATCHED HASH:", md5)
			return

def hash_file(file):
	md5 = hashlib.md5()
	f = open(file, 'rb')
	b = f.read()
	md5.update(b)
	return md5.hexdigest()

def print_mal():
	if(warn):
		print("\n", "-"*40, "\n")
	print("Potentially Malicious Files: ("+str(len(mal))+")")
	for m in mal:
		if(os.name == "nt"):
			m=m.replace("/", "\\")
		print("\t",m)

if __name__ == '__main__':
	main_scan()
	# write mal[] to a file
	a_list = main_scan()
	if not a_list:
		file = open("malfile.txt","w")
		file.close()
	else:
		text = open("malfile.txt", "w")
		for element in a_list:
			text.write(element + "\n")
		text.close()


