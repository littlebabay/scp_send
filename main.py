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
import os
from config import config

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
    
    # Function: Building ssh authentication by sending local rsa file to remote host  
    def authentication(self):

        for rsa in config.rsa:   
            child = pexpect.spawn('scp  %s %s@%s:%s' % ( rsa[0], self.usr, self.ip, rsa[1] ))  
            try: 
                i = child.expect (['Password:','yes', ' ' ,pexpect.TIMEOUT],timeout = 30)  
                # print '%s'% (i) 
                if i == 0:
                    child.sendline(self.pwd)
                    child.read()
                elif i == 1:
                    child.sendline('yes')
                    child.expect('Password:')
                    child.sendline(self.pwd)
                    child.read()
                elif i == 2:
                    return True 
                child.read()

            except pexpect.EOF:
                child.close()
                print 'Authentication Fail at %s: Do not received valid respose!'
                return False

            except pexpect.TIMEOUT:
                child.close()
                print 'Authentication Fail at %s: Timeout Error!'%(self.ip)
                return False

        return True

    # Function send_file: send one file every time 
    def send_file(self, file_list):
   
        for files in file_list:
            os.system('scp -C %s %s@%s:%s' % ( files[0], self.usr, self.ip, files[1] ))  
            print self.ip           

    # Function send_cmd: send one 
    def send_cmd(self,cmd_list): 

        for cmd in cmd_list:
            os.system('ssh %s@%s %s' % (self.usr, self.ip, cmd))  


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



def valid_ip(addr):

    try:
        child = pexpect.spawn('ssh root@%s %s'%(addr,'uname -a'))
        i = child.expect(['yes','Password:','Linux',pexpect.TIMEOUT],timeout=2)
        # print '%s'%(i)
        if i == 0 :
            child.sendline('no')
            child.read()
            child.close()
            return True
        elif i == 1 :
            child.sendline('test0000')
            child.read()
            child.close()
            return True
        elif i == 2:
            child.close()
            return True
        else:
            child.close()
            return False

    except pexpect.EOF:

        child.close()
        return False

    except pexpect.TIMEOUT:
        child.close()
        return False


class  update_client(threading.Thread):

    ip = ''
    file_list = ''
    cmd_list = ''
    usr = ''
    pwd = ''

    def __init__(self, ip, usr, pwd, file_list, cmd_list):

        threading.Thread.__init__(self)
        self.ip = ip
        self.usr = usr
        self.pwd = pwd
        self.file_list = file_list
        self.cmd_list = cmd_list

    def run(self):
        
        if (valid_ip(self.ip)) == False:
            return False
        else: 
            # host = local_host(config.usr_local,config.pwd_local)

            # host.local_cmd('rm /home/cros/.ssh/known_hosts')

            child = remote_client(self.ip,self.usr,self.pwd)
        
            result = child.authentication()
        
            if result == True:
                child.send_file(self.file_list)
                child.send_cmd(self.cmd_list)
            
# The main function
if __name__ == '__main__':  
    # Create a empoty client thread object list 
    client_list = []
    
    # Skip user assign ip and invalid ip ,then creat a thread for every valid ip.
    for ip in range(config.ip_range[0],config.ip_range[1]):
        if ip in config.ip_filter:
            print "Skip Ip"
        else:
            client_list.append(update_client('%s%s'%(config.ip_base,ip),config.usr_client,config.pwd_client,config.file_list,config.cmd_list))

    # start all the threads
    for client in client_list:
        client.start()
    

