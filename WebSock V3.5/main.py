import sys, os, pathlib
sys.path.append(os.path.join(pathlib.Path(__file__).parent, "WebApplication\\MiddleWare"))
from .WebApplication.MiddleWare.console import InteractiveConsole

# WEBSOCK V3.5 ( by Atiya Sameh Alkhodari )

# —> cookies-based authentication system. session lifespan authenticatoin.
# —> supports multiple encryption algorithms [Hashing, Symmetric, Asymmetric].
# —> straightforward SSL/TLS certificates & private keys loading.
# —> easy CSRF tokens embeding and error catching.
# —> [STILL UNDER DEVELOPMENT] asynchronuous functions and scalability support.

# hit run and type the command "RunServer"!
# follow the link the server will provide you with

if __name__ == '__main__':
    InteractiveConsole()
