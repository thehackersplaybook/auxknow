import warnings
from .engine.auxknow import AuxKnow, AuxKnowSession
from .engine.auxknow_config import AuxKnowConfig
from .common.models import AuxKnowAnswer
from .version import AuxKnowVersion

warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings:",
    category=UserWarning,
    module="pydantic.main",
)

__version__ = AuxKnowVersion.CURRENT_VERSION
__all__ = ["AuxKnow", "AuxKnowConfig", "AuxKnowAnswer", "AuxKnowSession"]
