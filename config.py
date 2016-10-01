#!/usr/bin/env python


class config:
 
    # file list discribe the files we want to send to client 
    # the format is like: ['source file address','dist address'],
    # you must used ',' at the end
    file_list = (
        ['image.dev.bin','/usr/local/'],
        #['image.dev.bin-800M','/usr/local/']
        #['image.dev.bin-800M','/usr/local/'],
        #['memtester_bitflip','/usr/local/sbin'],
        #['image.dev.bin','/usr/local/']
    )  
    #cmd list discribe the cmd list we want to run on client
    cmd_list = (
        'flashrom -p host -w /usr/local/image.dev.bin',
        'reboot'
    )    

    # local host name
    usr_local = 'cros'

    #local host password
    pwd_local = 'cros'
    
    # client user name
    usr_client = 'root'
    
    # client password
    pwd_client = 'test0000'    
 
    # network segment base address
    ip_base = '192.168.1.' 
   
    # ip address range to udate   
    ip_range = (100,105)

    # ip address to skip,like ip the host using
    ip_filter = [
        100, 101
    ]
