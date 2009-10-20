#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: ts=4 sts=4 sw=4 tw=79 sta et
"""
Overrides the socket interface in python to provide SOCKS support
on outgoing connections

Uses SOCKS 4a

"""

__author__ = 'Patrick Butler'
__email__  = 'pbutler@killertux.org'

#from socket import *
import socket as _socket
import struct
import sys
sys.modules['socket']._old_socket = sys.modules['socket'].socket

socks_ip   = "127.0.0.1"
socks_port = 9050

def set_socks_ip(sip, sport):
    """
    Sets the ip and port for the socks server
    """
    global socks_ip, socks_port
    socks_ip   = sip
    socks_port = sport

def connect_msg(ip, port):
    """
    Uses socks4a protocol so you can pass an IP address or a hostname
    """
    #ip to int
    #ips = map(int, ip.split("."))
    msg = struct.pack("!BBHBBBB", 0x4, 0x1, int(port), 0x0, 0x0, 0x0, 0x1)
    msg += "python"+'\0'
    msg += ip +'\0'
    return msg


class socket(_socket._old_socket):
    def connect(self, address):
        global socks_ip, socks_port
        self.r_ip   = address[0]
        self.r_port = address[1]
        _socket._old_socket.connect(self, (socks_ip, socks_port))
        self.send(connect_msg(self.r_ip, self.r_port))
        result = self.recv(8)
        okay = struct.unpack("!BBHL", result)
        if okay[1] == 0x5a:
            return
        else:
            raise ValueError, "Failed with code: %s" % hex(okay[1])

sys.modules['socket'].socket = socket

if __name__ == "__main__":
    import sys
    import urllib2
    req = urllib2.Request("http://www.whatismyip.com/automation/n09230945.asp", headers = {"User-Agent" :'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
    print urllib2.urlopen(req).read()

#    s = socket()
#    s.settimeout(3)
#    s.connect( ("google.com", 80) )
#    s.send("GET /ncr HTTP/1.1\r\nHost: www.google.com\r\nUser-Agent: Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)\r\n\r\n")
#    while True:
#        m = s.recv(1024)
#        if len(m) == 0:
#            break
#        sys.stdout.write(m)
#        sys.stdout.flush()
#    s.close()
    sys.exit(0)
