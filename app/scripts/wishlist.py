import requests
import json
import time
from scripts.utilpath import get_data_path
import keyring



def fetch_wishlist():
    STEAM_API_KEY = keyring.get_password("steamlike", "STEAM_API_KEY")
    STEAM_ID = keyring.get_password("steamlike", "STEAM_ID")
    url = "https://api.steampowered.com/IWishlistService/GetWishlist/v1"
    params = {
        'key': STEAM_API_KEY,
        'steamid': STEAM_ID,
        'include_appinfo': 'true'
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Failed to fetch wishlist.")
        return []

    data = response.json()
    wishlist_items = data.get("response", {}).get("items", [])

    wishlist = []

    for item in wishlist_items:
        appid = item.get("appid")
        try:
            details_url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
            details_response = requests.get(details_url).json()
            if not details_response.get(str(appid), {}).get("success"):
                continue

            game_data = details_response[str(appid)]['data']
            genres = [g['description'] for g in game_data.get('genres', [])]

            wishlist.append({
                "appid": appid,
                "name": game_data.get("name", "Unknown"),
                "genres": genres,
                "header_image": game_data.get("header_image")
            })

            time.sleep(0.5)

        except Exception as e:
            print(f"Error fetching details for appid {appid}: {e}")

    return wishlist

def main():
    wishlist = fetch_wishlist()

    with open(get_data_path("wishlist.json"), "w", encoding='utf-8') as f:
        json.dump(wishlist, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
