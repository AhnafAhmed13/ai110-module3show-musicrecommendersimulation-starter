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

# Related genres earn half the genre-match bonus (+1.0 instead of +2.0)
GENRE_RELATED: Dict[str, set] = {
    "pop":      {"indie pop", "synthwave"},
    "indie pop": {"pop"},
    "synthwave": {"pop", "rock"},
    "rock":     {"synthwave"},
    "lofi":     {"ambient", "jazz"},
    "ambient":  {"lofi", "jazz"},
    "jazz":     {"lofi", "ambient"},
}

# Related moods earn half the mood-match bonus (+0.75 instead of +1.5)
MOOD_RELATED: Dict[str, set] = {
    "happy":   {"relaxed"},
    "relaxed": {"happy", "chill"},
    "chill":   {"relaxed", "focused"},
    "focused": {"chill"},
    "intense": {"moody"},
    "moody":   {"intense"},
}


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

def score_song(user: UserProfile, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against a UserProfile.

    Scoring recipe:
      +2.0/+1.0   genre match        exact match +2.0, related genre +1.0 (always applied)
      +1.5/+0.75  mood match         exact match +1.5, related mood +0.75 (always applied)
      0 – 1.0     energy proximity   1.0 - |target - song|  (always applied)
      0 – 1.0     valence proximity  1.0 - |target - song|  (only if target_valence set)
      0 – 0.75    danceability       (1.0 - |delta|) * 0.75 (only if target_danceability set)
      0 – 0.5     tempo proximity    (1.0 - |delta| / 150) * 0.5, clamped ≥ 0 (only if target_tempo_bpm set)
      +0.5/-0.25  acousticness       reward if likes_acoustic, penalize otherwise (always applied)

    Returns:
        (score, reasons) where reasons is a list of human-readable strings
        explaining each contribution to the final score.
    """
    score = 0.0
    reasons = []

    # Genre match (exact +2.0, related +1.0)
    song_genre = song.get("genre")
    if song_genre == user.favorite_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")
    elif song_genre in GENRE_RELATED.get(user.favorite_genre, set()):
        score += 1.0
        reasons.append(f"related genre '{song_genre}' (+1.0)")

    # Mood match (exact +1.5, related +0.75)
    song_mood = song.get("mood")
    if song_mood == user.favorite_mood:
        score += 1.5
        reasons.append("mood match (+1.5)")
    elif song_mood in MOOD_RELATED.get(user.favorite_mood, set()):
        score += 0.75
        reasons.append(f"related mood '{song_mood}' (+0.75)")

    # Energy proximity (0–1.0)
    pts = round(max(1.0 - abs(user.target_energy - float(song["energy"])), 0.0), 2)
    score += pts
    reasons.append(f"energy proximity (+{pts:.2f})")

    # Valence proximity (0–1.0) — only if set
    if user.target_valence is not None:
        pts = round(1.0 - abs(user.target_valence - float(song["valence"])), 2)
        score += pts
        reasons.append(f"valence proximity (+{pts:.2f})")

    # Danceability proximity (0–0.75) — only if set
    if user.target_danceability is not None:
        pts = round((1.0 - abs(user.target_danceability - float(song["danceability"]))) * 0.75, 2)
        score += pts
        reasons.append(f"danceability proximity (+{pts:.2f})")

    # Tempo proximity (0–0.5) — only if set; 150 bpm is the normalisation denominator
    if user.target_tempo_bpm is not None:
        raw = 1.0 - abs(user.target_tempo_bpm - float(song["tempo_bpm"])) / 150.0
        pts = round(max(raw, 0.0) * 0.5, 2)
        score += pts
        reasons.append(f"tempo proximity (+{pts:.2f})")

    # Acousticness: boolean preference
    acousticness = float(song.get("acousticness", 0))
    if user.likes_acoustic:
        pts = round(acousticness * 0.5, 2)
        score += pts
        reasons.append(f"acoustic reward (+{pts:.2f})")
    else:
        penalty = round(acousticness * -0.25, 2)
        score += penalty
        reasons.append(f"acoustic penalty ({penalty:.2f})")

    return round(score, 2), reasons


def recommend_songs(user: UserProfile, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [
        (song, *score_song(user, song))
        for song in songs
    ]
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return [(song, score, ", ".join(reasons)) for song, score, reasons in ranked[:k]]
