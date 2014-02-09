#!/usr/bin/python
import argparse
import socket
import sys
    
# We can't use regular python-memcache since it doesn't enable explicit flag setting. Implememnt my own.
class MemcacheRaw:
    def __init__(self, addr='localhost', port=11211, timeout=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        self.sock.connect((addr, port))
        
    def set(self, key, val, flags=0, expiry=0):
        self.sock.sendall('set %s %d %d %d\r\n%s\r\n'%(key, flags, expiry, len(val), val))
        if not self.sockExpect('STORED\r\n'):
            raise Exception('Failed to store key %s'%key)
            
    def sockExpect(self, expect):
        buf = ''
        while True:
            d = self.sock.recv(len(expect) - len(buf))
            if not d:
                raise Exception('Socket closed')
            buf += d
            if len(buf) == len(expect):
                if buf == expect:
                    return True
                else:
                    return False

if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description='memcache populator.')
    argParser.add_argument('--addr', default='localhost', help='Server address. Defaults to localhost.')
    argParser.add_argument('--port', default=11211, type=int, help='Server port. Defaults to 11211.')
    argParser.add_argument('csv_file', help='CSV File to read data from. See: https://github.com/RedisLabs/memcache_populator for details.')
    
    args = argParser.parse_args()
    
    # Open input file
    try:
        f = open(args.csv_file)
    except Exception as e:
        print >> sys.stderr, 'Error %s opening file: %s'%e
        exit(1)

    # Connect to server
    try:
        srv = MemcacheRaw(addr=args.addr, port=args.port)
    except Exception as e:
        print >> sys.stderr, 'Error connecting to server: %s'%e
        exit(1)

    # Parse CSV file and fill server
    try:
        while True:
            line = f.readline()
            if not line:
                break
            parts = line.strip().split(',')
            srv.set(parts[0].decode('string_escape'), parts[1].decode('string_escape'), int(parts[2], 16), int(parts[3]))
    except Exception as e:
        print >> sys.stderr, 'Failed populating server from csv file: %s'%e
        exit(1)
