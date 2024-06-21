<h1><p align="center">layerzero-checker</p></h1>

<p align="center"><img src="images/icons/app.ico" width="400"></p>



<h1><p align="center">Content</p></h1>

- [Description](#Description)
- [Useful links](#Useful-links)
- [File structure](#File-structure)
- [How to run](#How-to-run)
  - [Windows](#Windows)
  - [Docker (image)](#Docker-image)
  - [Docker (building)](#Docker-building)
  - [Source code](#Source-code)
- [Updating](#Updating)
  - [Windows](#Windows-1)
  - [GitHub image](#GitHub-image)
  - [Self-built image](#Self-built-image)
  - [Source code](#Source-code-1)
- [Useful commands](#Useful-commands)
- [Report a bug or suggest an idea](#Report-a-bug-or-suggest-an-idea)
- [Express your gratitude](#Express-your-gratitude)



<h1><p align="center">Description</p></h1>
<p align="right"><a href="#Content">To the content</a></p>

⠀The program allows you to:
- Parse data about sybil addresses;
- Check specified addresses if they are sybil.  



<h1><p align="center">Useful links</p></h1>
<p align="right"><a href="#Content">To the content</a></p>

⠀[layerzero-checker](https://github.com/SecorD0/layerzero-checker)



<h1><p align="center">File structure</p></h1>
<p align="right"><a href="#Content">To the content</a></p>

⠀The program use the following files and directories:
- `files` — a user files directory:
  - `addresses.db` — a temporary database.
  - `addresses.xlsx` — a spreadsheet for specifying addresses and viewing results.
  - `errors.log` — a log file with errors that occurred during the work.
- `layerzero-checker.exe` / `app.py` — an executable file that runs the program.



<h1><p align="center">How to run</p></h1>
<p align="right"><a href="#Content">To the content</a></p>


<h2><p align="center">Windows</p></h2>

1. Download an EXE file from the [releases page](https://github.com/SecorD0/layerzero-checker/releases).
2. Create a folder and put the EXE file into it.
3. Run the program.
4. Open the spreadsheet named `addresses.xlsx`, fill in, save and close it. It's mandatory to specify:
- `address`.
5. Enter `1` and press `Enter` to check accounts for drop eligibility.
6. If there are still unchecked addresses left, wait a while or refresh the proxy list and run the check again.
7. Open the `addresses.xlsx` spreadsheet and switch to the `Results` sheet to view the results of the program.


<h2><p align="center">Docker (image)</p></h2>

1. Install Docker, in Ubuntu you can use the command:
```sh
. <(wget -qO- https://raw.githubusercontent.com/SecorD0/utils/main/installers/docker.sh)
```
2. Run the program:
```sh
docker run -it --rm -v $HOME/layerzero-checker/files:/program/files --name layerzero-checker ghcr.io/secord0/layerzero-checker:main
```
3. Open the spreadsheet named `addresses.xlsx`, fill in, save and close it. It's mandatory to specify:
- `address`.
4. Enter `1` and press `Enter` to check accounts for drop eligibility.
5. If there are still unchecked addresses left, wait a while or refresh the proxy list and run the check again.
6. Open the `addresses.xlsx` spreadsheet and switch to the `Results` sheet to view the results of the program.


<h2><p align="center">Docker (building)</p></h2>

1. Install Docker, in Ubuntu you can use the command:
```sh
. <(wget -qO- https://raw.githubusercontent.com/SecorD0/utils/main/installers/docker.sh)
```
2. Clone the repository:
```sh
git clone https://github.com/SecorD0/layerzero-checker
```
3. Go to the repository:
```sh
cd layerzero-checker
```
4. Build an image:
```sh
docker build -t layerzero-checker .
```
5. Run the program:
```sh
docker run -it --rm -v $HOME/layerzero-checker/:/program --name layerzero-checker layerzero-checker
```
6. Open the spreadsheet named `addresses.xlsx`, fill in, save and close it. It's mandatory to specify:
- `address`.
7. Enter `1` and press `Enter` to check accounts for drop eligibility.
8. If there are still unchecked addresses left, wait a while or refresh the proxy list and run the check again.
9. Open the `addresses.xlsx` spreadsheet and switch to the `Results` sheet to view the results of the program.


<h2><p align="center">Source code</p></h2>

1. Install [Python 3.8](https://www.python.org/downloads/).
2. Clone the repository:
```sh
git clone https://github.com/SecorD0/layerzero-checker
```
3. Go to the repository:
```sh
cd layerzero-checker
```
4. Set up an environment.
5. Install requirements:
```sh
pip install -r requirements.txt
```
6. Run the `app.py`.
7. Open the spreadsheet named `addresses.xlsx`, fill in, save and close it. It's mandatory to specify:
- `address`.
8. Enter `1` and press `Enter` to check accounts for drop eligibility.
9. If there are still unchecked addresses left, wait a while or refresh the proxy list and run the check again.
10. Open the `addresses.xlsx` spreadsheet and switch to the `Results` sheet to view the results of the program.


⠀If you want to build the EXE file by yourself:
- Install `pyinstaller`:
```sh
pip install pyinstaller
```
- Build the EXE file:
```sh
pyinstaller app.py -Fn layerzero-checker -i images/icons/app.ico --add-binary "images/icons;images/icons" --collect-datas fake_useragent
```



<h1><p align="center">Updating</p></h1>
<p align="right"><a href="#Content">To the content</a></p>


<h2><p align="center">Windows</p></h2>

1. Download an EXE file of the new version from the [releases page](https://github.com/SecorD0/layerzero-checker/releases) and replace the old one with it.


<h2><p align="center">GitHub image</p></h2>

1. Stop the container:
```sh
docker stop layerzero-checker
```
2. Remove the container:
```sh
docker rm layerzero-checker
```
3. Update the image:
```sh
docker pull ghcr.io/secord0/layerzero-checker:main
```


<h2><p align="center">Self-built image</p></h2>

1. Stop the container:
```sh
docker stop layerzero-checker
```
2. Remove the container:
```sh
docker rm layerzero-checker
```
3. Go to the repository:
```sh
cd layerzero-checker
```
4. Update the local files:
```sh
git pull
```
5. Rebuild the image:
```sh
docker build -t layerzero-checker .
```


<h2><p align="center">Source code</p></h2>

1. Go to the repository:
```sh
cd layerzero-checker
```
2. Update the local files:
```sh
git pull
```



<h1><p align="center">Useful commands</p></h1>
<p align="right"><a href="#Content">To the content</a></p>

⠀To run the program (GitHub image):
```sh
docker run -it --rm -v $HOME/layerzero-checker/files:/program/files --name layerzero-checker ghcr.io/secord0/layerzero-checker:main
```

⠀To run the program (self-built image):
```sh
docker run -it --rm -v $HOME/layerzero-checker/:/program --name layerzero-checker layerzero-checker
```

⠀To remove the container:
```sh
docker stop layerzero-checker; docker rm layerzero-checker
```



<h1><p align="center">Report a bug or suggest an idea</p></h1>
<p align="right"><a href="#Content">To the content</a></p>

⠀If you found a bug or have an idea, go to [the link](https://github.com/SecorD0/layerzero-checker/issues/new/choose), select the template, fill it out and submit it.



<h1><p align="center">Express your gratitude</p></h1>
<p align="right"><a href="#Content">To the content</a></p>

⠀You can express your gratitude to the developer by sending fund to crypto wallets!
- Address of EVM networks (Ethereum, Polygon, BSC, etc.): `0x900649087b8D7b9f799F880427DacCF2286D8F20`
- USDT TRC-20: `TNpBdjcmR5KzMVCBJTRYMJp16gCkQHu84K`
- SOL: `DoZpXzGj5rEZVhEVzYdtwpzbXR8ifk5bajHybAmZvR4H`
- BTC: `bc1qs4a0c3fntlhzn9j297qdsh3splcju54xscjstc`
