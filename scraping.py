"""Functions for scraping and information collection."""
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from utils import add_new_releases, save_releases, parse_album_info

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
    release_info_path = Path('.') / 'data' / (label_name + '.json')
    local_album_infos = [] 
    if release_info_path.is_file():
        with open(release_info_path, 'r') as f:
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
    
    # Check whether the requested album num is too long
    if album_num > len(web_album_infos):
        raise ValueError(f"Requested album number is too large: {album_num}")
    
    # Get local album informations
    local_album_infos = get_local_albums(label_name)
    
    albums = []
    apply_local_info = False
    for i, album in enumerate(web_album_infos):
        if i == album_num: 
            break
        
        # Get album name first
        album_text = album.find('p').contents
        album_name = album_text[0].strip()
        
        # Check whether the album info has been stored locally
        if len(local_album_infos) and\
                album_name == local_album_infos[0]['album_name']:
            # Add new releases (if any) to local info if no older releases are requested
            if i + len(local_album_infos) >= album_num:
                if len(albums):
                    save_releases(label_name, albums, local_album_infos)
                albums = albums + local_album_infos[:album_num - i]
            else:
                albums = albums + local_album_infos

            apply_local_info = True
            break
        
        extracted_album_info = parse_album_info(
            label_url, album, album_text=album_text, album_name=album_name)
        albums.append(extracted_album_info)
    
    # In case none release info is fetched from cache, 
    # add all potential new releases to local data
    if not apply_local_info:
        if len(local_album_infos):
            add_new_releases(label_name,
                            label_url,
                            albums,
                            web_album_infos,
                            local_album_infos)
        else:
            save_releases(label_name, albums, [])
        
    # Check whether current data covers the oldest info requested
    if len(albums) < album_num:
        # Parse older releases than local data
        tail_albums = []
        for i in range(len(albums), album_num):
            album_text = web_album_infos[i].find('p').contents
            album_name = album_text[0].strip()
            extracted_album_info = parse_album_info(
                label_url, web_album_infos[i],
                album_text=album_text, album_name=album_name)
            tail_albums.append(extracted_album_info)
        
        # Add older releases to local data
        save_releases(label_name, albums, tail_albums)
        
        albums += tail_albums
    
    return albums