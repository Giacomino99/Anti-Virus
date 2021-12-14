#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kallsyms.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/proc_fs.h>
#define ALLOW_SIZE  10
MODULE_DESCRIPTION("AV Kern Mod");
MODULE_AUTHOR("MMiller");
MODULE_LICENSE("GPL"); //Sure, whatever

unsigned long *sys_call_table;
asmlinkage int (*orig_execve)(const struct pt_regs *regs);
asmlinkage int (*orig_open)(char*, int, int);
asmlinkage int (*orig_openat)(const struct pt_regs *regs);

static int allow=0;
static struct proc_dir_entry* pde;
module_param(allow, int, 0660);

static inline void wp_cr0(unsigned long val)
{
    __asm__ __volatile__ ("mov %0, %%cr0": "+r" (val));
}

static inline void zero_cr0(void)
{
    wp_cr0(read_cr0() & (~0x10000));

}

static inline void one_cr0(void)
{
    wp_cr0(read_cr0() | 0x10000);

}

static ssize_t mywrite(struct file *file, const char __user *ubuf,size_t count, loff_t *ppos) 
{
    int c;
    char* buff = kmalloc(ALLOW_SIZE, GFP_KERNEL);

    if(*ppos > 0 || count > ALLOW_SIZE)
        return -EFAULT;

    if(copy_from_user(buff, ubuf, count))
        return -EFAULT;

    sscanf(buff,"%d",&allow);
    printk(buff);
    c = strlen(buff);
    *ppos = c;
    kfree(buff);
    return c;
}
 
static ssize_t myread(struct file *file, char __user *ubuf,size_t count, loff_t *ppos) 
{
    char buff[ALLOW_SIZE];
    int len = 0;

    if(*ppos > 0 || count < ALLOW_SIZE)
        return 0;
    len += sprintf(buff, "%d", allow);
    if(copy_to_user(ubuf,buff,len))
        return -EFAULT;
    *ppos = len;
    return len;
}

//asmlinkage long openat_hook(const struct pt_regs *regs)

asmlinkage int hooked_execve(const struct pt_regs *regs)
{
    char* buffer = kmalloc(PATH_MAX, GFP_KERNEL);
    char* argv[5];
    char* envp[4];

    if(strncpy_from_user(buffer, (char*)regs->di, PATH_MAX) <= 0)
    {
        printk("read failed");
        return 0;
    }
    printk("AV Scan:%s\n", buffer);

    if(strcmp(buffer, "/usr/bin/python3") == 0)
    {
        printk("NON RECURSION CHECK");
        return orig_execve(regs);
    }

    // strcpy(command, "python3 /home/benis/kernmod/new-mod/test.py ");
    // command = strcat(command, buffer);
    // printk("Command: %s", command);

    argv[0] = "/usr/bin/python3";
    argv[1] = "/home/benis/Anti-Virus/anti-virus/scan2.py";
    argv[2] = "-sf";
    argv[3] = buffer;
    argv[4] = NULL;
    
    envp[0] = "HOME=/";
    envp[1] = "TERM=linux";
    envp[2] = "PATH=/sbin:/usr/sbin:/bin:/usr/bin";
    envp[3] = NULL;

    allow = 0;
    call_usermodehelper(argv[0], argv, envp, UMH_WAIT_PROC);
    //kernel_read(res, buffer, 5, 0);
    //printk(buffer);
    //res = flip_open("/home/benis/kernmod/new-mod/res");
    if(allow)
    {
        kfree(buffer);
        return orig_execve(regs);
    }
    else
    {
        printk("VIRUS: %s", buffer);
        kfree(buffer);
        return -1;
    }
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

static struct file_operations myops = 
{
    .owner = THIS_MODULE,
    .read = myread,
    .write = mywrite,
};


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
    printk("Setting up Procfs entry");
    pde = proc_create("op_ok", 0666, NULL, &myops);
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
    proc_remove(pde);
    printk("reprot!\n");
}

module_init(simple_init);
module_exit(simple_exit);
