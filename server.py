import socket 
from _thread import *
import sys
from collections import defaultdict as df
import time


class Server:
    def __init__(self):
        self.rooms = df(list)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def accept_connections(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.count = 0
        self.server.bind((self.ip_address, int(self.port)))
        self.server.listen(100)

        while True:
            connection, address = self.server.accept()
            print(str(address[0]) + ":" + str(address[1]) + " Connected")
            print(str(self.count))

            start_new_thread(self.clientThread, (connection,))

        self.server.close()

    
    def clientThread(self, connection):
        user_id = connection.recv(1024).decode().replace("User ", "")
        room_id = connection.recv(1024).decode().replace("Join ", "")

        message = connection.recv(1024)
        print(str(message.decode()))

        if room_id not in self.rooms:
            connection.send("New Group created".encode())
        else:
            connection.send("Welcome to chat room".encode())

        if message:
            if str(message.decode()) == "PC":
                self.count += 1

        if (self.count > 2):
            print("room full")
            self.rooms[port].append(connection)
            connection.send("This Room is a personal room\n".encode())
            connection.send("The Room is full\n".encode())
            connection.send("Please restart the APP and pick another room\n".encode())
            self.remove(connection, room_id)
                
        else :
            self.rooms[room_id].append(connection)
            # if room_id not in self.rooms:
            #     connection.send("New Group created".encode())
            # else:
            #     connection.send("Welcome to chat room".encode())
            while True:
                try:
                    message = connection.recv(1024)
                    print(str(message.decode()))
                    if message:
                        if str(message.decode()) == "FILE":
                            self.broadcastFile(connection, room_id, user_id)

                        else:
                            message_to_send = str(user_id) + " : " + message.decode()
                            self.broadcast(message_to_send, connection, room_id)

                    else:
                        self.remove(connection, room_id)
                except Exception as e:
                    print(repr(e))
                    print("Client disconnected earlier")
                    break
    
    
    def broadcastFile(self, connection, room_id, user_id):
        file_name = connection.recv(1024).decode()
        lenOfFile = connection.recv(1024).decode()
        for client in self.rooms[room_id]:
            if client != connection:
                try: 
                    client.send("FILE".encode())
                    time.sleep(0.1)
                    client.send(file_name.encode())
                    time.sleep(0.1)
                    client.send(lenOfFile.encode())
                    time.sleep(0.1)
                    client.send(user_id.encode())
                except:
                    client.close()
                    self.remove(client, room_id)

        total = 0
        print(file_name, lenOfFile)
        while str(total) != lenOfFile:
            data = connection.recv(1024)
            total = total + len(data)
            for client in self.rooms[room_id]:
                if client != connection:
                    try: 
                        client.send(data)
                        # time.sleep(0.1)
                    except:
                        client.close()
                        self.remove(client, room_id)
        print("Sent")



    def broadcast(self, message_to_send, connection, room_id):
        for client in self.rooms[room_id]:
            if client != connection:
                try:
                    client.send(message_to_send.encode())
                except:
                    client.close()
                    self.remove(client, room_id)

    
    def remove(self, connection, room_id):
        if connection in self.rooms[room_id]:
            self.rooms[room_id].remove(connection)


if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345

    s = Server()
    s.accept_connections(ip_address, port)
