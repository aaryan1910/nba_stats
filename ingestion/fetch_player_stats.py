import time
import json
import os
from datetime import datetime
from nba_api.stats.endpoints import leaguedashplayerstats
from dotenv import load_dotenv

load_dotenv()

def fetch_player_stats(season="2025-26"):
    print(f"Fetching NBA player stats for {season} season...")
    
    # Basic box score stats
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed="PerGame",
        measure_type_detailed_defense="Base"
    )

    
    df = stats.get_data_frames()[0]
    
    # Keep only the columns we need
    columns = [
        "PLAYER_ID", "PLAYER_NAME", "TEAM_ABBREVIATION",
        "GP", "MIN", "PTS", "REB", "AST", "STL", "BLK",
        "FG_PCT", "FG3_PCT", "FT_PCT", "TOV", "PLUS_MINUS"
    ]
    
    df = df[columns]
    
    # Add metadata
    df["season"] = season
    df["ingested_at"] = datetime.utcnow().isoformat()
    
    print(f"Fetched {len(df)} players")
    return df

if __name__ == "__main__":
    df = fetch_player_stats()
    print(df.head())
    print(f"Shape: {df.shape}")