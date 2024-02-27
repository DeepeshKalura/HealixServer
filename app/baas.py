from abc import ABC, abstractmethod

class Baas(ABC):
    @abstractmethod
    def create_user(self, name):
        pass
    def get_user(self, id):
        pass
    def delete_user(self, id):
        pass
    def create_session(self, user_id):
        pass

    def create_thread(self, session_id, message, response, sentiment_compound):
        pass
    def session_completed(self, session_id):
        pass
