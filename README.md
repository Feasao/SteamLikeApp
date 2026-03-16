# SteamLike

A desktop app that recommends Steam games based on your playtime, genres and library stats.

## Requirements
- Python 3.10+
- Steam account + API key ([get it here](https://steamcommunity.com/dev/apikey))
- Steam ID ([find it here in your profile tab, it will say in the url](https://steamcommunity.com/profiles/))

## Running
Run the app:
```bash
python app/SteamLike.py
```

On first launch you will be prompted to enter your Steam API key and Steam ID. These are stored securely in your OS keychain.

Press **ANALYSE** to fetch and rank your games. Click any card to open it in Steam.

## Building the exe
```bash
pyinstaller --onefile --windowed --icon=app/SteamLike2.ico --add-data "app/components;components" --add-data "app/Itypes;Itypes" --add-data "app/scripts;scripts" --add-data "app/SteamLike2.ico;." app/SteamLike.py
```
Output will be in `dist/SteamLike.exe`.

## Built with
- PyQt6
- Scikit-learn
- PyInstaller
- beautifulsoup4
- keyring