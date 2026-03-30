from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: Optional[float] = None
    target_danceability: Optional[float] = None
    target_tempo_bpm: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    print(f"Loading songs from {csv_path}...")
    songs = []
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against a user preference dictionary.

    Scoring recipe (all signals are optional — only applied when the key exists
    in user_prefs):

      +2.0        genre match        (exact string)
      +1.5        mood match         (exact string)
      0 – 1.0     energy proximity   1.0 - |target - song|
      0 – 1.0     valence proximity  1.0 - |target - song|
      0 – 0.75    danceability       (1.0 - |delta|) * 0.75
      0 – 0.5     tempo proximity    (1.0 - |delta| / 150) * 0.5, clamped ≥ 0
      +0.5/-0.25  acousticness       reward if likes_acoustic, penalize otherwise

    Returns:
        (score, reasons) where reasons is a list of human-readable strings
        explaining each contribution to the final score.
    """
    score = 0.0
    reasons = []

    # Genre match
    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match
    if song.get("mood") == user_prefs.get("mood"):
        score += 1.5
        reasons.append("mood match (+1.5)")

    # Energy proximity (0–1.0)
    if "energy" in user_prefs:
        pts = round(1.0 - abs(user_prefs["energy"] - float(song["energy"])), 2)
        score += pts
        reasons.append(f"energy proximity (+{pts:.2f})")

    # Valence proximity (0–1.0)
    if "valence" in user_prefs:
        pts = round(1.0 - abs(user_prefs["valence"] - float(song["valence"])), 2)
        score += pts
        reasons.append(f"valence proximity (+{pts:.2f})")

    # Danceability proximity (0–0.75)
    if "danceability" in user_prefs:
        pts = round((1.0 - abs(user_prefs["danceability"] - float(song["danceability"]))) * 0.75, 2)
        score += pts
        reasons.append(f"danceability proximity (+{pts:.2f})")

    # Tempo proximity (0–0.5); 150 bpm is the normalisation denominator
    if "tempo_bpm" in user_prefs:
        raw = 1.0 - abs(user_prefs["tempo_bpm"] - float(song["tempo_bpm"])) / 150.0
        pts = round(max(raw, 0.0) * 0.5, 2)
        score += pts
        reasons.append(f"tempo proximity (+{pts:.2f})")

    # Acousticness: boolean preference
    if "likes_acoustic" in user_prefs:
        acousticness = float(song.get("acousticness", 0))
        if user_prefs["likes_acoustic"]:
            pts = round(acousticness * 0.5, 2)
            score += pts
            reasons.append(f"acoustic reward (+{pts:.2f})")
        else:
            penalty = round(acousticness * -0.25, 2)
            score += penalty
            reasons.append(f"acoustic penalty ({penalty:.2f})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return [(song, score, ", ".join(reasons)) for song, score, reasons in ranked[:k]]
