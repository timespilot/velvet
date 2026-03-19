import sys

from . import VelvetLustre


VelvetLustre(*[part.strip() for part in (sys.argv[1] if len(sys.argv) > 1 else "P1,P2").split(",")]).openPrompt()