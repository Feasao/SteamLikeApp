import time
import requests
import json
import keyring
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
    
    STEAM_API_KEY = keyring.get_password("steamlike", "STEAM_API_KEY")
    STEAM_ID = keyring.get_password("steamlike", "STEAM_ID")
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        'key': STEAM_API_KEY,
        'steamid': STEAM_ID,
        'include_appinfo': 'true'
    }

    response = requests.get(url, params=params)
    data = response.json()

    fields = ['appid', 'name', 'playtime_forever', 'rtime_last_played']

    GamesPlayed = [game for game in data['response']['games'] if game['playtime_forever'] > 0]
    GamesPlayed.sort(key=lambda g: g['playtime_forever'], reverse=True)

    cleaned_games = []
    for game in GamesPlayed:
        if game['name'] != 'TOXIKK':
            cleaned_game = {field: game[field] for field in fields if field in game}
            cleaned_games.append(cleaned_game)
            tag_data = get_tags(game['appid'])
            cleaned_game["genres"] = tag_data["genres"]
        time.sleep(0.5)


    with open(get_data_path('games.json'), 'w') as json_file:
        json.dump(cleaned_games, json_file, indent=4)

if __name__ == "__main__":
    main()