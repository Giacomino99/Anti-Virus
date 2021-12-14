import sys
# print(sys.argv[1])
# o = open('/home/benis/Anti-Virus/kernel-module/out.txt', 'w')
# o.write(sys.argv[1])
# o.close()

f = open("/proc/op_ok", 'w')
if(sys.argv[2] == "/bin/cat"):
	f.write("0")
else:
	f.write("1");
f.close()