__all__ = ["OSC_M32", "OSC_PILOT", "NULL_TARGET", "get_target"]

from . import OSC_M32
from . import OSC_PILOT
from . import NULL_TARGET

def get_target( targetInfo ):
    match targetInfo["type"]:
        case "OSC_M32": targetInstance = OSC_M32.OSC_M32( targetInfo )
        case "OSC_PILOT": targetInstance = OSC_PILOT.OSC_PILOT( targetInfo )
        case "NULL_TARGET": targetInstance = NULL_TARGET.NULL_TARGET( targetInfo )
        case _: targetInstance = NULL_TARGET.NULL_TARGET( targetInfo )
    return targetInstance
