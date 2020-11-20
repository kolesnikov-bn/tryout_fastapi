import os
from .base import *

env_name = os.getenv("ENV_NAME", "local")

if env_name == "production":
    from .prod import *
else:
    from .local import *
