import sys, asyncio
sys.path.append(r"C:\Users\skhodari\Desktop\ATTYA\WebSock\WebApplication\MiddleWare")
from async_server import server_runner

if __name__ == '__main__':
    server = asyncio.run(server_runner())
