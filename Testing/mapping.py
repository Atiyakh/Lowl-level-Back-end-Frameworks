from InfraWeb.MiddleWare.Routing import Mapping, ExtractApplicationsMapping
from settings import INSTALLED_APPLICATIONS

URLMapping = Mapping()
URLMapping.Structure(
    *ExtractApplicationsMapping(INSTALLED_APPLICATIONS),
)
