import warnings
from .engine.auxknow import AuxKnow, AuxKnowSession
from .engine.auxknow_config import AuxKnowConfig
from .common.models import AuxKnowAnswer

warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings:",
    category=UserWarning,
    module="pydantic.main",
)

__version__ = "0.0.15"
__all__ = ["AuxKnow", "AuxKnowConfig", "AuxKnowAnswer", "AuxKnowSession"]
