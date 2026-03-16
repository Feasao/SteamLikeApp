import requests
import time
import json
from scripts.utilpath import get_data_path

def get_tags(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"

    try:
        response = requests.get(url)
        data = response.json()

        if data[str(appid)]['success']:
            game_data = data[str(appid)]['data']
            genres = [g['description'] for g in game_data.get('genres', [])]
            return {"genres": genres}

    except Exception as e:
        print(f"Error fetching data for appid {appid}: {e}")
        return {"genres": []}

def main():
    url = "https://store.steampowered.com/api/featuredcategories"
    response = requests.get(url)
    data = response.json()
    specials_raw = data['specials']['items']
    formatted_specials = []
    for item in specials_raw:
        appid = item['id']
        tags = get_tags(appid)
        
        formatted = {
            "appid": appid,
            "name": item['name'],
            "genres": tags,
            "img_icon_url": item['large_capsule_image'],
        }
        formatted_specials.append(formatted)
        time.sleep(0.5)

    with open(get_data_path("specials.json"), "w", encoding='utf-8') as f:
        json.dump(formatted_specials, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
