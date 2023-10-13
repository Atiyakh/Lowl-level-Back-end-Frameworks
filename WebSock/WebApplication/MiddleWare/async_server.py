from socket import *
from request_processor import request_processor_
import asyncio, traceback

class AsyncServer:
    async def request_handler(self, reader, writer):
        try:
            request_content = await reader.read(1024)
            print(request_content)
            response = request_processor_(request_content).response
            writer.write(response)
            await writer.drain()
            writer.close()
        except:
            traceback.print_exc()

    async def start_server(self):
        self.host = gethostbyname(gethostname())
        self.port = 8080
        self.server_stream = await asyncio.start_server(
        self.request_handler, self.host, self.port)
        print(f"[WebSock] web server initiated - http://{gethostbyname(gethostname())}:{self.port}/")
        await self.server_stream.serve_forever()

async def server_runner():
    server = AsyncServer()
    await server.start_server()
