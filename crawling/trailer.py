from urllib.request import urlopen

from bs4 import BeautifulSoup
from movie import *

def getTrailer(movies):
    youtube_url = 'https://www.youtube.com/results?search_query='
