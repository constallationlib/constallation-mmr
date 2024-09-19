import requests
from rig import Rig

class RigGroup:
    def __init__(self, api_key: str, api_secret: str, rig_group_id: int = None, rig_group_name: str = "",
                 rig_group_enabled: bool = False, rig_group_rental_limit: int = 1) -> None:
        self._rig_group_id = rig_group_id
        self._rig_group_name = rig_group_name
        self._enabled = rig_group_enabled
        self._rental_limit = rig_group_rental_limit
        self._api_key = api_key
        self._api_secret = api_secret

        # If rig_group_id is not provided, create a new rig group, otherwise get existing one
        if self._rig_group_id is None and len(rig_group_name) > 0:
            self._create()
        else:
            self._get_rig_group()

    def _get_rig_group(self):
        """ Fetches the rig group details from the API and updates instance attributes """
        if self._rig_group_id is None:
            raise ValueError("rig_group_id is required to fetch rig group details")

        url = f"https://www.miningrigrentals.com/api/v2/riggroup/{self._rig_group_id}"
        headers = {
            'Authorization': f'Bearer {self._api_key}:{self._api_secret}'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                rig_group_data = data['data']
                self._rig_group_id = int(rig_group_data['id'])
                self._rig_group_name = rig_group_data['name']
                self._enabled = bool(int(rig_group_data['enabled']))
                self._rental_limit = int(rig_group_data['rental_limit'])
            else:
                raise Exception(f"Failed to fetch rig group: {data}")
        else:
            raise Exception(f"Error fetching rig group: {response.status_code} - {response.text}")

    def _create(self):
        """ Sends a PUT request to create a new rig group on the API """
        url = "https://www.miningrigrentals.com/api/v2/riggroup"
        headers = {
            'Authorization': f'Bearer {self._api_key}:{self._api_secret}',
            'Content-Type': 'application/json'
        }
        payload = {
            "name": self._rig_group_name,
            "enabled": int(self._enabled),  # Assuming 1 for True, 0 for False
            "rental_limit": self._rental_limit
        }

        response = requests.put(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                rig_group_data = data['data']
                self._rig_group_id = int(rig_group_data['id'])
                self._rig_group_name = rig_group_data['name']
                self._enabled = bool(int(rig_group_data['enabled']))
                self._rental_limit = int(rig_group_data['rental_limit'])
            else:
                raise Exception(f"Failed to create rig group: {data}")
        else:
            raise Exception(f"Error creating rig group: {response.status_code} - {response.text}")

    def delete(self):
        """ Sends a DELETE request to remove the rig group from the API """
        if self._rig_group_id is None:
            raise ValueError("rig_group_id is required to delete a rig group")

        url = f"https://www.miningrigrentals.com/api/v2/riggroup/{self._rig_group_id}"
        headers = {
            'Authorization': f'Bearer {self._api_key}:{self._api_secret}',
            'Content-Type': 'application/json'
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data['data'].get('deleted') == True:
                return True
            else:
                raise Exception(f"Failed to delete rig group: {data}")
        else:
            raise Exception(f"Error deleting rig group: {response.status_code} - {response.text}")