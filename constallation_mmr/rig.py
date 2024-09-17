from typing import Optional, List
import requests
import threading
import time

class MRRAuthenticationError(Exception):
    """Custom exception for authentication errors in Mining Rig Rentals API."""
    def __init__(self, message="API key and secret key are required for this operation"):
        self.message = message
        super().__init__(self.message)


class Rig:
    def __init__(self, rig_id: int, rig_refresh_rate: int = 5, mmr_api_key: str = None, mmr_api_secret: str = None):
        """
        The Rig class provides an OOP-based interface for fetching rig information from the API.
        :param rig_id: The ID of the rig to query
        :param rig_refresh_rate: controls the interval of data requerying
        :param mmr_api_key: API key for authenticated requests
        :param mmr_api_secret: API secret for authenticated requests
        """
        self.rig_id = rig_id
        self._rig_refresh_rate = rig_refresh_rate
        self._mmr_api_key = mmr_api_key
        self._mmr_api_secret = mmr_api_secret
        self._data = {}
        self._stop_thread = False
        self._fetch_rig_data()
        self._start_refresh_thread()

    def _fetch_rig_data(self):
        url = f"https://www.miningrigrentals.com/api/v2/rig/{self.rig_id}"

        try:
            response = requests.get(url)
            if response.status_code == 200 and response.json().get("success"):
                self._data = response.json().get("data")
            else:
                raise Exception(f"Failed to fetch rig data: {response.text}")
        except Exception as e:
            print(f"Error while fetching rig data: {e}")

    def _start_refresh_thread(self):
        self._thread = threading.Thread(target=self._refresh_data_loop, daemon=True)
        self._thread.start()

    def _refresh_data_loop(self):
        while not self._stop_thread:
            time.sleep(self._rig_refresh_rate)
            self._fetch_rig_data()

    def stop_refresh(self):
        self._stop_thread = True
        if self._thread.is_alive():
            self._thread.join()

    def __del__(self):
        """
        Destructor method that stops the thread when the object is destroyed.
        """
        self.stop_refresh()

    def delete_rig(self):
        """
        Deletes the rig from the MiningRigRentals service.
        This method requires valid API key and secret.
        """
        if not self._mmr_api_key or not self._mmr_api_secret:
            raise MRRAuthenticationError()

        url = f"https://www.miningrigrentals.com/api/v2/rig/{self.rig_id}/delete"
        headers = {
            'x-api-key': self._mmr_api_key,
            'x-api-secret': self._mmr_api_secret
        }

        try:
            response = requests.delete(url, headers=headers)
            if response.status_code == 200 and response.json().get("success"):
                print(f"Rig {self.rig_id} successfully deleted.")
            else:
                raise Exception(f"Failed to delete rig: {response.text}")
        except Exception as e:
            print(f"Error while deleting rig: {e}")

    @property
    def id(self):
        return self._data.get("id")

    @property
    def name(self):
        return self._data.get("name")

    @property
    def owner(self):
        return self._data.get("owner")

    @property
    def type(self):
        return self._data.get("type")

    @property
    def status(self):
        return self._data.get("status")

    @property
    def online(self):
        return self._data.get("online")

    @property
    def xnonce(self):
        return self._data.get("xnonce")

    @property
    def poolstatus(self):
        return self._data.get("poolstatus")

    @property
    def region(self):
        return self._data.get("region")

    @property
    def rpi(self):
        return self._data.get("rpi")

    @property
    def suggested_diff(self):
        return self._data.get("suggested_diff")

    @property
    def optimal_diff(self):
        return self._data.get("optimal_diff")

    @property
    def ndevices(self):
        return self._data.get("ndevices")

    @property
    def device_memory(self):
        return self._data.get("device_memory")

    @property
    def extensions(self):
        return self._data.get("extensions")

    @property
    def price(self):
        return self._data.get("price")

    @property
    def minhours(self):
        return self._data.get("minhours")

    @property
    def maxhours(self):
        return self._data.get("maxhours")

    @property
    def hashrate(self):
        return self._data.get("hashrate")

    @property
    def error_notice(self):
        return self._data.get("error_notice")

    @property
    def description(self):
        return self._data.get("description")

    @property
    def available_status(self):
        return self._data.get("available_status")

    @property
    def shorturl(self):
        return self._data.get("shorturl")

    @property
    def device_ram(self):
        return self._data.get("device_ram")

    @property
    def hours(self):
        return self._data.get("hours")

    @property
    def rented(self):
        return self._data.get("rented")



def fetch_rigs(
    rig_ids: List[int],
    rigs_refresh_rate: int = 5,
    mmr_api_key: Optional[str] = None,
    mmr_api_secret: Optional[str] = None
) -> List[Rig]:
    """
    Fetches multiple rigs and returns them as constallation_mmr.Rig objects.
    :param rig_ids: A list of rigs to query.
    :param rigs_refresh_rate: The interval at which the rigs autorefresh.
    :param mmr_api_key: Optional API key for authenticated requests.
    :param mmr_api_secret: Optional API secret for authenticated requests.
    :return: list of Rig objects.
    """
    rigs = []
    for rig_id in rig_ids:
        _rig = Rig(rig_id, rigs_refresh_rate, mmr_api_key, mmr_api_secret)
        rigs.append(_rig)

    return rigs

def fetch_rig(
    rig_id: int,
    rigs_refresh_rate: int = 5,
    mmr_api_key: Optional[str] = None,
    mmr_api_secret: Optional[str] = None
) -> Rig:
    """
    Fetches a single rig and returns it as a constallation_mmr.Rig object.
    :param rig_id: The ID of the rig to query.
    :param rigs_refresh_rate: The interval at which the rigs autorefresh.
    :param mmr_api_key: Optional API key for authenticated requests.
    :param mmr_api_secret: Optional API secret for authenticated requests.
    :return: constallation_mmr.Rig object.
    """
    return Rig(rig_id, rigs_refresh_rate, mmr_api_key, mmr_api_secret)