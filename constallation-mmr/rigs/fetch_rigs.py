from rig import Rig

def fetch_rigs(rig_ids:list[int], rigs_refresh_rate:int=5):
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