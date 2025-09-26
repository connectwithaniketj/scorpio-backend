import requests
from ..config import settings

class ScorpioClient:
    def __init__(self, base_url: str = settings.scorpio_base_url):
        self.base_url = base_url.rstrip("/")
        print(self.base_url)

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