#!/usr/bin/env python 
'''''
   This is a open source project for everyone to save our time
you can copy and spread it freely, But , make sure not to modify 
this title content. We are devote to build a tools that can send 
file by telnet conveniently.The first version is just a simple
example that can send file by scp cmd and I will enrich it later.
Best regard for you.

@author: Eric.gao
@time  : 2016/9/22

''' 

# Import everything we need 
import pexpect 
import socket
# User login information 
user = 'root'  
mypassword = 'test0000'

# Function send_file: send one file every time 
def send_file(ip,user,mypassword,filename,dest):
    
    child = pexpect.spawn('scp %s %s@%s:%s' % ( filename,user,ip,dest ))  
    try: 
        child.expect ('Password:')  
        child.sendline (mypassword)

    except pexpect.EOF:
        child.close()
   
    child.expect(pexpect.EOF)
    print child.before
    

# Function send_cmd: send one 
def send_cmd(user,ip,cmd,mypassword): 

    child = pexpect.spawn('ssh %s@%s %s' % (user,ip,cmd))
    try:
        i = child.expect(['Password:','yes','shit'])
        if i == 0:
            child.sendline (mypassword)
        elif i == 1:
            child.sendline ('yes')
            child.expect ('Password:')
            child.sendline (mypassword)
        elif i == 2:
            print 'Time Out Error\r\n'
    except pexpect.EOF:
        child.close()

    #child.expect(pexpect.EOF)
    print "\nsend cmd '"+cmd+"'"

# Function local_cmd: run a local cmd 
def local_cmd(cmd,mypassword): 

    child = pexpect.spawn('%s' % (cmd))
    try:
        i = child.expect(['Password:','yes','shit'])
        if i == 0:
            child.sendline (mypassword)
        elif i == 1:
            child.sendline ('yes')
            child.expect ('Password:')
            child.sendline (mypassword)
        elif i == 2:
            print 'Time Out Error\r\n'
    except pexpect.EOF:
        child.close()

    #child.expect(pexpect.EOF)
    print "\nlocal cmd '"+cmd+"'"

#Function: To verify if the ip is accessable

def valid_ip(addr):

    try:
        child = pexpect.spawn('ssh root@%s %s'%(addr,'cd'))
        i = child.expect(['yes','Password:',pexpect.TIMEOUT],timeout=5)
        if i == 0:
            child.sendline('no')
            return True
        else:
            return False

    except pexpect.EOF:

        child.close()
        return False

# The main function
if __name__ == '__main__':  

    ipfilter = [
       105,
       110    
    ]

    # file list that will send to dest machine
    filelist = [
	#['test.sh','/usr/bin/'],
	#['test.mkv','/var/log/']i
         ['mp_test.txt','/']
    ]
    count = 0
    #local_cmd('rm /home/cros/.ssh/known_hosts','cros')
    # traversal all hosts in the ip range define as below 
    for ip in range(100,120):
        # kick off the host define by user 
	if ip in ipfilter:
            print '192.168.2.%s Kicked of by user\r\n'%ip
        elif valid_ip('192.168.2.%s'%ip) == False:
            print 'Skip....Invalid ip address\r\n'
        else:
            count = count + 1
            print '192.168.2.%s will be control\r\n'%ip
 
            local_cmd('rm /home/cros/.ssh/known_hosts','cros')
            send_cmd(user,'192.168.2.%s'%ip,'mount -o remount,rw /',mypassword)
    
            for one_file in filelist:
                send_file('192.168.2.%s'%ip,user,mypassword,one_file[0],one_file[1])  
    
    print 'There are %s host has been updated!'%count
 
