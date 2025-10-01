import requests
from ..config import settings

class ScorpioClient:
    def __init__(self, base_url: str = settings.scorpio_base_url, headers=None):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {"Accept": "application/ld+json"}
        #print(self.base_url)

    def get_entities(self):
        r = requests.get(f"{self.base_url}/entities/")
        r.raise_for_status()
        return r.json()

    def get_entity(self, entity_id: str):
        r = requests.get(f"{self.base_url}/entities/{entity_id}")
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()

    def get_entity_history(self, entity_id: str, attr: str = None):
        url = f"{self.base_url}/temporal/entities/{entity_id}"
        if attr:
            url += f"?attrs={attr}"
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    
    def get_entity_types(self):
            url = f"{self.base_url}/types"  # use the dedicated /types endpoint
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()

            # Extract the typeList
            type_list = data.get("typeList")
            
            # If it's a single string, wrap in list
            if isinstance(type_list, str):
                type_list = [type_list]

            return type_list if type_list else []
    
    def query_entities(self, params: dict = None, headers: dict = None):
        """
        Query entities from Scorpio.

        :param params: Dictionary of query parameters (e.g., type, attrs, q, georel, geometry, coordinates)
        :param headers: Optional dictionary of headers to use in the request
        :return: JSON list of entities
        """
        headers = headers or self.headers
        params = params or {}

        url = f"{self.base_url}/entities"
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        if response.status_code != 200:
            raise Exception(f"Scorpio query failed: {response.status_code} {response.text}")
        return response.json()
    
    def query_temporal_entity(self, entity_id, params=None):
        url = f"{self.base_url}/temporal/entities/{entity_id}"
        if params is None:
            params = {}
        # params["options"] = "temporalValues"
        res = requests.get(url, params=params)
        res.raise_for_status()
        return res.json()