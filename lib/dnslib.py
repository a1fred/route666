#!/usr/bin/env python

import sys
import socket
import fcntl
import struct


class DNSQuery:
    """
    DNSQuery class from
    http://code.activestate.com/recipes/491264-mini-fake-dns-server/
    """

    def __init__(self, data):
        self.data = data
        self.domain = ''

        tipo = (ord(data[2]) >> 3) & 15   # Opcode bits
        if tipo == 0:                     # Standard query
            ini = 12
            lon = ord(data[ini])
            while lon != 0:
                self.domain += data[ini+1:ini+lon+1]+'.'
                ini += lon + 1
                lon = ord(data[ini])

    def success_packet(self, ip):
        packet = ''
        if ip:
            packet += self.data[:2] + "\x81\x80"
            packet += self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'  # Questions and Answers Counts
            packet += self.data[12:]  # Original Domain Name Question
            packet += '\xc0\x0c'  # Pointer to domain name
            packet += '\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'  # Response type, ttl and resource data length -> 4 bytes
            packet += str.join('', map(lambda x: chr(int(x)), ip.split('.'))) # 4bytes of IP
        return packet

    def error_packet(self):
        packet = ''
        packet += self.data[:2] + "\x81\x83"
        packet += self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'  # Questions and Answers Counts
        packet += self.data[12:]  # Original Domain Name Question
        packet += '\xc0\x0c'  # Pointer to domain name
        packet += '\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x00'  # Response type, ttl and resource data length -> 4 bytes
        return packet

    def respuesta(self, ip):
        try:
            str.join('', map(lambda x: chr(int(x)), ip.split('.')))
            return self.success_packet(ip)
        except ValueError:
            return self.error_packet()
        except AttributeError:
            return self.error_packet()



#
def get_interface_ip_address(ifname):
    """
    get_ip_address code from ifname
    http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
            )[20:24])
    except:
        return None


def BindServer(ip='', port=53, resolver=None):
    try:
        udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udps.bind((ip, port))
    except Exception, e:
        print "Failed to create socket on UDP port 53:", e
        sys.exit(1)

    print 'Route666 :: * 60 IN A %s\n' % ip

    try:
        while 1:
            data, addr = udps.recvfrom(1024)
            p = DNSQuery(data)
            resp = resolver(p.domain)
            udps.sendto(p.respuesta(resp), addr)
            print 'Request: %s -> %s' % (p.domain, resp)
    except KeyboardInterrupt:
        print '\nBye!'
        udps.close()
