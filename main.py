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

"""
  This is remote_client class to discribe a remote client machine.
we can do some operates on the remote machine through network.We 
need to know the ip address ,user name , password of client.

"""
class remote_client:
    
    ip = ""
    usr = ""
    pwd = ""

    # init function
    def __init__(self, ip, usr, pwd):
        self.ip = ip
        self.usr = usr
        self.pwd = pwd
        print "\r\n######################### %s@%s  ############################"%(self.usr,self.ip)
    
    # Function send_file: send one file every time 
    def send_file(self, file_list):
   
        for files in file_list:

            child = pexpect.spawn('scp %s %s@%s:%s' % ( files[0], self.usr, self.ip, files[1] ))  
            try: 
                i = child.expect (['Password:','yes',pexpect.TIMEOUT],timeout = 30)  
            
                if i == 0:
                    child.sendline (self.pwd)
                elif i == 1:
                    child.sendline ('yes')
                    child.expect('Password:')
                    child.sendline (self.pwd)
                    child.read()
            except pexpect.EOF:
                child.close()
                print 'Not receive the needed key word!'

            except pexpect.TIMEOUT:
                child.close()
                print 'Timeout Error!'
   
            child.expect(pexpect.EOF)
            print child.before
    

    # Function send_cmd: send one 
    def send_cmd(self,cmd): 

        child = pexpect.spawn('ssh %s@%s %s' % (self.usr, self.ip, cmd))
        try:
            i = child.expect(['Password:','yes',pexpect.TIMEOUT],timeout=5)
            if i == 0:
                child.sendline (self.pwd)
            elif i == 1:
                child.sendline ('yes')
                child.expect ('Password:')
                child.sendline (self.pwd)
                child.read()

        except pexpect.EOF:
            child.close()
            print 'Not receive the needed key word!'

        except pexpect.TIMEOUT: 
            child.close()
            print 'Timeout Error!'

        child.expect(pexpect.EOF)
        print "send cmd '"+cmd+"'"

    def __del__(self):

        print 'Exit\r\n'

"""
   This is a local_host class to describe ourself,we can 

run some command on local host.you need to know my user name

and password.

"""
class local_host():

    usr = ''
    pwd = ''

    def __init__(self,usr,pwd):
        self.usr = usr
        self.pwd  = pwd

    # Function local_cmd: run a local cmd 
    def local_cmd(self,cmd): 

        child = pexpect.spawn('%s' % (cmd))
        try:
            i = child.expect(['Password:','yes','',pexpect.TIMEOUT],timeout = 5)
            if i == 0:
                child.sendline (self.pwd)
                print 1
            elif i == 1:
                child.sendline ('yes')
                child.expect ('Password:')
                child.sendline (self.pwd)
                print 2
            child.read()
            child.close()

        except pexpect.EOF:
            child.close()
            print 'No valid Response!'

        except pexpect.TIMEOUT:
            child.close()
            print 'Timeout Error'
            
        #child.expect(pexpect.EOF)
        print "\nlocal cmd '"+cmd+"'"


#Function: To verify if the ip is accessable

def valid_ip(addr):

    try:
        child = pexpect.spawn('ssh root@%s %s'%(addr,'cd'))
        i = child.expect(['yes','Password:',pexpect.TIMEOUT],timeout=5)
        if i == 0 or i ==1:
            child.sendline('no')
            return True
        else:
            return False

    except pexpect.EOF:

        child.close()
        return False

# The main function
if __name__ == '__main__':  

    file_list = (
        #['image.dev.bin-800M','/usr/local/']
        ['ddr_read_data_eye_up.up','/usr/local/'],
        ['ddr_read_data_eye_down.down','/usr/local/']
    )    

    ip_base = '192.168.2'    

    ip_filter = [
        101
    ]

    count = 0

    host = local_host('cros','cros')

    for ip in range(118,119):

        host.local_cmd('rm /home/cros/.ssh/known_hosts')
   
        if ip in ip_filter:
            print "Skip Ip"

        elif valid_ip('192.168.2.%s'%ip) == False:
            print "Invalid IP"

        else:
             
            count = count +1
            
            client = remote_client('192.168.2.%s'%ip,'root','test0000')
    
            client.send_file(file_list)

            # client.send_cmd('sudo chmod 777 update_firmware && /usr/local/update_firmware')
            #client.send_cmd('stop powerd')
            
            del client

    print 'Successfuly update %s client'%count




