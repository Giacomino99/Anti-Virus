obj-m += av.o
all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
	echo > out.txt
clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
