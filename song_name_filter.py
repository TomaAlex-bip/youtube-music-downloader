import re

words_to_filter_title = [
    "official",
    "video",
    "hd",
    "hq",
    "lyric",
    "lyrics",
    "music",
    "videoclip",
    "oficial",
    "single",
    "audio",
    "track",
    "clip",
    "tudorchirilaonline",
    "remastered",
]

words_to_filter_artist_name = [
    "topic",
    "oficial",
    "official",
    "16hz",
    "20cm",
    "youtube",
    "channel",
    "group",
    "vevo",
    "music",
]


def check_artist_name(artist):
    if artist == "lunaamara":
        artist = "luna amara"
    if artist == "siaiei":
        artist = "cia"
    if artist.find("codrin bradea") != -1:
        artist = "bazooka"
    if artist == "2886carolina":
        artist = "iris"
    if artist == "scandalos":
        artist = "puya"
    if artist.find("digital") != -1:
        artist = "slipknot"
    if artist.find("paulo") != -1:
        artist = "stone sour"
    if artist.find("warner") != -1:
        artist = "metallica"
    if artist.find("ben") != -1:
        artist = "metallica"
    if artist == "dim":
        artist = "slipknot"
    if artist.find("npdt") != -1:
        artist = "scorpions"

    return artist


def filter_song(title, artist):
    title = title.lower()
    for w in words_to_filter_title:
        title = title.replace(w, "")

    artist = artist.lower()
    for w in words_to_filter_artist_name:
        artist = artist.replace(w, "")

    title = re.sub(r'[^\w\s\-\']', '', title)
    title = " ".join(title.split())
    artist = re.sub(r'[^\w\s]', '', artist)
    artist = " ".join(artist.split())

    title = title.strip()
    artist = artist.strip()

    artist = check_artist_name(artist)

    if artist in title:
        return title.title(), artist.title()

    return f"{artist.title()} - {title.title()}", artist.title()















