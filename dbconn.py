import psycopg2
import urllib.parse
import ShoppingApi as sapi
import imgscrapertest as imgscraper
import os


def DatabaseProvisioning():
	smartphones = ["https://www.jumia.co.ke/mobile-phones/samsung/", "https://www.jumia.co.ke/mobile-phones/huawei/",	"https://www.jumia.co.ke/mobile-phones/apple/",	"https://www.jumia.co.ke/android-phones/nokia_1/?price=7000-97011",	"https://www.jumia.co.ke/mobile-phones/tecno/?sort=Price%3A%20High%20to%20Low&dir=desc",	"https://www.jumia.co.ke/mobile-phones/oppo/", "https://www.jumia.co.ke/mobile-phones/infinix/", "https://www.jumia.co.ke/smartphones/xiaomi/", "https://www.jumia.co.ke/smartphones/sony/"]
	tablets = ["https://www.jumia.co.ke/ipads/apple/", "https://www.jumia.co.ke/tablets/samsung/", "https://www.jumia.co.ke/tablets/huawei/", "https://www.jumia.co.ke/tablets/lenovo/", "https://www.jumia.co.ke/tablets/amazon/"]
	laptops = ["https://www.jumia.co.ke/laptops/dell/?sort=Price%3A%20High%20to%20Low&dir=desc", "https://www.jumia.co.ke/laptops/apple/", "https://www.jumia.co.ke/laptops/brand-asus/", "https://www.jumia.co.ke/laptops/hp/", "https://www.jumia.co.ke/laptops/lenovo/"]
	tvs = ["https://www.jumia.co.ke/televisions/sony/", "https://www.jumia.co.ke/televisions/samsung/", "https://www.jumia.co.ke/televisions/tcl/", "https://www.jumia.co.ke/televisions/lg/", "https://www.jumia.co.ke/televisions/skyworth/", "https://www.jumia.co.ke/televisions/hisense/", "https://www.jumia.co.ke/televisions/nasco/", "https://www.jumia.co.ke/televisions/haier--mooka", "https://www.jumia.co.ke/televisions/syinix/", "https://www.jumia.co.ke/televisions/vision-plus/"]
	smartwatches = ["https://www.jumia.co.ke/smart-watches/apple", "https://www.jumia.co.ke/smart-watches/huawei", "https://www.jumia.co.ke/smart-watches/mi", "https://www.jumia.co.ke/smart-watches/lenovo"]

	power_banks = ["https://www.jumia.co.ke/mobile-phone-accessories-power-banks/anker/", "https://www.jumia.co.ke/mobile-phone-accessories-power-banks/oraimo/"]
	chargers = ["https://www.jumia.co.ke/mobile-phone-adapters/infinix/", "https://www.jumia.co.ke/mobile-phone-adapters/apple/", "https://www.jumia.co.ke/mobile-phone-adapters/samsung/"]
	headphones = ["https://www.jumia.co.ke/electronics-headphone/jbl/", "https://www.jumia.co.ke/electronics-headphone/brand-sennheiser--sony--plantronics--philips--logitech/", "https://www.jumia.co.ke/electronics-headphone/beats/", "https://www.jumia.co.ke/electronics-headphone/pace/"]
	memory_cards = ["https://www.jumia.co.ke/computer-memory-cards/sandisk/", "https://www.jumia.co.ke/computer-memory-cards/sandisk/?page=2", "https://www.jumia.co.ke/computer-memory-cards/samsung/", "https://www.jumia.co.ke/computer-memory-cards/toshiba/", "https://www.jumia.co.ke/computer-memory-cards/advance/", "https://www.jumia.co.ke/computer-memory-cards/transcend/", "https://www.jumia.co.ke/computer-memory-cards/oraimo/"]
	mice = ["https://www.jumia.co.ke/mouse/logitech/", "https://www.jumia.co.ke/mouse/hp/", "https://www.jumia.co.ke/mouse/-razer/", "https://www.jumia.co.ke/mouse/dell/", "https://www.jumia.co.ke/mouse/brand-asus/", "https://www.jumia.co.ke/mouse/kingston/", "https://www.jumia.co.ke/mouse/cooler-master/", "https://www.jumia.co.ke/mouse/lenovo/", "https://www.jumia.co.ke/mouse/benq/", "https://www.jumia.co.ke/mouse/apple/"]
	keyboards = ["https://www.jumia.co.ke/computer-keyboards/logitech/", "https://www.jumia.co.ke/computer-keyboards/-razer--apple/"]
	# TODO: Write a script to remove the crappy products that have been scraped, from the database
	
	makeup = ["https://www.jumia.co.ke/womens-make-up/la-colour/", "https://www.jumia.co.ke/womens-make-up/maybelline/", "https://www.jumia.co.ke/womens-make-up/focallure/", "https://www.jumia.co.ke/womens-make-up/flori-roberts/", "https://www.jumia.co.ke/womens-make-up/huddah-cosmetics/", "https://www.jumia.co.ke/womens-make-up/kiss-beauty/", "https://www.jumia.co.ke/womens-make-up/loreal/", "https://www.jumia.co.ke/womens-make-up/mary-kay/", "https://www.jumia.co.ke/womens-make-up/nyx/", "https://www.jumia.co.ke/zoya/"]

	maleFragrances = ["https://www.jumia.co.ke/mens-fragrances/david-off/", "https://www.jumia.co.ke/mens-fragrances/calvin-klein/", "https://www.jumia.co.ke/mens-fragrances/issey-miyake/", "https://www.jumia.co.ke/mens-fragrances/hugo-boss/", "https://www.jumia.co.ke/mens-fragrances/versace/", "https://www.jumia.co.ke/mens-fragrances/burberry/", "https://www.jumia.co.ke/mens-fragrances/bvlgari/", "https://www.jumia.co.ke/mens-fragrances/ralph-lauren/", "https://www.jumia.co.ke/mens-fragrances/dunhill/", "https://www.jumia.co.ke/mens-fragrances/mont-blanc/", "https://www.jumia.co.ke/mens-fragrances/azzaro/"]

	femaleFragrances = ["https://www.jumia.co.ke/womens-fragrances/calvin-klein/", "https://www.jumia.co.ke/womens-fragrances/chris-adams/", "https://www.jumia.co.ke/womens-fragrances/elizabeth-arden/", "https://www.jumia.co.ke/womens-fragrances/rasasi/", "https://www.jumia.co.ke/womens-fragrances/chanel/", "https://www.jumia.co.ke/womens-fragrances/beyonce/", "https://www.jumia.co.ke/womens-fragrances/dolce-gabbana/", "https://www.jumia.co.ke/womens-fragrances/victoria-s-secret/", "https://www.jumia.co.ke/womens-fragrances/burberry/", "https://www.jumia.co.ke/womens-fragrances/bvlgari/"]

	skinCare = ["https://www.jumia.co.ke/skin-care-prducts/garnier/", "https://www.jumia.co.ke/skin-care-prducts/loreal/", "https://www.jumia.co.ke/mosara/", "https://www.jumia.co.ke/skin-care-prducts/vaseline/", "https://www.jumia.co.ke/skin-care-prducts/dove1/", "https://jumia.co.ke/skin-care-prducts/mixa/", "https://www.jumia.co.ke/skin-care-prducts/neutrogena/", "https://www.jumia.co.ke/skin-care-prducts/nivea/", "https://www.jumia.co.ke/skin-care-prducts/the-body-shop/", "https://www.jumia.co.ke/skin-care-prducts/st-ives/"]

	device_list = [smartphones, tablets, laptops, tvs, smartwatches, power_banks, chargers, headphones, memory_cards, mice, keyboards, makeup, maleFragrances, femaleFragrances, skinCare]
	device_cat_list = ["smartphones", "tablets", "laptops", "tvs", "smartwatches", "power_banks", "chargers", "headphones", "memory_cards", "mice", "keyboards", "makeup", "maleFragrances", "femaleFragrances", "skinCare"]

	#con = psycopg2.connect(database="jjtestdb", user="postgres", password="hieg") #for local work

	DATABASE_URL = os.environ['DATABASE_URL']
	con =  psycopg2.connect(DATABASE_URL, sslmode='require')

	device_page = []
	j = 0

	with con:

		cur = con.cursor()

		for cat in device_cat_list:
			executionDrop = "DROP TABLE IF EXISTS "+cat
			cur.execute(executionDrop)
			executionCreate = "CREATE TABLE "+cat+"(img_url TEXT, brand TEXT, name TEXT, price TEXT, discount TEXT, link TEXT)"
			cur.execute(executionCreate)
		for device in device_list:	
			for link in device:
				device_page = sapi.storeJumia(link)
				for i in device_page:
						img = imgscraper.JumiaImgScraper(i[5])
						corr_link = urllib.parse.quote((i[5]), safe='')
						corr_link = "https://c.jumia.io/?a=146734&c=9&p=r&E=kkYNyk2M4sk%3D&ckmrdr=" + corr_link + "&utm_campaign=146734"
						executionInsert = "INSERT INTO "+device_cat_list[j]+"(img_url, brand, name, price, discount, link) VALUES(%(url)s, %(br)s, %(nm)s, %(prc)s, %(dnt)s, %(lnk)s)"
						cur.execute(executionInsert, ({"url":img, "br":i[1], "nm":i[2], "prc":i[3], "dnt":i[4], "lnk":corr_link}))
			j = j + 1
	
	cur.execute("UPDATE maleFragrances SET brand = 'Calvin Klein' WHERE brand = 'Calvin Klien'")
	return(print("DB successfully provisioned"))

if __name__ == "__main__": # python modules run when they are imported; the code in this block will not be run when imported
	DatabaseProvisioning()