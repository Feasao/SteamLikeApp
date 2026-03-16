import requests
from bs4 import BeautifulSoup
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
            large_capsule_image = game_data.get("header_image", "")
            return genres, large_capsule_image
    except Exception as e:
        print(f"Error fetching genres for appid {appid}: {e}")
    return []

def scrape_popular_new_releases(max_games=150):
    base_url = "https://store.steampowered.com/search/"
    params = {
        "sort_by": "Released_DESC",
        "supportedlang": "english,greek",
        "filter": "popularnew",
        "ndl": "1",
        "page": 1
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    games = []

    while len(games) < max_games:
        print(f"Fetching page {params['page']}...")
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page {params['page']}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a", class_="search_result_row")

        if not results:
            print("No more results found.")
            break

        for result in results:
            if len(games) >= max_games:
                break

            title = result.find("span", class_="title").get_text(strip=True)
            link = result["href"]
            appid = link.split("/app/")[1].split("/")[0] if "/app/" in link else None
            if not appid:
                continue
            
            genres, large_capsule_image = get_tags(appid)
            time.sleep(0.5)

            games.append({
                "appid": int(appid),
                "name": title,
                "genres": genres,
                "img_icon_url": large_capsule_image
            })

        params["page"] += 1
        time.sleep(.5)

    return games


def main():
    new_and_trending = scrape_popular_new_releases()
    with open(get_data_path("new_and_trending.json"), "w", encoding='utf-8') as f:
        json.dump(new_and_trending, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
