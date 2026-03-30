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
