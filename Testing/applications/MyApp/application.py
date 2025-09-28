from importlib.machinery import SourceFileLoader
import os, pathlib

class Application:
    def __init__(self):
        __file__ = 'c:/Users/skhodari/Desktop/Attya/ATTYA/applications/MyApp/application.py'
        self._application_path = __file__
        self.application_path = pathlib.Path(__file__).parent
        self.views_path = os.path.join(self.application_path, 'views.py')
        self.views = SourceFileLoader('views', self.views_path).load_module()
        self.models_path = os.path.join(self.application_path, 'models.py')
        self.models = SourceFileLoader('models', self.models_path).load_module()
        self.urls_path = os.path.join(self.application_path, 'urls.py')
        self.urls = SourceFileLoader('urls', self.urls_path).load_module()
        self.mapping = self.urls.URLMapping.raw_urls
        self.assets_path = os.path.join(self.application_path, 'assets')
        self.static_path = os.path.join(self.assets_path, 'static')
        self.media_path = os.path.join(self.assets_path, 'media')
        self.database_schemas_path = os.path.join(self.assets_path, 'database_schemas')
        self.sqlite3_path = os.path.join(self.application_path, 'sqlite3')
