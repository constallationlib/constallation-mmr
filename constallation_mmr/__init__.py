__name__ = "constallation_mmr"
__version__ = "1.1.0"
__author__ = "Coulter Stutz"
__email__ = "coulterstutz@constallation.wiki"
from .rig import *
from .riggroup import *
__all__ = ["Rig", "fetch_rigs", "fetch_rig", "RigGroup"]