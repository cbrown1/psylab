# -*- coding: utf-8 -*-

import sys

if sys.platform == 'linux2':
    # Confirmed working on linux
    import termios, os
    TERMIOS = termios
    def getchar():
        #Returns a single character from standard input
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

elif sys.platform == "win32":
    from msvcrt import getch
    def getchar():
        ch = getch()
        return ch

elif sys.platform == "darwin":
    raise Exception, "This feature not yet supported on mac"

if __name__ == '__main__':
    print 'type something'
    s = ''
    while 1:
        c = getchar()
        if c == 'q':
                break
        print "captured key", c
