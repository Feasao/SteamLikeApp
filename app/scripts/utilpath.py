import os
import sys

def get_data_path(filename):
    if getattr(sys, 'frozen', False):
        base = os.path.join(os.environ["APPDATA"], "SteamLike")
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, filename)