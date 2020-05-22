import os
import socket
import sys


def readserver(serverfile):
    adict = {}
    relpath = os.path.dirname(__file__)
    filename = os.path.join(relpath, serverfile)
    with open(filename, 'r') as f:
        for line in f:
            splitline = line.split(' ')
            url = splitline[0]
            ip = splitline[1]
            adict[url] = ip
    return adict


def makeSoc():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('[TS2]: Server socket created')
        return ss
    except socket.error as err:
        print('{} \n'.format('socket open error ', err))


def bindSoc(sock, port):
    # binds socket to port and gets info
    server_binding = ('0.0.0.0', port)
    sock.bind(server_binding)
    sock.listen(1)
    host = socket.gethostname()
    print('[TS2]: Server host name is: ', host)
    print("[TS2]: Server IP address is:  ", socket.gethostbyname(host))


def getDictVal(k, dict):
    #case insenstive get for dict, returns value
    for key in dict:
        if key.lower() == k.lower():
            return key, dict[key]
    return None, None

def ts2():
    adict = readserver('PROJ2-DNSTS2.txt')
    print(adict)
    tsListenPort = int(sys.argv[1])
    print(tsListenPort)
    ss = makeSoc()
    bindSoc(ss, tsListenPort)
    c_sock_id, addr = ss.accept()
    print("[TS2]: Got a connection request from a LS at", addr)

    while True:
        data_from_client = c_sock_id.recv(1024)
        if not data_from_client:
            break
        decodeData = data_from_client.decode('utf-8')
        print('[TS2]: Data received from LS:: ', decodeData)

        hostname, ip = getDictVal(decodeData, adict)
        if hostname is not None:
            msg = f'{hostname} {ip} A'
            c_sock_id.send(msg.encode('utf-8'))

    ss.close()
    c_sock_id.close()


if __name__ == '__main__':
    ts2()
