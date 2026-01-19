from pathlib import Path

from environs import Env


env = Env()

ROLE = env.str("ROLE", default="local")
BASE_PATH = Path.cwd().absolute()

if ROLE == "local":
    env.read_env(path=str(BASE_PATH / ".env"))
