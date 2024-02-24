import requests

class Convex: 
    def __init__ (self, base_url):
        self.url = base_url
    
    def create_user(self, name):
        user_url = self.url + "/users"
        response = requests.post(user_url, json={"name": name})
        return response.json()
    
    def get_user(self, id):
        user_url = self.url + f"/users/{id}"
        response = requests.get(user_url)
        return response.json()
    
    def delete_user(self, id):
        user_url = self.url + f"/users/{id}"
        
        response = requests.delete(user_url)
        return response.status_code

