from socket import *
from request_processor import request_processor_
import traceback, views, pathlib, os
import asyncio, ssl

# asynchronous HTTP-like low-level Server
# HTTPS-supported server. straightforward
# certificates loading. default port 8888
 
class AsyncServer:
    async def request_handler(self, reader, writer):
        try:
            self.far_host_peername = writer.get_extra_info('peername')
            request_content = await reader.read(65_000)
            generated_response = await request_processor_(request_content, self.far_host_peername, views)
            if generated_response:
                response = generated_response.response
            else:
                response = b'HTTP/1.1 404 Not Found\n\r\n\r404 Page Not Found\n\r\n\r'
            writer.write(response)
            await writer.drain()
            writer.close()
        except:
            traceback.print_exc()
    def set_port(self, port):
        self.port = port
    def set_secure(self, secure):
        self.secure = secure
    async def start_server(self):
        try:
            self.host = gethostbyname(gethostname())
            if self.secure:
                self.certificatePath = os.path.join(pathlib.Path(__file__).parent, 'Certificates\\ssl_tls_certificate.pem')
                self.privatKeyPath = os.path.join(pathlib.Path(__file__).parent, 'Certificates\\server_private_key.pem')
                self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                self.context.load_cert_chain(
                    certfile=self.certificatePath, 
                    keyfile=self.privatKeyPath
                )
                self.server_stream = await asyncio.start_server(
                    self.request_handler, self.host,
                    self.port, ssl=self.context
                )
            else:
                self.server_stream = await asyncio.start_server(
                    self.request_handler, self.host, self.port
                )
            print(f"[WebSock] Web serve initiated successfully - http://{gethostbyname(gethostname())}:{self.port}/")
            await self.server_stream.serve_forever()
        except OSError as e:
            if e.errno == 10048:
                print("[WebSock] Server is already running.")

async def server_runner(port, secure):
    server = AsyncServer()
    server.set_port(port)
    server.set_secure(secure)
    await server.start_server()
