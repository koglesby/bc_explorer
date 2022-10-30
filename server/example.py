from utils import save_label_url
from scraping import get_label_page

# Add a new label with its bandcamp URL
save_label_url("GD4YA", "https://gd4ya.bandcamp.com")

# Get label releases
albums = get_label_page(label_name="GD4YA", album_num=10)
print(albums)