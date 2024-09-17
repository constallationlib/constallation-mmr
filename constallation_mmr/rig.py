import requests
import threading
import time


class Rig:
    def __init__(self, rig_id: int, rig_refresh_rate: int = 5):
        """
        The Rig class provides an OOP-based interface for fetching rig information from the API.
        :param rig_id: The ID of the rig to query
        :param rig_refresh_rate: controls the interval of data requerying
        """

        self.rig_id = rig_id
        self._rig_refresh_rate = rig_refresh_rate
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



def fetch_rigs(rig_ids:list[int], rigs_refresh_rate:int=5) -> list[Rig]:
    """
    Fetches multiple rigs and returns them as constallation_mmr.Rig objects.
    :param rig_ids: A list of rigs to query.
    :param rigs_refresh_rate: The interval of which the rigs autorefresh
    :return: list of Rigs
    """
    rigs = []
    for _ in rig_ids:
        _rig = Rig(_, rigs_refresh_rate)
        rigs.append(_rig)

    return rigs

def create_rig(name, server, description=None, status=None, price_btc_enabled=None, price_btc_price=None,
               price_btc_autoprice=None, price_btc_minimum=None, price_btc_modifier=None, price_ltc_enabled=None,
               price_ltc_price=None, price_ltc_autoprice=None, price_eth_enabled=None, price_eth_price=None,
               price_eth_autoprice=None, price_doge_enabled=None, price_doge_price=None, price_doge_autoprice=None,
               price_type="mh", minhours=None, maxhours=None, extensions=None, hash_hash=None, hash_type="mh",
               suggested_diff=None, ndevices=None):
    """
    Creates a rig using the specified parameters and returns a Rig object.
    """
    # Construct the payload
    payload = {
        "name": name,
        "server": server,
        "price": {
            "type": price_type,
            "btc": {
                "enabled": price_btc_enabled,
                "price": price_btc_price,
                "autoprice": price_btc_autoprice,
                "minimum": price_btc_minimum,
                "modifier": price_btc_modifier
            },
            "ltc": {
                "enabled": price_ltc_enabled,
                "price": price_ltc_price,
                "autoprice": price_ltc_autoprice
            },
            "eth": {
                "enabled": price_eth_enabled,
                "price": price_eth_price,
                "autoprice": price_eth_autoprice
            },
            "doge": {
                "enabled": price_doge_enabled,
                "price": price_doge_price,
                "autoprice": price_doge_autoprice
            }
        },
        "hash": {
            "hash": hash_hash,
            "type": hash_type
        },
        "minhours": minhours,
        "maxhours": maxhours,
        "extensions": extensions,
        "type": hash_type,
        "status": status,
        "description": description,
        "suggested_diff": suggested_diff,
        "ndevices": ndevices
    }

    # Remove None values from payload
    payload = {k: v for k, v in payload.items() if v is not None}
    payload["price"] = {k: v for k, v in payload["price"].items() if v is not None}
    payload["hash"] = {k: v for k, v in payload["hash"].items() if v is not None}

    url = "https://www.miningrigrentals.com/api/v2/rig/create"

    try:
        response = requests.post(url, json=payload)
        response_data = response.json()

        if response.status_code == 200 and response_data.get("success"):
            rig_data = response_data.get("data")
            return Rig(rig_id=rig_data["id"], data=rig_data)
        else:
            raise Exception(f"Failed to create rig: {response.text}")

    except Exception as e:
        print(f"Error while creating rig: {e}")