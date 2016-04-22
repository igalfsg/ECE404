#! /bin/bash

#Reset tables
iptables -t nat -F
iptables -F

#Place no restriction on outbond packets
iptables -I OUTPUT 1 -j ACCEPT

#Block this IP's
IPlist = ("10.10.1.1" "192.168.24.21") 
for i in ${IPlist[@]}
do
   iptables -A INPUT -s $i -j REJECT
done


#Block incoming Pings
iptables -A INPUT -p icmp --icmp-type echo-request -j REJECT

#forward unused port to port 22
#activate random port 9000
iptables -A INPUT -p tcp --dport 9000 -j ACCEPT

#now send it to port 22
iptables -t nat -A PREROUTING -p tcp  --dport 9000 -j DNAT --to-destination 10.164.202.1:22

#accept forwarding ports in 22
iptables -A FORWARD -p tcp --dport 22 -j ACCEPT

#only allow ssh in port 22 from ecn
iptables -A INPUT -s ecn.purdue.edu -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j REJECT

#accept http requests only from an ip
iptables _A INPUT -p tcp -s 128.46.4.86 --dport 80 -j ACCEPT
iptables _A INPUT -p tcp --dport 80 -j REJECT

#accept Auth/Ident in port 113
iptables -A INPUT -p tcp --dport 113 -j ACCEPT
