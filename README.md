# BOF fuzzer for OSCP python 3 All in one
Send controlled amount of bytes, send msf-pattern, calculate offset, custom buffer, badcharacters all in one.

Generally when you go through the buffer overflow procedure, I tend to make a messy python script, that keeps on getting updated with sloppy code.
That's why I created this fuzzer to keep it organized, and be more efficient.

Why use this fuzzer?
Run it once, after that you will have: offset and the badcharacters, only thing left after that is to find the jmp esp(or any other register), run msfvenom and send the buffer.

Quality of life features:
Keeps track of: buffer size, offset and prefixes -> thus no need to retype everytime.

Typical use case:
1) Open vulnerable program with immunity debugger.
2) Use MODE 2, and send bytes till you get an overflow.  RESET IMMUNITY.
3) Use MODE 3, (script already remembers the last buffer size you sent), and it automatically send buffer of msf-pattern. RESET IMMUNITY.
4) Use MODE 4, (script already remembers the last buffer size you sent), input the eip you saw, and get the offset, which is automatically set in script.  RESET IMMUNITY.
5) Use MODE 6, (script already remembers the last buffer size and offset you sent), MODE 1 (place badchars after eip), and manually check the buffer on immunity. RESET IMMUNITY

Usage:

python3 bof_fuzzer.py -ip <IP> -p <Port> -prefix <Prefix> -offset <Offset> -size <Buffer Size>

### You can run the script without arguments, and you can change the arguments while script is running.

Hope this script will make your life easier, but make sure to know what you are doing.

Demo of the script will be available soon on my website:  https://bytesdeluge.com

-AceSineX
