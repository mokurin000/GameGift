micromamba activate game_gift

micromamba run pip install -e .
micromamba run pip install pyinstaller

$ENV:PLAYWRIGHT_BROWSERS_PATH = 0
$ENV:HTTPS_PROXY = "http://127.0.0.1:7890"
micromamba run playwright install chromium

micromamba run pyinstaller --optimize 2 -y -D -n GameGift src/gamegift/__main__.py