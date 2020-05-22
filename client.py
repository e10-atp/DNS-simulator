import os
import socket
import sys


def readHNS():
    urls = list()
    relpath = os.path.dirname(__file__)
    filename = os.path.join(relpath, 'PROJ2-HNS.txt')
    with open(filename, 'r') as f:
        for line in f:
            urls.append(line.strip())
    return urls


def makeSoc():
    try:
        Soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('[C]: Client socket created')
        return Soc
    except socket.error as err:
        print('{} \n'.format('socket open error ', err))


def connect(sock, port, hostname):
    # bind port to IP and port No. then connect to server
    serverip = socket.gethostbyname(hostname)
    server_binding = (serverip, port)
    sock.connect(server_binding)


def makeWriteFile():
    relpath = os.path.dirname(__file__)
    outname = os.path.join(relpath, 'RESOLVED.txt')
    outfile = open(outname, 'w')
    return outfile


def client():
    lsHostName = sys.argv[1]
    lsListenPort = int(sys.argv[2])
    urls = readHNS()
    print(urls)
    lsSoc = makeSoc()
    connect(lsSoc, lsListenPort, lsHostName)

    out = makeWriteFile()
    for link in urls:
        lsSoc.send((link.encode('utf-8')))
        lsData = lsSoc.recv(1024)
        lsdecoded = lsData.decode('utf-8')
        print('[C]: Data received from LS:: ', lsdecoded)
        out.write(f'{lsdecoded}' + '\n')

    lsSoc.close()
    out.close()


if __name__ == '__main__':
    client()
