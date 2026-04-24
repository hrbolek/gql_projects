
import dataclasses
import strawberry

from ..Dataloaders import LoaderMap
from ..ServiceDefinitions.ServiceContext import ServiceContext

def createContext():
    return {}

class ApplicationInfo(strawberry.Info):   
    @property
    def loaders(self) -> LoaderMap:
        return self.context["loaders"]
    
    @property
    def request(self):
        return self.context["request"]
    
    @property
    def user(self):
        return self.context["user"]
    
    @property
    def ServiceCtx(self):
        result = self.context.get("ServiceCtx")
        if result is None:
            result = self.context["ServiceCtx"] = ServiceContext(
                loaders=self.loaders, 
                user=self.user,
                request=self.request
            )
        return result   