# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

### Features it does not consider

**Both versions:** The system has no awareness of artist, popularity, release era, listening history, or context (time of day, activity). Two songs with identical feature vectors are interchangeable — the system cannot tell a beloved classic from an unknown track. It also treats all features as independent; there's no relationship captured between, say, high energy *and* high danceability together (which defines a different feel than either alone).

**Original only:** Because mood was active, the system at least captured emotional tone. With mood disabled in the experiment, emotional nuance disappears entirely — "happy" and "moody" songs are treated as equals.

---

### Genres or moods that are underrepresented

**Both versions:** The `GENRE_RELATED` graph only covers pop, indie pop, synthwave, rock, lofi, ambient, and jazz. Genres like hip-hop, classical, R&B, electronic, and country have no related-genre entries. A fan of any of those genres can only ever earn exact-match genre points — never partial credit for nearby genres.

**Original (worse for this):** The exact genre bonus was +2.0, so an unlisted-genre fan lost twice as many points compared to listed-genre fans when songs were near-misses rather than exact matches.

**Mood side:** `MOOD_RELATED` has no entries for moods like "sad", "angry", "romantic", or "nostalgic". In the original logic, users with those moods got zero mood credit for any song, since neither exact nor related matches existed.

---

### Cases where the system overfits to one preference

**Original:** Genre + mood together dominated scoring (up to +3.5 of ~7.25 max). Users with a matching genre+mood combination got pushed to the top regardless of whether the song's energy, tempo, or valence actually fit. A lofi/chill song could outscore a synthwave/chill song for a lofi fan even if the synthwave song was a much closer match on every continuous dimension.

**Experiment (current):** Energy proximity is worth 0–2.0, the single largest component. The entire ranking effectively becomes an energy-distance sort. Two users with the same `target_energy` but completely different genre/mood preferences receive nearly identical top-5 recommendations.

---

### Ways the scoring might unintentionally favor some users

**Both versions:**
- **Power users** (all optional fields set) can score up to ~2.25 higher than minimal users. A minimal user whose taste is actually well-represented may rank below a power user whose detailed preferences only weakly align.
- **`likes_acoustic=True` users** get up to +0.5 from acousticness; `likes_acoustic=False` users only get up to -0.25 penalty. Acoustic songs survive in non-acoustic recommendations more than non-acoustic songs survive in acoustic ones.
- **Genre graph members** (pop, rock, lofi, jazz fans) get partial credit for related-genre songs. Fans of unlisted genres never do.

**Original additionally favors:** Users whose genre *and* mood both appear in the graph — they earn partial credit on two categorical axes, while an R&B/romantic user earns partial credit on neither.

**Experiment additionally favors:** Users whose musical taste genuinely centers on energy level (workout listeners, EDM fans with consistent high-energy preference). Their `target_energy` is a meaningful signal. Users with inconsistent or contextual energy preferences (varying by mood, time, activity) get poor results because their single `target_energy` value misrepresents them.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
