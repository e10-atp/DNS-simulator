import socket
import sys
import selectors


def makeSoc():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('[LS]: Server socket created')
        return ss
    except socket.error as err:
        print(f'socket open error {err}')


def bindSoc(sock, port):
    # binds socket to port and gets info
    sock.bind(('0.0.0.0', port))
    sock.listen(1)
    host = socket.gethostname()
    print('[LS]: Server host name is: ', host)
    print("[LS]: Server IP address is:  ", socket.gethostbyname(host))


def connectToServer(sock, portnum, hostname):
    # bind port to IP and port No. then connect to server
    serverip = socket.gethostbyname(hostname)
    server_binding = (serverip, portnum)
    sock.connect(server_binding)


def readArgs():
    # returns relevant args
    return (
        int(sys.argv[1]),
        sys.argv[2],
        int(sys.argv[3]),
        sys.argv[4],
        int(sys.argv[5])
    )


def load_server():
    (
        lsListenPort,
        ts1Hostname,
        ts1ListenPort,
        ts2Hostname,
        ts2ListenPort
    ) = readArgs()

    t1Soc = makeSoc()
    connectToServer(t1Soc, ts1ListenPort, ts1Hostname)
    t1Soc.setblocking(False)

    t2Soc = makeSoc()
    connectToServer(t2Soc, ts2ListenPort, ts2Hostname)
    t2Soc.setblocking(False)

    # soc between client and ls
    cs = makeSoc()
    bindSoc(cs, lsListenPort)
    c_sock, addr = cs.accept()
    print("[LS]: Got a connection request from a client at", addr)

    sel = selectors.DefaultSelector()
    sel.register(t1Soc, selectors.EVENT_READ, data=None)
    sel.register(t2Soc, selectors.EVENT_READ, data=None)

    while True:
        data_from_client = c_sock.recv(1024)
        if not data_from_client:
            break
        t1Soc.send(data_from_client)
        t2Soc.send(data_from_client)
        events = sel.select(timeout=5)
        if not events:
            c_sock.send(f'{data_from_client.decode("utf-8")} - Error:HOST NOT FOUND'.encode('utf-8'))
        else:
            for key, mask in events:
                sock = key.fileobj
                recv_data = sock.recv(1024)
                if recv_data is None:
                    c_sock.send(f'{data_from_client.decode("utf-8")} - Error:HOST NOT FOUND'.encode('utf-8'))
                else:
                    c_sock.send(recv_data)
                    break

    c_sock.close()
    t1Soc.close()
    t2Soc.close()


if __name__ == '__main__':
    load_server()
