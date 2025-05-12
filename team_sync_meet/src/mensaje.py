import socket
import threading

class Mensaje:
    def __init__(self, username, host='127.0.0.1', port=55555):
        self.username = username
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode("utf-8")

                if message == "@username":
                    self.client.send(self.username.encode("utf-8"))
                else:
                    print(message)
            except:
                print("An error occurred")
                self.client.close()
                break

    def write_messages(self):
        while True:
            message = f"{self.username}: {input('')}"
            self.client.send(message.encode("utf-8"))

    def start(self):
        recieve_thread = threading.Thread(target=self.receive_messages)
        recieve_thread.start()

        write_thread = threading.Thread(target=self.write_messages)
        write_thread.start()