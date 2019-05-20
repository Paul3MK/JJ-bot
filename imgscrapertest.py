import bs4
from urllib import request
import lxml

def JumiaImgScraper(url):
    
    req = request.Request(url, headers={'User-Agent' : "Mono Browser"})
    html = request.urlopen(req)
    bs = bs4.BeautifulSoup(html, "lxml")
    image = bs.find(attrs={"class":"lazy", "data-position":"0"})["data-src"]

    return image

#def main():
#    JumiaImgScraper("https://www.jumia.co.ke/6.1-2018-5.5-32gb-rom-3gb-ram-16mp-camera-dual-sim-black-copper-nokia-mpg114073.html")

# main()