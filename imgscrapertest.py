import bs4
from urllib import request
import lxml
import psycopg2

def JumiaImgScraper(url):
    
    req = request.Request(url, headers={'User-Agent' : "Mono Browser"})
    html = request.urlopen(req)
    bs = bs4.BeautifulSoup(html, "lxml")
    image = bs.find(attrs={"class":"lazy", "data-position":"0"})["data-src"]

    return image

# def main():
#     #JumiaImgScraper("https://www.jumia.co.ke/6.1-2018-5.5-32gb-rom-3gb-ram-16mp-camera-dual-sim-black-copper-nokia-mpg114073.html")

#     cbrand = input("Choice of brand: ")

#     con = psycopg2.connect(database="jjtestdb", user="postgres", password="hieg")
#     off = 0
#     with con:

#         cur = con.cursor()
#         smartphone_cards = [0, 1, 2, 3, 4, 5, 6, 7, 8]

#         for i in range(0, 9):
#             cur.execute("SELECT * FROM smartphones WHERE brand = %s LIMIT 1 OFFSET %s", (cbrand, off))
#             returned_phone = cur.fetchone()
#             off += 1
#             if returned_phone == None:
#                 break
#             if returned_phone[5] == None:
#                 continue
#             print(JumiaImgScraper(returned_phone[5]))

# main()