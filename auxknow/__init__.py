import warnings
from .auxknow import AuxKnow

warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings:",
    category=UserWarning,
    module="pydantic.main",
)

__version__ = "0.0.1"
__all__ = ["AuxKnow"]
