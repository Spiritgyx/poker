import socket as SO
import threading as TH
import sys
import time
import datetime
from uuid import getnode as getMac


waitConnect = 1
wantConnect = 2
waitMsg = 3
sendMsg = 4
waitReconnect = 5
wantReconnect = 6
wantDisconnect = 10


def getLocalId():
    return getMac()


class GNet:
    waitConnect = 1
    wantConnect = 2
    waitMsg = 3
    sendMsg = 4
    waitReconnect = 5
    wantReconnect = 6
    wantDisconnect = 10
    def __init__(self, args):
        # data и connections записаны в виде списка для универсализации
        # т.е. не важно будет создаваться сервер или клиент через данный класс
        # messages = ["...", "...", ...]
        self.messages = []  # данные отправляемые соединениям
        # data = ["...", "...", ...]
        self.data = []  # данные получаемые от соединений
        # connections = [[addr, conn, status, nick, mac, slot, id, thread], ...]
        # 0,1 addr, conn: connection information
        # 2 status: waitConnect, waitMsg, sendMsg, waitReconnect, wantDisconnect,
        # wantReconnect, wantConnect,
        # 3 nick: player nickname
        # 4 mac: unique player id
        # 5 slot: -1 spectator, 0->N players on table
        # 6 id: player id in server(need to server commands kick|ban|giveCash|...)
        # 7 thread: object thread
        self.srvSock = SO.socket()
        self.connections = []  # соединения
        self.maxConnections = 0  # максимальное число соединений
        self.localId = getLocalId()  # мак-адрес устройства
        self.currentId = 0  # текущий обрабатываемый id подключения ПС нужен ли он?
        self.myType = ""  # client | server
        self.checkArgs(args)
        pass

    def setLocalId(self, ID):
        self.localId = ID

    # проверка аргументов запуска приложения
    def checkArgs(self, args):
        if len(args) == 1:
            self.myType = "client"
            self.maxConnections = 1
            self.data.append("")
            self.messages.append({"msg": "", "wantMsg": ""})
            self.connections.append(["addr", "conn", wantConnect,
                                     "nick", "mac", "slot", 0, "th"])
        if len(args) > 1:
            if args[1] == "client":
                self.myType = "client"
                self.maxConnections = 1
                self.data.append("")
                self.messages.append({"msg": "", "wantMsg": ""})
                self.connections.append(["addr", "conn", wantConnect,
                                         "nick", "mac", "slot", 0, "th"])
            elif args[1] == "server":
                self.myType = "server"
                self.maxConnections = 1
                for i in args[2:]:
                    #print(i)
                    param, value = i.split("=")
                    if param == "maxPlayers":
                        value = int(value)
                        if value >= 1:
                            self.maxConnections = value
                        else:
                            raise ValueError
                ind = 0
                for i in range(self.maxConnections):
                    self.data.append([])
                    self.messages.append({"msg": "", "wantMsg": ""})
                    self.connections.append(
                        ["addr", "conn", waitConnect,
                         "nick", "mac", "slot", ind, "th"])
                    ind += 1
                del ind
        pass

    def threadControl(self, mode, args):
        if (mode == "connect") and (self.myType == "client"):
            self.connections[0][7] = TH.Thread(target=self.client, args=(args,))
            self.connections[0][7].start()
            # self.connections[0][7].join()
        elif (mode == "create") and (self.myType == "server"):
            ip = ""
            port = 9090
            if len(args) >= 1:
                for i in args[1:]:
                    print(i)
                    param, value = i.split("=")
                    if param == "ip":
                        ip = value
                    elif param == "port":
                        port = int(value)
            self.srvSock.bind((ip, port))
            self.srvSock.listen(self.maxConnections)
            for i in range(self.maxConnections):
                self.connections[i][7] = TH.Thread(target=self.server, args=(args, i))
                self.connections[i][7].start()
                # self.connections[i][7].join()

    def client(self, args):
        ip = "127.0.0.1"
        port = 9090
        if len(args) >= 1:
            for i in args[1:]:
                # print(i)
                param, value = i.split("=")
                if param == "ip":
                    ip = value
                elif param == "port":
                    port = int(value)
        sock = SO.socket()
        # print(ip)
        try:
            sock.connect((ip, port))
        except ConnectionRefusedError:
            print("Неверный адрес")
            return 1
        self.connections[0][1] = sock
        self.connections[0][2] = waitMsg
        status = self.connections[0][2]
        msg = self.messages[0]
        while True:
            try:
                time.sleep(0.2)
                if status == waitMsg:
                    sock.settimeout(20)
                    data = sock.recv(256).decode("ascii")
                    self.data[0] = data
                    print("From server {0} bytes".format(str(len(data))))
                    self.scanMsgClient(data)
                    status = sendMsg
                    if msg["wantMsg"] == "":
                        msg["msg"] = "wait"
                    else:
                        msg["msg"] = msg["wantMsg"]
                        msg["wantMsg"] = ""
                elif status == sendMsg:
                    sock.send(bytes(msg["msg"], encoding="ascii"))
                    print("To server {0} bytes".format(str(len(msg["msg"]))))
                    status = waitMsg

                    pass
                elif status == wantDisconnect:
                    sock.close()
                    break
                    pass
                elif status == wantReconnect:
                    pass
            except ConnectionResetError:
                print("Connection with server has lost.")
                status = wantReconnect

                # TODO: запилить поток соединения клиента с сервером

    def scanMsgClient(self, data):
        if data == "wait":
            pass
        else:
            # тут присылается json с различными инструкциями
            pass
        pass

    def scanMsgServer(self, data):
        if data == "wait":
            pass
        else:
            # тут присылается json с различными инструкциями
            pass
        pass

    def server(self, args, ind):
        sock = self.srvSock
        conn, addr = sock.accept()
        print("Client {0} connected on {1} thread".format(str(addr), str(ind)))
        self.connections[ind][0], self.connections[ind][1] = addr, conn
        self.connections[ind][2] = sendMsg
        status = self.connections[ind][2]
        msg = self.messages[ind]
        if msg["wantMsg"] == "":
            msg["msg"] = "wait"
        else:
            msg["msg"] = msg["wantMsg"]
            msg["wantMsg"] = ""
        while True:
            try:
                time.sleep(0.2)
                if status == sendMsg:
                    conn.send(bytes(msg["msg"], encoding="ascii"))
                    print("To client [ID:{0}] {1} bytes".format(str(self.connections[ind][6]),
                                                                str(len(msg["msg"]))))
                    status = waitMsg
                elif status == waitMsg:
                    conn.settimeout(20)
                    data = conn.recv(256).decode("ascii")
                    self.data[ind] = data
                    print("From client [ID:{0}] {1} bytes".format(
                        str(self.connections[ind][6]), str(len(msg["msg"]))))
                    self.scanMsgServer(data)
                    status = sendMsg
                elif status == waitReconnect:
                    conn, addr = sock.accept()
                    self.connections[ind][0], self.connections[ind][1] = addr, conn
                    self.connections[ind][2] = sendMsg
                    status = self.connections[ind][2]
                    msg = self.messages[ind]
                    if msg["wantMsg"] == "":
                        msg["msg"] = "wait"
                    else:
                        msg["msg"] = msg["wantMsg"]
                        msg["wantMsg"] = ""
                pass
            except ConnectionResetError:
                print("Connection with client [id:{0},mac:{1}] has lost. Try to reconnect".format(
                    str(self.connections[ind][6]), str(self.connections[ind][4])))
                status = waitReconnect
                self.connections[ind][2] = status
        pass
