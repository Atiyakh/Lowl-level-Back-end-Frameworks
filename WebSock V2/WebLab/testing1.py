from socket import (
	gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM)
import traceback, time

IMG_path = r"C:\Users\skhodari\Desktop\favicon.jpg"

file = open(IMG_path, 'rb')
IMG_Bytes = file.read(); file.close()

IMG_Pkt = (b"HTTP/1.1 200 OK\n\r"+
	f"content-length: {IMG_Bytes.__len__()}\n\r".encode('utf-8')+
	IMG_Bytes
)

HOST = (gethostbyname(gethostname()), 80)
webserver_socket = socket(AF_INET, SOCK_STREAM)
webserver_socket.bind(HOST)

webserver_socket.listen(5)

while True:
	try:
		conn, addr = webserver_socket.accept()
		print(f"New Connection - {addr[0]}:{addr[1]} - {time.ctime()}")
		request = conn.recv(1024)
		print(request)
		conn.sendall(IMG_Pkt)
		conn.close()
	except:
		traceback.print_exc()
