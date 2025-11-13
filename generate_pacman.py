import requests
from bs4 import BeautifulSoup

USERNAME = "Beebek-Sharma"
OUTPUT_LIGHT = "pacman-contribution-graph.svg"
OUTPUT_DARK = "pacman-contribution-graph-dark.svg"

def download_svg(theme, output):
    url = f"https://github-contribution-stats.vercel.app/api/pacman?username={USERNAME}&theme={theme}"
    svg = requests.get(url).text
    with open(output, "w", encoding="utf-8") as f:
        f.write(svg)

download_svg("light", OUTPUT_LIGHT)
download_svg("dark", OUTPUT_DARK)

print("Pacman graphs generated!")
