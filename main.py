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
import time
import threading

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
    
    # Function send_file: send one file every time 
    def send_file(self, file_list):
   
        for files in file_list:

            child = pexpect.spawn('scp -C %s %s@%s:%s' % ( files[0], self.usr, self.ip, files[1] ))  
            try: 
                i = child.expect (['Password:','yes',pexpect.TIMEOUT],timeout = 30)  
            
                if i == 0:
                    child.sendline (self.pwd)
                elif i == 1:
                    child.sendline ('yes')
                    child.expect('Password:')
                    child.sendline (self.pwd)
                   # child.read()
            except pexpect.EOF:
                child.close()
                print 'Not receive the needed key word!'

            except pexpect.TIMEOUT:
                child.close()
                print 'Timeout Error!'

            child.expect(pexpect.EOF)  
            print child.before+self.ip

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

#    def __del__(self):

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
#        print "\nlocal cmd '"+cmd+"'"


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

class  update_client(threading.Thread):

    ip = ''
    file_list = ''
    cmd_list = ''
    usr = 'root'
    pwd = 'test0000'

    def __init__(self, ip, file_list, cmd_list):

        threading.Thread.__init__(self)
        self.ip = ip
        self.file_list = file_list
        self.cmd_list = cmd_list

    def run(self):

        host = local_host('cros','cros')

        host.local_cmd('rm /home/cros/.ssh/known_hosts')

        child = remote_client(self.ip,self.usr,self.pwd)
        child.send_file(self.file_list)
        child.send_cmd(self.cmd_list)
        
# The main function
if __name__ == '__main__':  

    file_list = (
        #['image.dev.bin-800M','/usr/local/']
        ['image.dev.bin-800M','/usr/local/'],
        ['image.dev.bin-800M','/usr/local/'],
        ['ddr_read_data_eye_down.down','/usr/local/'],
        ['ddr_read_data_eye_up.up','/usr/local/']
    )

    cmd_list =(

    )    

    ip_base = '192.168.2'    

    ip_filter = [
        101
    ]
    #count = 0

    client1 = update_client('192.168.1.101',file_list,cmd_list)
    client2 = update_client('192.168.1.104',file_list,cmd_list)
    client3 = update_client('192.168.1.103',file_list,cmd_list)

    client1.start()
    client2.start()
#    client3.start()
"""
    for ip in range(118,119):

        host.local_cmd('rm /home/cros/.ssh/known_hosts')
   
        if ip in ip_filter:
            print "Skip Ip"

        elif valid_ip('192.168.2.%s'%ip) == False:
            print "Invalid IP"

        else:

            client1 = update_client()
             
            
            client = remote_client('192.168.2.%s'%ip,'root','test0000')
    
            client.send_file(file_list)
"""
            




