from InfraWeb.MiddleWare.request_processor import request_processor_
from socket import gethostbyname, gethostname
import traceback, pathlib, os, asyncio, ssl
import mapping

async def receive_request(reader, chunk_size=8192):
    headers = b""; body = b""
    while True:
        if b"\r\n\r\n" in headers:  # Header-body separator detected
            headers, body = headers.split(b"\r\n\r\n", 1)
            if b"content-length: " in headers.lower():
                # locating content-length
                indx1 = headers.lower().find(b"content-length: ") + 16
                indx2 = headers[indx1:].find(b"\r\n") + indx1
                content_length_str = headers[indx1: indx2].strip()
                try: content_length = int(content_length_str)
                except ValueError:
                    raise ValueError(f"Invalid content-length: {content_length_str}")
                # loopin throu for the body
                while len(body) < content_length:
                    unsent_body_length = content_length - len(body)
                    buffer_size = min(unsent_body_length, 65536)  # Optimize buffer size
                    chunk = await reader.read(buffer_size)
                    if not chunk:
                        raise ConnectionError("Connection closed unexpectedly while reading the body.")
                    body += chunk
                return headers, body
            else: return headers, body
        else:
            chunk = await reader.read(chunk_size)
            if not chunk:  # If the connection is closed unexpectedly
                if b"\r\n\r\n" not in headers or "content-length" in headers:
                    print("[InfraWeb] Connection closed unexpectedly while reading headers.")
                    return None
            headers += chunk

class AsyncServer:
    async def request_handler(self, reader, writer):
        try:
            self.far_host_peername = writer.get_extra_info('peername')
            request = await receive_request(reader)
            if request:
                headers, body = request
                generated_response = await request_processor_(headers, body, self.far_host_peername, mapping)
                if generated_response:
                    response = generated_response.response
                else:
                    response = b'HTTP/1.1 404 Not Found\n\r\n\r404 Page Not Found'
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
                self.certificatePath = os.path.join(pathlib.Path(__file__).parent, 'Certificates/ssl_tls_certificate.pem')
                self.privatKeyPath = os.path.join(pathlib.Path(__file__).parent, 'Certificates/server_private_key.pem')
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
            print(f"[InfraWeb] Web server initiated successfully - http://{gethostbyname(gethostname())}{(f":{self.port}" if self.port != 80 else '')}/")
            await self.server_stream.serve_forever()
        except OSError as e:
            if e.errno == 10048:
                print("[InfraWeb] Server is already running.")

async def server_runner(port, secure, installed_apps_):
    global installed_apps
    installed_apps = installed_apps_
    server = AsyncServer()
    server.set_port(port)
    server.set_secure(secure)
    await server.start_server()
