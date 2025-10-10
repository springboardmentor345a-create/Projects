import pandas as pd


def safe_cast_int(x, default=0):
   try:
     return int(x)
   except Exception:
     return default