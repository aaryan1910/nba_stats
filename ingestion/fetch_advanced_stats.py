import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from io import StringIO

def fetch_advanced_stats(season="2026"):
    print(f"Fetching advanced stats from Basketball Reference...")
    
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_advanced.html"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "advanced"})
    
    df = pd.read_html(StringIO(str(table)))[0]
    
    # Drop duplicate header rows BR inserts
    df = df[df["Player"] != "Player"]
    
    # Keep only columns we need
    columns = ["Player", "Team", "G", "PER", "TS%", "USG%", "OWS", "DWS", "WS", "WS/48", "OBPM", "DBPM", "BPM", "VORP"]
    df = df[columns]

    # Rename for consistency
    df = df.rename(columns={"Player": "player_name", "Team": "team"})
    
    # Convert numeric columns
    numeric_cols = ["PER", "TS%", "USG%", "OWS", "DWS", "WS", "WS/48", "OBPM", "DBPM", "BPM", "VORP"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    
    # Add metadata
    df["season"] = "2025-26"
    df["ingested_at"] = datetime.utcnow().isoformat()
    
    print(f"Fetched {len(df)} player records")
    return df

if __name__ == "__main__":
    df = fetch_advanced_stats()
    print(df.head())
    print(f"Shape: {df.shape}")