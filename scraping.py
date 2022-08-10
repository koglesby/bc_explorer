"""Functions for scraping and information collection."""
import imghdr
import json
import requests
import pathlib
from pathlib import Path
from bs4 import BeautifulSoup

def get_label_urls():
    """Return the dictionary of label urls."""
    # Check and load label url json file
    data_dir = Path('.') / 'data'
    if not data_dir.is_dir():
        data_dir.mkdir()
    
    label_urls = {}
    url_filepath = data_dir / 'label_urls.json'
    if url_filepath.is_file():
        with open(url_filepath, 'r') as f:
            label_urls = json.load(f)
    
    return label_urls

def scrape_label_releases(label_url):
    """Scrape label releases given the label url."""
    try:
        result = requests.get(label_url)
    except:
        raise Exception(f"Cannot fetch info from url: {label_url}")

    try:
        doc = BeautifulSoup(result.text, 'html.parser')
    except:
        raise Exception(f"Fail to parse html from url: {label_url}")
    
    try:
        album_infos = doc.find_all(class_='music-grid-item')
    except:
        raise Exception(f"Fail to find album infos from url: {label_url}")
    
    return album_infos

def get_local_albums(label_name):
    """Get the list of album infos stored locally."""
    album_info_path = Path('.') / 'data' / label_name + '.json'
    local_album_infos = [] 
    if album_info_path.is_file():
        with open(album_info_path, 'r') as f:
            local_album_infos = json.load(f)
    
    return local_album_infos
        
def get_label_page(label_name, album_num=10, refresh=False):
    """Return the list of label releases given label name."""
    # Get label->url dictionary
    label_urls = get_label_urls()
    
    # Check whether label url is stored
    if label_name not in label_urls:
        raise KeyError(f"Label name {label_name} not found in library")
    label_url = label_urls[label_name]
    
    # Get the list of album info from label url
    web_album_infos = scrape_label_releases(label_url)
    
    # Get local album informations
    local_album_infos = get_local_albums(label_name)
    
    albums = []
    for i, album in enumerate(web_album_infos):
        if i == album_num: 
            break
        
        # Get album name first
        album_text = album.find('p').contents
        album_name = album_text[0].strip()
        
        # Check whether the album info has been stored locally
        if album_name == local_album_infos[0]['album_name']:
            albums = albums + local_album_infos[:album_num - i]
            # TODO: Store new album info locally
            break
        
        # Parse album info
        try:
            album_link = album.find('a')['href']
            # Judge whether the link is relative
            if album_link[0] != 'h':
                album_link = label_url + album_link[1:]

            # Cover
            img_item = album.find('img')
            # Detect lazy image source url
            if 'data-original' in img_item.attrs:
                img_url = img_item['data-original']
            else:
                img_url = img_item['src']
                
            # Artist name
            if len(album_text) > 1:
                artist_name = album_text[2].get_text().strip()
            else:
                artist_name = ""
        except:
            print(f"Error parsing album {i}")
        
        albums.append(
            {
                'album_url': album_link,
                'cover_img_url': img_url,
                'album_name': album_name,
                'artist_name': artist_name,
                # TODO: Add more album info
            }
        )
    
    # TODO: Store new album info locally (if any)
    
    return albums