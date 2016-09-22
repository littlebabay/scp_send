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
import pexpect  

def send_file(ip,user,mypassword):
    
    child = pexpect.spawn('scp %s %s@%s:/' % ( './test.txt',user,ip ))  
    try: 
        child.expect ('Password:')  
        child.sendline (mypassword)

    except pexpect.EOF:
        child.close()
   
    child.expect(pexpect.EOF)
    print child.before

if __name__ == '__main__':  
    user = 'root'  
    ip = '192.168.1.104'  
    mypassword = 'test0000'  
    
    send_file(ip,user,mypassword)  
   
