# index.py - Entry point for the Rocket Tracker application
# This script loads environment variables, sets up the server configuration, and starts the server.
#                    /^\
#                   /   \
#                  /     \
#                 / _   _ \
#                (  o   o  )  
#                _\   ^   /_
#              .'  \  |  /  `.
#             /  .-`-^-'-.  \
#            /_.-'         '-._\
#             /               \
#            /  _  _  _  _  _  \
#           / __/ \/ \/ \/ \__ \
#           \/  |\/\/\/\/\/|  \/
#              _|            |_
#             /  \          /  \
#            /    \________/    \
#            \__________________/
#
# __    __  __     ___    __  __   ___    __  ___    _____    __   _____        __   __  _____  _      __  __    
#/ / /\ \ \/__\   / __\  /__\/ /  /___\/\ \ \/ _ \   \_   \/\ \ \ /__   \/\  /\/__\ / _\/__   \/_\    /__\/ _\   
#\ \/  \/ /_\    /__\// /_\ / /  //  //  \/ / /_\/    / /\/  \/ /   / /\/ /_/ /_\   \ \   / /\//_\\  / \//\ \    
# \  /\  //__   / \/  \//__/ /__/ \_// /\  / /_\\  /\/ /_/ /\  /   / / / __  //__   _\ \ / / /  _  \/ _  \_\ \_  
#  \/  \/\__/   \_____/\__/\____|___/\_\ \/\____/  \____/\_\ \/    \/  \/ /_/\__/   \__/ \/  \_/ \_/\/ \_/\__(_) 
                                                                                                               





import os, subprocess
from typing import Any
from dotenv import load_dotenv
load_dotenv()
def required_env(name: str) -> Any:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Environment variable '{name}' is required but not set.")
    return value

port = int(required_env("PORT"))
dev  = required_env("DEV")

print(port, dev, os.getcwd())
try:
    subprocess.run([
        "uvicorn", "src.server:app",
        *(["--reload"] if dev else []),
        "--host", "0.0.0.0",
        "--port", str(port)
    ], cwd=os.getcwd())
except KeyboardInterrupt:
    print("Server stopped by user.")
except Exception as e:
    print(f"An error occurred while starting the server: {e}")
    raise
