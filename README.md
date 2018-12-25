# PrintWatcher

PrintWatcher monitors a specified directory for new files of printable type (pdf, png, jpg, txt or user selectable) and shells out to the `lp` command to print them.  It also maintains a "database" of jobs printed.

    Usage: printd.py [OPTIONS] DIRECTORY

    Options:
      --ptime FLOAT  loop polling interval (default: 2.5s)
      --ext TEXT     what types to print (default: "pdf;png;jpg;txt")
      --log TEXT     directory for archive of printed files (default: _log)
      --cmd TEXT     print command to shell out to (default: lp)
      --help         Show this message and exit.

PrintWatcher reads the inital contents of the print folder and deliberately ignores those files that were there at the time the program is started.  Only changes to the folder that occur after launching `printd.py` are tracked and acted on.

Note: I have only tested this on 64-bit linux, not 32-bit.  The only issue that might come up is the `hash()` of the `os.stat()` call. 
It probably won't make a difference, but I notice that the hash function on 64-bit python is different enough than 32-bit python 
that it warants a closer look to make sure the hashing strategy of the `FileStore` still works the same.

    Python 2.7.15rc1 (default, Apr 15 2018, 21:51:34) 
    [GCC 7.3.0] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import os
    >>> import platform
    >>> platform.architecture()
    ('64bit', '')
    >>> [hex(hash(os.stat(f))) for f in os.listdir(".")]
    ['-0x2d2b0f1830658e14', '0x5fb210d4cf3c423', '-0x171c8db56ac54d0b', '0x7cf4a771ab6b6683', '0x46e74ddba82eb094', '-0x68c2e04bab6d4b69', '-0x2c207fa10106623b', '0x41a4407a21404b7c', '0x260e7e4be4d75c2b']

    Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import os
    >>> import platform
    >>> platform.architecture()
    ('32bit', 'WindowsPE')
    >>> [hex(hash(os.stat(f))) for f in os.listdir(".")]
    ['-0x11e55e73', '-0x17add4d6', '0x43ce4ee2', '0x4a71ae77', '-0x73fbb891', '-0x279ad375', '0x21220556', '0x9af37e6', '0x78bd18e9']
   

## Quick Start

Make a directory visible from the linux box that can successfully use your printer. Make this directory in a share that is also visible from the gimped-up computer that can't use the printer as well.

In the case of a linux guest in on a windows host, it might look like this:

    /mnt/hgfs/E/VMSHARE/
    
Clone the PrintWatcher repo into a folder there and change into the directory:

    git clone https://github.com/kbrafford/PrintWatcher.git
    cd PrintWatcher
    
Make sure the `printd.py` file is marked as executable:

    chmod +x printd.py
    
Create a directory for the print "queue":

    mkdir _q
    
From the linux machine (with the printer), launch the monitor and leave it running:

    ./printd.py _q
    
That's it!  Now you should be able to copy files into this directory (the `_q` directory you made) and they will be sent to your printer.
    

## Purpose

HP hasn't released a driver for my printer since Windows XP. Seriously. When I moved to Windows 7, I actually had to install Microsoft's clever insurance against another Vista-style debacle, the ["WinXP Mode" Virtual PC image](https://www.wikihow.com/Install-Windows-XP-Mode-in-Windows-7) just so I could use my printer.

The other day I had an urgent need to print something. It reminded me of when I needed to find an actual typewriter in order to fill out the application to grad school.  Anyway, time was of the essence, and I was tired of leeching off of my employer's printer or going to FedEx late at night every time I need something printed.  

I finally got [VMWare Workstation Pro](https://www.vmware.com/products/workstation-pro.html) installed on my home dev box. It's a nice Xeon CPU with lots of ECC memory and has been the most stable computer I've had, so I am in no hurry to upgrade to a new OS yet.  I always intended to partition my work into multiple virtual servers but never actually followed through until now.

I set up several Mint Linux virtual machines, and earmarked one for the printer.  I plugged in the laserjet and VMWare intercepted the USB connection and offered to connect to it.  I selected the print server VM and Mint Linux already had a driver ready to go.  Inside the Linux VM issuing the command `lp filename.pdf` was enough to get my printout finally!  Turns out after 7 years I also need to get new toner, but at least Amazon has also been busy innovating its business since the last time I needed print supplies too :-)

After seeing how freaking easy it was to print from the Linux side I decided to automate the process.

I set up a shared folder that can be seen from the Windows host or any of the Linux guests and wrote a Python "pseudo-daemon" that just polls the directory and looks for new files to show up. In order to support the use-case where I am over-writing the same file--which is a common way to "print" if you are making intermediate PDF files--I made a key of a hash of the file's inode data and the filename to decide when a new file has shown up.

Once that was mostly working, I realized that I could just save off a copy of all printed files into a temp archive too. It helped during the debug, plus the `FileStore` class is something that I've thrown together a few times in different flavors as a debug tool over the years, and I think I might do a side-project to formalize it for reuse. Or maybe I'll finally learn how to use a NoSQL db like a real developer.

BTW you can also add this to the "Send To" menu in Windows.  Just add a link to the directory being monitored following the example [here](https://www.howtogeek.com/howto/windows-vista/customize-the-windows-vista-send-to-menu/) and now when you right-click on any file in Windows Explorer you can "Send To" your print folder...and it prints, like as if you had for-realz printer support!
