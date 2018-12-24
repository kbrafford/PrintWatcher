# print_queue

print_queue monitors a directory for new files of printable type (pdf, png, jpg, txt) and uses the `lp` command to print them.  It also maintains a "database" of jobs printed.

HP doesn't release drivers for my printer past Windows XP, so I made this so that I can use linux to rescue me.  I just print to a PDF in a folder that a print server VM (using VMWare Professional 15, if anyone's curious) can monitor and it routes it to the printer as well as makes an archival copy in a poor-man's filesystem database.

I'm not sure why I did the database thing, but it seemed a little prudent at least until I run this thing for awhile and make sure it works solidly.

It uses a hash of the file's name and `stat` information to try to smoothly handle overwriting the same filename, since that will probably be the main way I use it (i.e. "Save to PDF" over a file that my windows app is already set to write to).

One can also add this to the "Send To" menu in Windows.  Just add a link to the directory being monitored following the example here: https://www.howtogeek.com/howto/windows-vista/customize-the-windows-vista-send-to-menu/
