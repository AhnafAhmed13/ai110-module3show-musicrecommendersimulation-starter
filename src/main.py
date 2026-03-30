"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, UserProfile


def main() -> None:
    songs = load_songs("../data/songs.csv")

    profiles = {
        "High-Energy Pop": UserProfile(
            favorite_genre="pop",
            favorite_mood="happy",
            target_energy=0.9,
            likes_acoustic=False,
            target_valence=0.85,
            target_danceability=0.85,
            target_tempo_bpm=128,
        ),
        "Chill Lofi": UserProfile(
            favorite_genre="lofi",
            favorite_mood="calm",
            target_energy=0.2,
            likes_acoustic=True,
            target_valence=0.4,
            target_danceability=0.35,
            target_tempo_bpm=75,
        ),
        # --- Edge case / adversarial profiles ---
        "Sad Gym Rat (mood not in catalog)": UserProfile(
            favorite_genre="pop",
            favorite_mood="sad",        # no song has mood="sad"
            target_energy=0.9,
            likes_acoustic=False,
        ),
        "Valence Contradiction (happy mood, dark valence)": UserProfile(
            favorite_genre="indie pop",
            favorite_mood="happy",
            target_energy=0.76,
            likes_acoustic=False,
            target_valence=0.05,        # wants dark emotional tone
            target_danceability=0.8,
        ),
        "Acoustic Energy Seeker (conflicting features)": UserProfile(
            favorite_genre="rock",
            favorite_mood="intense",
            target_energy=0.91,
            likes_acoustic=True,        # acoustic songs tend to be low energy
            target_danceability=0.7,
        ),
        "Out-of-Range Energy (unclamped bug test)": UserProfile(
            favorite_genre="ambient",
            favorite_mood="chill",
            target_energy=1.5,          # outside [0, 1] — was a negative-score bug
            likes_acoustic=True,
        ),
        "Genre Hermit (nothing in catalog matches)": UserProfile(
            favorite_genre="classical",  # not in catalog
            favorite_mood="peaceful",    # not in catalog
            target_energy=0.3,
            likes_acoustic=True,
            target_valence=0.6,
            target_tempo_bpm=80,
        ),
        "Everything Maxed (weight dominance test)": UserProfile(
            favorite_genre="pop",
            favorite_mood="happy",
            target_energy=1.0,
            likes_acoustic=False,
            target_valence=1.0,
            target_danceability=1.0,
            target_tempo_bpm=200,       # beyond all songs in catalog
        ),
        "Tempo Punisher (extreme BPM silences tempo signal)": UserProfile(
            favorite_genre="lofi",
            favorite_mood="chill",
            target_energy=0.35,
            likes_acoustic=True,
            target_tempo_bpm=300,       # all songs clamp to 0 tempo points
        ),
    }

    for profile_name, profile in profiles.items():
        print(f"\n{'='*40}")
        print(f"Profile: {profile_name}")
        print(f"{'='*40}")

        recommendations = recommend_songs(profile, songs, k=5)

        print("\nTop recommendations:\n")
        for rec in recommendations:
            # You decide the structure of each returned item.
            # A common pattern is: (song, score, explanation)
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
