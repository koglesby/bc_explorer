"""Helper functions"""
from cProfile import label
import os
import json
from pathlib import Path


def parse_album_info(
        label_url, raw_album_info, album_text=None, album_name=None):
    """Parse and return detailed album info from raw html."""
    try:
        if album_text is None:
            album_text = raw_album_info.find('p').contents
            album_name = album_text[0].strip()

        album_link = raw_album_info.find('a')['href']
        # Judge whether the link is relative
        if album_link[0] != 'h':
            album_link = label_url + album_link[1:]

        # Cover
        img_item = raw_album_info.find('img')
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
        print(f"Error parsing album {album_name}")

    extracted_album_info = {
        'album_url': album_link,
        'cover_img_url': img_url,
        'album_name': album_name,
        'artist_name': artist_name,
        # TODO: Add more album info
    }

    return extracted_album_info


def save_label_url(label_name, url):
    """Save a label name -> url pair in local json file."""
    # Check and load label url json file
    data_dir = Path('.') / 'data'
    if not data_dir.is_dir():
        data_dir.mkdir()

    label_urls = {}
    url_filepath = data_dir / 'label_urls.json'
    if url_filepath.is_file():
        with open(url_filepath, 'r') as f:
            label_urls = json.load(f)

    label_urls[label_name] = url

    # Save json file
    with open(url_filepath, 'w') as fw:
        json.dump(label_urls, fw)


def save_releases(label_name, new_releases, old_releases):
    """Concatenate new and old releases and add them to local data."""
    release_info_path = Path('.') / 'data' / (label_name + '.json')
    with open(release_info_path, 'w') as fw:
        label_releases = new_releases + old_releases
        json.dump(label_releases, fw)
    print("Releases saved")


def add_new_releases(
        label_name, label_url, new_releases, web_album_info, old_releases):
    """Add all the new release info to local data."""
    release_info_path = Path('.') / 'data' / (label_name + '.json')

    assert(len(new_releases) <= len(web_album_info))

    label_releases = []
    label_releases += new_releases
    
    # Get the missing release info between new and old releases
    for i in range(len(new_releases), len(web_album_info)):
        album = web_album_info[i]
        
        album_text = album.find('p').contents
        album_name = album_text[0].strip()
        
        # Check whether the album info has been stored locally
        if len(old_releases) and\
                album_name == old_releases[0]['album_name']:                
            label_releases += old_releases
            break
        
        extracted_album_info = parse_album_info(
            label_url, album, album_text=album_text, album_name=album_name)
        label_releases.append(extracted_album_info)

    with open(release_info_path, 'w') as fw:
        json.dump(label_releases, fw)
    
    print("New releases added")
