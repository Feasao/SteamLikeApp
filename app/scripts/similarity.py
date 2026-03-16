import json
import math
import time
from collections import defaultdict
from scripts.utilpath import get_data_path

NOW = int(time.time())
RECENCY_WINDOW = 180 * 24 * 3600 

def load_json(path):
    with open(get_data_path(path), "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_recency(rtime_last_played):
    if not rtime_last_played:
        return 0
    age = NOW - rtime_last_played
    if age < 0:
        return 1.0
    return math.exp(-math.log(2) * age / RECENCY_WINDOW)

def build_tag_profile(owned_games, wishlist_games=None):
    tag_weights = defaultdict(float)
    total_weight = 0

    for game in owned_games:
        playtime = game.get("playtime_forever", 0)
        genres = game.get("genres", [])
        rtime_last_played = game.get("rtime_last_played", 0)
        if not genres:
            continue

        recency_boost = normalize_recency(rtime_last_played)
        weight = math.log(playtime + 1) * (1 + 0.25 * recency_boost)
        weight_per_tag = weight / len(genres)

        for tag in genres:
            tag_weights[tag] += weight_per_tag
            total_weight += weight_per_tag

    if wishlist_games:
        for game in wishlist_games:
            genres = game.get("genres", [])
            if (sum(tag_weights.values()) > 0):
                weight_per_wishlist_game = (sum(tag_weights.values()) * 0.75) / len(wishlist_games)
                for game in wishlist_games:
                    genres = game.get("genres", [])
                    if not genres:
                        continue
                    weight_per_tag = weight_per_wishlist_game / len(genres)
                    for tag in genres:
                        tag_weights[tag] += weight_per_tag
                        total_weight += weight_per_tag

    for tag in tag_weights:
        tag_weights[tag] /= total_weight if total_weight > 0 else 1

    return dict(tag_weights)

def compute_similarity(candidate_tags, tag_profile):
    return sum(tag_profile.get(tag, 0) for tag in candidate_tags)

def rank_candidates(candidates, tag_profile, owned_appids=None):
    if owned_appids is None:
        owned_appids = set()

    ranked = []
    for game in candidates:
        if game["appid"] in owned_appids:
            continue

        tags = game.get("genres") or []
        score = compute_similarity(tags, tag_profile)

        if score > 0:
            ranked.append({**game, "similarity_score": round(score, 4)})

    return sorted(ranked, key=lambda x: x["similarity_score"], reverse=True)

def main():
    owned = load_json("games.json")
    wishlist = load_json("wishlist.json")
    specials = load_json("specials.json")
    trending = load_json("new_and_trending.json")

    tag_profile = build_tag_profile(owned, wishlist)
    with open(get_data_path("tag_profile.json"), "w", encoding="utf-8") as f:
        json.dump(tag_profile, f, indent=4, ensure_ascii=False)

    owned_ids = {game["appid"] for game in owned}
    candidates = specials + trending

    ranked = rank_candidates(candidates, tag_profile, owned_ids)

    with open(get_data_path("ranked.json"), "w", encoding="utf-8") as f:
        json.dump(ranked, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(ranked)} ranked recommendations.")

if __name__ == "__main__":
    main()
