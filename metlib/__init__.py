name = "metlib"
help = 'help(metlib.functions)'
help = 'help(metlib.flib)'
from . import flib
from .functions import cdiff
from .functions import relative_vorticity
from .functions import absolute_vorticity
from .functions import divergence
from .functions import advection
from .functions import potential_temperature
from .functions import potential_vorticity
__version__ = '0.0.1.1'
