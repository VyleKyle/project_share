import requests
from bs4 import BeautifulSoup

cookies = {
    'borrowed-cookies-from-my-own-session': 'for scraping their site'
    'against-TOS': 'probably'
    # But they didn't support sorting dependencies by downloads.
    # I forget exactly what I was trying to find, but this was a nice bit of random python.
}


def fetch_modpacks(base_url, pages, cookies=cookies):
    modpacks = []
    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch the webpage at {url}")
            print(response.content)
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        for item in soup.find_all("li", class_="project-listing-row"):
            name_tag = item.find("h3")
            downloads_tag = item.find("span", text=lambda x: x and 'Downloads' in x)

            if name_tag and downloads_tag:
                name = name_tag.text.strip()
                downloads = downloads_tag.text.strip().split()[0].replace(',', '')
                modpacks.append((name, int(downloads)))

    return modpacks

def main():
    base_url = "https://www.curseforge.com/minecraft/mc-mods/millenaire/relations/dependencies"
    total_pages = 17
    modpacks = fetch_modpacks(base_url, total_pages)

    # Sort the modpacks based on downloads
    modpacks.sort(key=lambda x: x[1], reverse=True)

    # Print top 20 modpacks
    top_20_modpacks = modpacks[:20]
    for i, (name, downloads) in enumerate(top_20_modpacks):
        print(f"{i+1}. {name}: {downloads} downloads")

if __name__ == "__main__":
    main()

