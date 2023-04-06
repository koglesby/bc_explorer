"""Functions for scraping and information collection."""
from urllib.parse import urlparse
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from utils import add_new_releases, save_releases, parse_album_info
import uuid


def scrape_search(search_term):
    try:
        clean_search_term = search_term.replace(" ", "+")
        result = requests.get(
            "https://bandcamp.com/search?q=" + clean_search_term + "&item_type=b&from=results")
    except:
        raise Exception(f"Cannot fetch info from url")
    try:
        doc = BeautifulSoup(result.text, 'html.parser')
    except:
        raise Exception(f"Fail to parse html from url")

    try:
        searchresults = doc.find_all(class_='searchresult')
        searchresult_arr = []
        for i, searchresult in enumerate(searchresults):
            if i == 10:
                break

            result_info = searchresult.find(class_='result-info')

            search_img = searchresult.find(class_='art').find('img')['src']

            heading_contents = result_info.find(
                class_='heading').find('a').contents
            heading = heading_contents[0].strip()

            itemurl_contents = searchresult.find(
                class_='itemurl').find('a').contents
            itemurl = itemurl_contents[0].strip()

            itemtype_contents = searchresult.find(class_='itemtype').contents
            itemtype = itemtype_contents[0].strip()

            subhead_contents = searchresult.find(class_='subhead').contents
            subhead = subhead_contents[0].strip()

            searchresult_object = {
                'name': heading,
                'url': itemurl,
                'itemtype': itemtype,
                'subhead': subhead,
                'img_src': search_img,
                'id': uuid.uuid4().hex
            }

            searchresult_arr.append(searchresult_object)
    except:
        raise Exception(f"Fail to find search results from url")
    return searchresult_arr


def scrape_user_search(username):
    """Scrape the Bandcamp search result for user."""
    try:
        result = requests.get(
            "https://bandcamp.com/search?q=" + username + "&item_type=f")
    except:
        raise Exception(f"Cannot fetch user search result")
    try:
        doc = BeautifulSoup(result.text, 'html.parser')
    except:
        raise Exception(f"Fail to parse html from url")

    try:
        searchresults = doc.find_all(class_='searchresult')
        searchresult_arr = []
        for i, searchresult in enumerate(searchresults):
            # Only fetch 10 results
            if i == 10:
                break

            result_info = searchresult.find(class_='result-info')

            try:
                search_img = searchresult.find(class_='art').find('img')['src']
            except:
                search_img = ""

            heading_contents = result_info.find(
                class_='heading').find('a').contents
            heading = heading_contents[0].strip()

            itemurl_contents = searchresult.find(
                class_='itemurl').find('a').contents
            itemurl = itemurl_contents[0].strip()

            try:
                genre_contents = searchresult.find(class_='genre').contents
                genre = genre_contents[0].strip()[7:]
            except:
                genre = ""

            searchresult_object = {
                'name': heading,
                'url': itemurl,
                'img_src': search_img,
                'genre': genre,
                'id': uuid.uuid4().hex
            }

            searchresult_arr.append(searchresult_object)
    except:
        raise Exception(f"Fail to find search results from url")

    return searchresult_arr


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
        result = requests.get(label_url + '/music')
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


def get_label_page_by_url(label_url):
    """does the thing"""

    web_album_infos = scrape_label_releases(label_url)

    albums = []

    for i, album in enumerate(web_album_infos):

        # Get album name first
        album_text = album.find('p').contents
        album_name = album_text[0].strip()

        extracted_album_info = parse_album_info(
            label_url, album, album_text=album_text, album_name=album_name)

        albums.append(extracted_album_info)

    return albums


def get_release_details(release_url):
    """Return release details based on url"""
    try:
        result = requests.get(release_url)
    except:
        raise Exception(f"Cannot fetch info from url")
    try:
        doc = BeautifulSoup(result.text, 'html.parser')
        release_credits = doc.find_all(class_='tralbum-credits')

        stringy = release_credits[0].contents[0]

        scraped_release_date = stringy.strip()

    except:
        raise Exception(f"Fail to parse html from url")

    return scraped_release_date


def scrape_recommended(release_url):
    """Return release details based on url"""
    try:
        result = requests.get(release_url)
    except:
        raise Exception(f"Cannot fetch info from url")
    try:
        doc = BeautifulSoup(result.text, 'html.parser')

        whole_els = doc.find_all(class_='recommended-album')
        # create an empty list to store the extracted information
        extracted_info = []

        # iterate over each element
        for element in whole_els:
            # use BeautifulSoup to parse the element's HTML
            soup = BeautifulSoup(str(element), 'html.parser')

            # extract the required information
            album_art = soup.find('img', class_='album-art')['src']

            # change the image src to a larger version
            new_number = '2'

            # Split the string into two parts: before and after the underscore
            string_parts = album_art.split('_')
            before_underscore = string_parts[0] + '_'
            after_underscore = string_parts[1]

            # Replace the numbers after the underscore with the new number
            new_string = before_underscore + new_number + \
                '.' + after_underscore.split('.')[1]

            release_title = soup.find('span', class_='release-title').text
            by_artist = soup.find('span', class_='by-artist').text
            # remove 'by ' from scraped by-artist
            artist = by_artist[3:]

            go_to_album = soup.find('a', class_='go-to-album')['href']
            # remove query string from the end of the scraped href ( '...?from=footer-cc-a26986634' )
            href_without_querystring = urlparse(
                go_to_album)._replace(query=None).geturl()

            # create an object for the extracted information
            # info_object = {
            #     'album_art': new_string,
            #     'release_title': release_title,
            #     'by_artist': artist,
            #     'go_to_album': href_without_querystring
            # }
            info_object = {
                'cover_img_url': new_string,
                'album_name': release_title,
                'artist_name': artist,
                'album_url': href_without_querystring
            }

        #     <ReleaseCard v-if="itemtype === 'ARTIST' || itemtype === 'LABEL'" :key="release.album_name"
        #   :url="release.album_url" :artist="itemtype === 'ARTIST' ? label_name : release.artist_name"
        #   :cover="release.cover_img_url" :title="release.album_name" :fromItemtype="itemtype">
        # </ReleaseCard>

            # append the object to the list of extracted information
            extracted_info.append(info_object)

    except:
        raise Exception(f"Fail to parse html from url")

    return extracted_info


def scrape_following_labels(profile_url):
    """Get the labels and artists a Bandcamp user is following."""
    following_url = profile_url + '/following/artists_and_labels'
    try:
        result = requests.get(following_url)
    except:
        raise Exception(f"Cannot fetch info from url: {following_url}")

    try:
        doc = BeautifulSoup(result.text, 'html.parser')
    except:
        raise Exception(f"Fail to parse html from url: {following_url}")

    try:
        follow_infos = doc.find_all(class_='fan-username')
    except:
        raise Exception(
            f"Fail to find following info from url: {following_url}")

    all_follows = [{'label_name': follow.get_text(), 'label_url': follow['href']}
                   for follow in follow_infos]

    return all_follows


# def get_label_page(label_name, album_num=10, refresh=False):
#     """Return the list of label releases given label name."""
#     # Get label->url dictionary
#     label_urls = get_label_urls()

#     # Check whether label url is stored
#     if label_name not in label_urls:
#         raise KeyError(f"Label name {label_name} not found in library")

#     label_url = label_urls[label_name]['url']

#     # Get the list of album info from label url
#     web_album_infos = scrape_label_releases(label_url)

#     # Check whether the requested album num is too long
#     if album_num > len(web_album_infos):
#         raise ValueError(f"Requested album number is too large: {album_num}")

#     # Get local album informations
#     local_album_infos = get_local_albums(label_name)

#     albums = []
#     apply_local_info = False
#     for i, album in enumerate(web_album_infos):
#         if i == album_num:
#             break

#         # Get album name first
#         album_text = album.find('p').contents
#         album_name = album_text[0].strip()

#         # Check whether the album info has been stored locally
#         if len(local_album_infos) and\
#                 album_name == local_album_infos[0]['album_name']:
#             # Add new releases (if any) to local info if no older releases are requested
#             if i + len(local_album_infos) >= album_num:
#                 if len(albums):
#                     save_releases(label_name, albums, local_album_infos)
#                 albums = albums + local_album_infos[:album_num - i]
#             else:
#                 albums = albums + local_album_infos

#             apply_local_info = True
#             break

#         extracted_album_info = parse_album_info(
#             label_url, album, album_text=album_text, album_name=album_name)
#         albums.append(extracted_album_info)

#     # In case none release info is fetched from cache,
#     # add all potential new releases to local data
#     if not apply_local_info:
#         if len(local_album_infos):
#             add_new_releases(label_name,
#                              label_url,
#                              albums,
#                              web_album_infos,
#                              local_album_infos)
#         else:
#             save_releases(label_name, albums, [])

#     # Check whether current data covers the oldest info requested
#     if len(albums) < album_num:
#         # Parse older releases than local data
#         tail_albums = []
#         for i in range(len(albums), album_num):
#             album_text = web_album_infos[i].find('p').contents
#             album_name = album_text[0].strip()
#             extracted_album_info = parse_album_info(
#                 label_url, web_album_infos[i],
#                 album_text=album_text, album_name=album_name)
#             tail_albums.append(extracted_album_info)

#         # Add older releases to local data
#         save_releases(label_name, albums, tail_albums)

#         albums += tail_albums

#     return albums
