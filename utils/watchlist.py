import pandas as pd
import os

FILE = "watchlist.csv"

def save_watchlist(entry):
    df = pd.DataFrame([entry])

    if os.path.exists(FILE):
        old = pd.read_csv(FILE)
        df = pd.concat([old, df], ignore_index=True)

    df.to_csv(FILE, index=False)

def load_watchlist():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame()