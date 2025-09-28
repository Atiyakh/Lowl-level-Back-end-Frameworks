from importlib.machinery import SourceFileLoader
import os, pathlib

application = SourceFileLoader(
    'application',
    os.path.join(pathlib.Path(__file__).parent, 'application.py')
).load_module()

MyAppApp = application.Application()
