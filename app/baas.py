from abc import ABC, abstractmethod

class Baas(ABC):
    @abstractmethod
    def create_user(self, name):
        pass
    def get_user(self, id):
        pass
    def delete_user(self, id):
        pass