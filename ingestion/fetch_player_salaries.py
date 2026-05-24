import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from io import StringIO

def fetch_player_salaries(season="2025-26"):
    print(f"Fetching NBA player salaries from Basketball Reference...")
    
    url = "https://www.basketball-reference.com/contracts/players.html"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "player-contracts"})
    df = pd.read_html(StringIO(str(table)))[0]
    
    # Flatten multi-level columns
    df.columns = ["rank", "player_name", "team", "salary_2025_26", "salary_2026_27", 
                  "salary_2027_28", "salary_2028_29", "salary_2029_30", "salary_2030_31", "guaranteed"]
    
    # Drop header repeat rows
    df = df[df["player_name"] != "Player"]
    df = df[df["player_name"].notna()]
    
    # Keep only current season salary
    df = df[["player_name", "team", "salary_2025_26"]]
    
    # Clean salary - remove $ and commas
    df["salary"] = df["salary_2025_26"].str.replace("$", "", regex=False)
    df["salary"] = df["salary"].str.replace(",", "", regex=False)
    df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
    df = df.drop(columns=["salary_2025_26"])
    
    # Drop players with no salary data
    df = df[df["salary"].notna()]
    
    # Add metadata
    df["season"] = season
    df["ingested_at"] = datetime.utcnow().isoformat()
    
    print(f"Fetched {len(df)} player salaries")
    return df

if __name__ == "__main__":
    df = fetch_player_salaries()
    print(df.head(10))
    print(f"Shape: {df.shape}")