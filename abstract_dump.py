from abc import ABC, abstractmethod 
  
class AbstractDump(ABC): 
  
    @abstractmethod
    def dump_apikeys(self, entries, package, version_code, version_name):
        pass
        
    @abstractmethod
    def dump_strings(self, entries):
        pass