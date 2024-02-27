import requests
from baas import Baas

class Convex(Baas): 
    """
    A class representing a Convex API client.

    Args:
        base_url (str): The base URL of the Convex API.

    Attributes:
        url (str): The complete URL of the Convex API.

    Methods:
        create_user: Creates a new user.
        get_user: Retrieves user information.
        delete_user: Deletes a user.
    """

    def __init__ (self, base_url):
        self.url = base_url
    
    def create_user(self, name):
        """
        Creates a new user.

        Args:
            name (str): The name of the user.

        Returns:
            dict: The JSON response containing the user information.
        """
        user_url = self.url + "/users"
        response = requests.post(user_url, json={"name": name})
        return response.json()
    
    def get_user(self, id):
        """
        Retrieves user information.

        Args:
            id (int): The ID of the user.

        Returns:
            dict: The JSON response containing the user information.
        """
        user_url = self.url + f"/users/{id}"
        response = requests.get(user_url)
        return response.json()
    
    def delete_user(self, id):
        """
        Deletes a user.

        Args:
            id (int): The ID of the user.

        Returns:
            int: The status code of the delete request.
        """
        user_url = self.url + f"/users/{id}"
        response = requests.delete(user_url)
        return response.status_code
    

    def create_session(self, user_id):
        """
        Creates a new session.

        Args:
            token (str): The token of the user.

        Returns:
            dict: The JSON response containing the session information.
        """
        session_url = self.url + f"/sessions"
        response = requests.post(session_url, json={"id": user_id})
        return response.json()
    

    def create_thread(self, session_id, message, response, sentiment_compound):
        thread_url = self.url + f"/sessions/threads/{session_id}"
        response = requests.post(thread_url, json={"message": message, "response": response, "sentiment_compound": sentiment_compound})
        print("I reached here at least")
        print(response.text)
        update_url = self.url + f"/sessions/{session_id}"
        requests.patch(update_url)
        return response.json()
        

    def session_completed(self, session_id):
        thread_url = self.url + f"/sessions/threads/{session_id}"
        response = requests.patch(thread_url)
        
    
    


convex = Convex("http://localhost:3001")

id = (convex.create_user("John Doe"))

print(id)

user = convex.get_user(id["id"])
print(user)

res = convex.create_session(user_id=id["id"])
print(res)


thread_1 = convex.create_thread(session_id=res["id"], message="Niklo Bol ra hu mey", response="terko", sentiment_compound="0.8")
print(thread_1)


thread2 = convex.create_thread(session_id=res["id"], message="Daka ho yrr merko dekne de", response="sabko dek lega mey", sentiment_compound="0.9")
print(thread2)

thread3 = convex.create_thread(session_id=res["id"], message="Kya bol raha hai", response="kuch nahi", sentiment_compound="0.1")
print(thread3)

thread4 = convex.create_thread(session_id=res["id"], message="Kyu bol ra hi", response="kuch tho", sentiment_compound="0.6")
print(thread4)

convex.session_completed(res["id"])


status_code = convex.delete_user(id["id"])
assert status_code == 200

print("End of the program")

