import warnings
from .auxknow import AuxKnow, AuxKnowConfig, AuxKnowAnswer, AuxKnowSession

warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings:",
    category=UserWarning,
    module="pydantic.main",
)

__version__ = "0.0.8"
__all__ = ["AuxKnow", "AuxKnowConfig", "AuxKnowAnswer", "AuxKnowSession"]
