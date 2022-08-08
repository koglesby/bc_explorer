from bs4 import BeautifulSoup
import requests

url = "https://svbkvlt.bandcamp.com"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

album_infos = doc.find_all(class_="music-grid-item")

for i, sample_album in enumerate(album_infos, 1):
    print(f"Processing album number #{i}")
    
    try:
        # Link
        album_link = sample_album.find('a')['href']
        # Judge whether the link is relative
        if album_link[0] != 'h':
            album_link = url + album_link[1:]

        # Cover
        img_item = sample_album.find('img')
        # Detect lazy image source url
        if 'data-original' in img_item.attrs:
            img_url = img_item['data-original']
        else:
            img_url = img_item['src']
            
        # Album name
        album_text = sample_album.find('p').contents
        album_name = album_text[0].strip()

        # Artist name
        if len(album_text) > 1:
            artist_name = album_text[2].get_text().strip()
        else:
            artist_name = ""

        # Print info
        print("Page URL: https://ad93.bandcamp.com")
        print("Album link:", album_link)
        print('Album cover image:', img_url)
        print("Album name:", album_name)
        print("Artist:", artist_name)
    except:
        print(f"Error parsing album {i}")