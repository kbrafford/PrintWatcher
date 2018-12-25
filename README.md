# PrintWatcher

PrintWatcher monitors a specified directory for new files of printable type (pdf, png, jpg, txt or user selectable) and shells out to the `lp` command to print them.  It also maintains a "database" of jobs printed.

    Usage: printd.py [OPTIONS] DIRECTORY

    Options:
      --ptime FLOAT  loop polling interval (default: 2.5s)
      --ext TEXT     what types to print (default: "pdf;png;jpg;txt")
      --log TEXT     directory for archive of printed files (default: _log)
      --cmd TEXT     print command to shell out to (default: lp)
      --help         Show this message and exit.


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
