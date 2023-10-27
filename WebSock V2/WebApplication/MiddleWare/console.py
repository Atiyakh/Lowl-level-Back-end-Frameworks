from async_server import server_runner
from MiddleWare.Database.models_formater import ModelsParser
from MiddleWare.Database.Models import UpdateSchema
import asyncio, threading, traceback
import os, pathlib

def Execution(code):
    exec(code, globals())

def RunServer(port, secure=False):
    asyncio.run(server_runner(port, secure))

def InteractiveConsole():
    print('[WebSock] Interactive Console Activated...')
    while True:
        command = input()
        if command == "SaveSchema":
            try: ModelsParser()
            except:
                traceback.print_exc()
                raise ValueError(
                    "[WebSock] Failed to save your schema."
                )
        elif command == "UpdateSchema":
            try: UpdateSchema()
            except:
                traceback.print_exc()
                raise ValueError(
                    "[WebSock] Failed to update the database schema."
                )
        elif command.find("RunServer") == 0:
            if len(command) > 11:
                port = int(command[9:].strip())
            else: port = 8888
            try: threading.Thread(target=RunServer, args=(port,)).start()
            except:
                raise ValueError(
                    "[WebSock] Unable to run the the server."
                )
        elif command.find("RunSecure") == 0:
            if len(command) > 11:
                port = int(command[9:].strip())
            else: port = 8888
            try: threading.Thread(target=RunServer, args=(port, True)).start()
            except:
                raise ValueError(
                    "[WebSock] Unable to run the the server."
                )
        elif command.find("LoadCertificate") == 0:
            try:
                cert_path = command[15:].strip()
                cert_file = open(cert_path, 'rb')
                cert_content = cert_file.read()
                cert_file.close()
                inner_file = open(os.path.join(pathlib.Path(__file__).parent, 'Certificates\\ssl_tls_certificate.pem'), 'wb')
                inner_file.write(cert_content)
                inner_file.close()
            except:
                traceback.print_exc()
                print('[WebSock] Unable to load the certificate.')
        elif command.find("LoadCryptoKey") == 0:
            try:
                key_path = command[13:].strip()
                key_file = open(key_path, 'rb')
                key_content = key_file.read()
                key_file.close()
                inner_file = open(os.path.join(pathlib.Path(__file__).parent, 'Certificates\\cryptographic_key.pem'), 'wb')
                inner_file.write(key_content)
                inner_file.close()
            except:
                traceback.print_exc()
                print('[WebSock] Unable to load the certificate.')
        else:
            threading.Thread(target=Execution, args=(command,)).start()
