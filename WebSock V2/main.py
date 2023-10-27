import sys, os, pathlib
sys.path.append(os.path.join(pathlib.Path(__file__).parent, "WebApplication\\MiddleWare"))
from console import InteractiveConsole

# WEBSOCK V2 ( by Atiya Sameh Alkhodari )

# cookies-based authentication system. session lifespan authenticatoin.
# multiple encryption algorithms [Hashing, Symmetric, Asymmetric].
# straightforward SSL/TLS certificates & private keys loading.

# 1 TODO  embeding CSRF tokens.
# 4 FIXME CharField choices.
# 5 TODO  retreive previous database load after implementing UpdateSchema.
# 7 FIXME use proper passwords management [django documentation].
# * proper asynchronuous functions and scalability.

# hit run and type the command "RunServer"!
# follow the link the the server will provide you with

if __name__ == '__main__':
    InteractiveConsole()
