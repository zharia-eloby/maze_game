# A Maze Game

## General Overview:
This program takes in user input to dynamically generate a maze and includes the capability of solving a maze. The player can choose their difficulty by picking predetermined sizes or doing a custom size.

See the [game_screenshots](https://github.com/zharia-eloby/maze_game/tree/main/game_screenshots) folder for previews!

## How to Run:
### From the Executable:
1. Go to the [Releases](https://github.com/zharia-eloby/maze_game/releases) page
2. Select the latest release
3. Under the `Assets` section, select the zipped folder titled `MazeGame-<versions>-<releaseDate>`, i.e. `MazeGame-v2.0.0-Dec2024`, to download the folder containing the executable
4. Open the downloaded folder
5. In the folder, there's an executable named `maze_game_app.exe`. Click on it to start playing!

### From the Source:
Prerequisite:
* Have Python 3.x installed

Steps:
1. Download or clone this repo
2. Open a terminal and navigate to this repo
3. (optional, but recommended) Start a virtual environment by running `python -m venv .`, then run `Scripts\activate`
    * See these [docs](https://docs.python.org/3/library/venv.html) for more info on virtual environments
4. Run `pip install -r requirements.txt` to install all dependencies
5. Run `python app/run.py`
