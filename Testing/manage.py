from InfraWeb.MiddleWare import Console
from settings import INSTALLED_APPLICATIONS
from async_server import server_runner

# InfraWeb 2.0

# Hit run and type the command "RunServer"!
# Follow the link the server will provide you with

if __name__ == '__main__':
    Console.InteractiveConsole(
        server_runner=server_runner,
        installed_apps=INSTALLED_APPLICATIONS
    )
