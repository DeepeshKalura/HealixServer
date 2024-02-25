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

