import psycopg2
import urllib.parse
import ShoppingApi as sapi
import imgscrapertest as imgscraper
import os

#smartphones_page1 = [('https://ke.jumia.is/MDoWbVSri14mL5e88fjM6ulsWxY=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/53/264851/1.jpg?5479', 'Huawei', 'P30 Lite, 6.15&quot;, 128GB + 4GB (Dual SIM), Black', 'P30 Lite, 6.15", 128GB + 4GB (Dual SIM), Black', 28999, '-3%', 'https://www.jumia.co.ke/huawei-p30-lite-6.15-128gb-4gb-dual-sim-black-15846235.html'), ('https://ke.jumia.is/EOSbs9th81x2CxL-hupuGeRCypw=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/95/436911/1.jpg?0473', 'Infinix', '', 'Smart 2HD X609, 6",  16GB + 1GB (Dual SIM), Gold', 7999, -1, 'https://www.jumia.co.ke/infinix-smart-2hd-x609-6-16gb-1gb-dual-sim-gold-infinix-mpg135096.html'), ('https://ke.jumia.is/GIyqp_ZFruZqToteeJgVmcMN4NA=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/74/011031/1.jpg?0555', 'Xiaomi', '', 'Redmi Go - 5.0", 4G (8GB+1GB RAM) - (8MP+5MP) Camera,Dual SIM, Black.', 5499, '-35%', 'https://www.jumia.co.ke/redmi-go-5.0-4g-8gb1gb-ram-8mp5mp-cameradual-sim-black.-xiaomi-mpg151735.html'), ('https://ke.jumia.is/apTtqDIcjVN_EPc-y7bAo9G9plI=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/61/120741/1.jpg?8549', 'Infinix', '', 'Hot S3, 5.7", 3GB + 32GB, ( SINGLE SIM), Red.', 9699, '-58%', 'https://www.jumia.co.ke/hot-s3-5.7-3gb-32gb-single-sim-red.-infinix-mpg149391.html'), ('https://ke.jumia.is/ubvmYRaVvRUlQqI1TrTbtWqVHnI=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/34/524821/1.jpg?0034', 'Fourmobile', 'S610 Shine - 5.5&quot; - 3GB + 32GB - 18MP (Dual SIM) - Black', 'S610 Shine - 5.5" - 3GB + 32GB - 18MP (Dual SIM) - Black', 7599, '-37%', 'https://www.jumia.co.ke/fourmobile-s610-shine-5.5-3gb-32gb-18mp-dual-sim-black-12842543.html'), ('https://ke.jumia.is/RoYGnuavuJaJZlXUxHOcSCZ-g6E=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/20/128351/1.jpg?6127', 'Infinix', 'Hot 7 - 6.2&quot; - 1GB RAM -16GB ROM - 13MP+8MP - Dual SIM - Champagne Gold.', 'Hot 7 - 6.2" - 1GB RAM -16GB ROM - 13MP+8MP - Dual SIM - Champagne Gold.', 9399, '-22%', 'https://www.jumia.co.ke/infinix-hot-7-6.2-1gb-ram-16gb-rom-13mp8mp-dual-sim-champagne-gold.-15382102.html'), ('https://ke.jumia.is/M92dYj6F_CkR4idsa_qFJDm6BQ0=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/37/411801/1.jpg?6937', 'Xiaomi', '', 'Redmi 6, 5.45", 4G, 64GB + 3GB (Dual SIM), Gold', 11999, '-48%', 'https://www.jumia.co.ke/redmi-6-5.45-4g-64gb-3gb-ram-fingerprint-sensor-125-mp-rear-back-camera-dual-sim-gold-xiaomi-mpg133111.html'), ('https://ke.jumia.is/q-4lBdfAcwk8LhpiNtGb-6SXyjQ=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/48/01439/1.jpg?9004', 'Xiaomi', '', 'Redmi 6A, 5.45" - (16GB+2GB RAM) - 13 MP Camera (Dual SIM), 4G Black', 7999, '-43%', 'https://www.jumia.co.ke/redmi-6a-4g-smartphone-android-8.1-helio-a22-quad-core-2gb-ram-16gb-rom-black-xiaomi-mpg125823.html'), ('https://ke.jumia.is/cPivCxX6CCWlJcjccS-x29cOU4o=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/69/299541/1.jpg?4774', 'Infinix', 'HOT 7 - 32GB - 2GB, 6.2&quot;, 13MP, 4000mAh, Dual SIM Quad-Core 1.3GHz Processor - Black', 'HOT 7 - 32GB - 2GB, 6.2", 13MP, 4000mAh, Dual SIM Quad-Core 1.3GHz Processor - Black', 11899, '-41%', 'https://www.jumia.co.ke/hot-7-32gb-2gb-6.2-13mp-4000mah-dual-sim-quad-core-1.3ghz-processor-black-infinix-mpg151689.html'), ('https://ke.jumia.is/EGMENw-UzAlmU8Lem6I41kCWi8Q=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/95/646911/1.jpg?5168', 'Nokia', '3.1 - 5.2&quot;,2GB RAM, 16GB ROM-,Android v8.0 Oreo, Dual SIM - 13MP + 8MP - White', '3.1 - 5.2",2GB RAM, 16GB ROM-,Android v8.0 Oreo, Dual SIM - 13MP + 8MP - White', 9399, '-41%', 'https://www.jumia.co.ke/nokia-3.1-5.22gb-ram-16gb-rom-android-v8.0-oreo-dual-sim-13mp-8mp-white-11964659.html'), ('https://ke.jumia.is/a4XdE90BAGAzsvLBJpH9sgStSKY=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/40/487041/1.jpg?4627', 'Huawei', '', 'Honor 7S 5.45" 2GB +16GB 3020mAh Dual SIM Smartphone - Black', 8799, '-27%', 'https://www.jumia.co.ke/huawei-honor-7s-5.45-2gb-16gb-3020mah-dual-sim-smartphone-black-14078404.html'), ('https://ke.jumia.is/Z3r3FWjDZrDTMXKHHdjgLgsrUk0=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/71/945951/1.jpg?7568', 'Gionee', 'S11 Lite - 5.7&quot;, 64GB, 4GB RAM, 16MP+13MP, Dual SIM, Black', 'S11 Lite - 5.7", 64GB, 4GB RAM, 16MP+13MP, Dual SIM, Black', 13499, '-21%', 'https://www.jumia.co.ke/gionee-s11-lite-5.7-64gb-4gb-ram-16mp13mp-dual-sim-black-15954917.html'), ('https://ke.jumia.is/KO8JNnvFTYHKtOFeeRcmq8skt6Q=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/35/337141/1.jpg?3625', 'Honor', '8x 6.5-Inch (4GB, 128GB ROM), Dual 20MP + 16MP Dual SIM - Black.', '8x 6.5-Inch (4GB, 128GB ROM), Dual 20MP + 16MP Dual SIM - Black.', 24999, '-29%', 'https://www.jumia.co.ke/honor-8x-6.5-inch-4gb-128gb-rom-dual-20mp-16mp-dual-sim-black.-14173353.html'), ('https://ke.jumia.is/5IQutfwrd4uLOR6sQIWKWxxHPJk=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/94/907441/1.jpg?4766', 'OPPO', 'A3s, 2GB +16GB (Dual SIM), Purple..', 'A3s, 2GB +16GB (Dual SIM), Purple..', 12499, '-26%', 'https://www.jumia.co.ke/a3s-2gb-16gb-dual-sim-purple-oppo-mpg118409.html'), ('https://ke.jumia.is/uQKYp7InRFdCBuoiZ400-btVReg=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/99/520441/1.jpg?0912', 'Huawei', 'Y6 Prime 2019, 6.09&#039;&#039;, 32GB, 13MP(f/1.8) Camera, Android 9.0, Sapphire Blue', "Y6 Prime 2019, 6.09'', 32GB, 13MP(f/1.8) Camera, Android 9.0, Sapphire Blue", 13499, '-12%', 'https://www.jumia.co.ke/y6-prime-2019-6.09-32gb-13mpf1.8-camera-android-9.0-sapphire-blue-huawei-mpg147349.html'), ('https://ke.jumia.is/ku1PNRfpDDqBQTWcgl4hQYO3sQY=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/98/183131/1.jpg?9667', 'TECNO', 'Camon 11, 32GB+3GB, 4GLTE (Dual SIM), Black + Free OTG Cable', 'Camon 11, 32GB+3GB, 4GLTE (Dual SIM), Black + Free OTG Cable', 14300, '-27%', 'https://www.jumia.co.ke/camon-11-32gb3gbram-4glte-6.2-16mp-dual-sim-black-free-otg-cable.-tecno-mpg130185.html'), ('https://ke.jumia.is/eVdpjmGQX47plVOipdUCirvOJ-w=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/21/286341/1.jpg?5569', 'Oukitel', '', 'C12 Pro, 6.18" ,16GB + 2GB RAM, (Dual SIM) Black', 6859, '-38%', 'https://www.jumia.co.ke/c12-pro-6.18-16gb-2gb-dual-sim-4g-black-oukitel-mpg151905.html'), ('https://ke.jumia.is/bQp8Bu4G2-dch_ExR3zg3kBy-Nw=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/66/500151/1.jpg?0567', 'Samsung', 'Galaxy A50 - 128GB Rom - 4GB Ram, 4000mAh, Dual SIM 4G -Blue', 'Galaxy A50 - 128GB Rom - 4GB Ram, 4000mAh, Dual SIM 4G -Blue', 29787, '-15%', 'https://www.jumia.co.ke/galaxy-a50-128gb-rom-4gb-ram-4000mah-dual-sim-4g-blue-samsung-mpg151241.html'), ('https://ke.jumia.is/CJGAqRLJdQJnssoppIge9sF1_rk=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/52/017441/1.jpg?7399', 'X-TIGI', 'V5 - 4.0&quot; - 8GB+1GB - Android 8.1- Dual SIM- Black', 'V5 - 4.0" - 8GB+1GB - Android 8.1- Dual SIM- Black', 3499, '-30%', 'https://www.jumia.co.ke/v5-4.0-8gb1gb-android-8.1-dual-sim-black-x-tigi-mpg130225.html'), ('https://ke.jumia.is/T0_RPsNSuALY4qnI9OUo8W86eJ0=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/10/32385/1.jpg?3152', 'Cubot', 'J3 - 16GB - 1GB RAM - 8MP Camera - Dual Sim - 3G - Black', 'J3 - 16GB - 1GB RAM - 8MP Camera - Dual Sim - 3G - Black', 4999, '-38%', 'https://www.jumia.co.ke/j3-16gb-1gb-ram-8mp-camera-dual-sim-3g-black-cubot-mpg120875.html'), ('https://ke.jumia.is/lmpbYHcovPiIhGu1crlDI0grMfg=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/49/35359/1.jpg?6502', 'X-TIGI', 'V15, 5.0&quot;, 16GB  + 1GB (Dual SIM), Gold', 'V15, 5.0", 16GB  + 1GB (Dual SIM), Gold', 4599, '-43%', 'https://www.jumia.co.ke/v15-5.0-16gb1gb-android-8.1-5mp-camera-dual-sim-gold-x-tigi-mpg124487.html'), ('https://ke.jumia.is/ZfXO_2ZgW40G5VRlbz-a1UYnw_4=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/31/990541/1.jpg?6482', 'TECNO', 'Spark 2, 16GB, 1GB RAM, 13MP Camera (Dual SIM) Midnight Black', 'Spark 2, 16GB, 1GB RAM, 13MP Camera (Dual SIM) Midnight Black', 9299, -1, 'https://www.jumia.co.ke/spark-2-16gb-1gb-ram-13mp-camera-dual-sim-champagne-gold-tecno-mpg111845.html'), ('https://ke.jumia.is/STCLjhR9uuTGBl1SW1qt9SKkvJk=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/78/613701/1.jpg?8318', 'Huawei', '', 'Y5 Prime 2018 - 5.45" - 16GB - 2GB RAM - 13MP Camera (Dual SIM) - Gold', 9199, '-29%', 'https://www.jumia.co.ke/y5-prime-2018-5.45-16gb-2gb-ram-13mp-camera-dual-sim-gold-huawei-mpg112442.html'), ('https://ke.jumia.is/dio4BcNJ0qZG-qDtiBKkFEd_RwQ=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/96/831541/1.jpg?7041', 'Samsung', '', 'Galaxy J4 Core, 16GB+1GB  (Dual SIM), Black', 10499, '-34%', 'https://www.jumia.co.ke/galaxy-j4-core-16gb1gb-dual-sim-black-samsung-mpg149438.html'), ('https://ke.jumia.is/AXII0zUIVOb9dj-WLkbAGV1VPZE=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/81/142501/1.jpg?2438', 'Huawei', 'Y9 (2019) - 6.5&quot; - 64GB - 4GB RAM - 16MP+2MP Dual Camera, 4G (Dual SIM) +suprise gift', 'Y9 (2019) - 6.5" - 64GB - 4GB RAM - 16MP+2MP Dual Camera, 4G (Dual SIM) +suprise gift', 21399, '-21%', 'https://www.jumia.co.ke/y92019-6.5-64gb-4gb-ram-16mp2mpdual-sim-black-huawei-mpg123767.html'), ('https://ke.jumia.is/c8k6Ncq7__-jeqIlLE6A2I0Ks74=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/80/020801/1.jpg?7183', 'Nokia', '2.1, 5.5&quot; (8GB+1GB RAM) 8MP Camera, Dual SIM (4G) - Blue Silver', '2.1, 5.5" (8GB+1GB RAM) 8MP Camera, Dual SIM (4G) - Blue Silver', 7999, '-20%', 'https://www.jumia.co.ke/2.1-5.5-8gb1gb-ram-8mp-camera-dual-sim-4g-blue-silver-nokia-mpg121899.html'), ('https://ke.jumia.is/y18oR47ATqlwPsDFXXEQGRLE92I=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/99/41126/1.jpg?5298', 'Ulefone', 'S9 Pro - 5.5&quot; - 16GB - 2GB RAM - (13MP+5MP) Dual Camera, 4G (Dual SIM), Black', 'S9 Pro - 5.5" - 16GB - 2GB RAM - (13MP+5MP) Dual Camera, 4G (Dual SIM), Black', 7699, '-33%', 'https://www.jumia.co.ke/s9-pro-5.5-16gb-2gb-ram-13mp5mp-dual-camera-4g-dual-sim-black-ulefone-mpg147059.html'), ('https://ke.jumia.is/yHz3AneBgVe6OBnXa_pnGDt6meo=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/99/75628/1.jpg?6291', 'Nokia', '1 - 8GB - 1GB RAM - Dual SIM - Dark Blue', '1 - 8GB - 1GB RAM - Dual SIM - Dark Blue', 5499, '-31%', 'https://www.jumia.co.ke/1-8gb-1gb-ram-dual-sim-dark-blue-nokia-mpg123346.html'), ('https://ke.jumia.is/6e0tiOAtth0xha2XaS7Rx47sfWw=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/14/259061/1.jpg?6055', 'Nokia', '5.1 - 5.5&quot; HD+  - 16 GB - 2 GB RAM - Black.', '5.1 - 5.5" HD+  - 16 GB - 2 GB RAM - Black.', 14000, -1, 'https://www.jumia.co.ke/5.1-plus-5.8-hd-32-gb-3-gb-ram-black-nokia-mpg127408.html'), ('https://ke.jumia.is/sieWgpvI9dXBiHpKiegUPs-nQzo=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/79/363901/1.jpg?9827', 'Ulefone', '', 'S10 Pro - 5.7" - 16GB - 2GB RAM, 4G LTE (Dual SIM), Black', 7999, '-27%', 'https://www.jumia.co.ke/s10-pro-5.7-16gb-2gb-ram-4g-lte-dual-sim-black-ulefone-mpg134964.html'), ('https://ke.jumia.is/n5XAaYehtXhuxn42BpbE-eEH7Yc=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/68/369641/1.jpg?0473', 'Infinix', '', 'Smart 2HD X609, 6", 16GB + 1GB (Dual SIM), Black', 7999, -1, 'https://www.jumia.co.ke/smart-2hd-x609-6-16gb-1gb-dual-sim-black-infinix-mpg131954.html'), ('https://ke.jumia.is/RNntO4nHnN0NizJYVtUcnvI93YE=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/89/696701/1.jpg?6892', 'Infinix', 'Smart 2, 5.5&quot;, 16GB, 1GB RAM, 13MP Camera, 4G, Dual SIM - Serene Gold', 'Smart 2, 5.5", 16GB, 1GB RAM, 13MP Camera, 4G, Dual SIM - Serene Gold', 8599, '-28%', 'https://www.jumia.co.ke/smart-2-5.5-16gb-1gb-ram-13mp-camera-4g-dual-sim-gold-infinix-mpg123674.html'), ('https://ke.jumia.is/9ZzOlvryug5RpZ_aGiGGTTePnxY=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/88/613701/1.jpg?6562', 'Huawei', '', 'Y5 Prime 2018, 5.45", 16GB + 2GB, (Dual SIM) - Blue.', 9199, '-29%', 'https://www.jumia.co.ke/y5-prime-2018-16gb-2gb-dual-sim-blue-huawei-mpg116297.html'), ('https://ke.jumia.is/e6DMeRcP8A6eD7Dw9onF1TzRDt4=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/58/966701/1.jpg?0949', 'Huawei', '', 'Y9 (2019), 64GB + 4GB, 4G (Dual SIM), Blue + Surprise Gift', 21499, '-17%', 'https://www.jumia.co.ke/y9-2019-6.5-64gb-4gb-ram-16mp2mp-dual-camera-4g-dual-sim-blue-suprise-gift.-huawei-mpg147068.html'), ('https://ke.jumia.is/HK0wA8EJZeg8cN0MGYVgAzBtpD0=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/98/613701/1.jpg?3626', 'Huawei', '', 'Y7 Prime (2018) 5.99" - 3GB + 32GB, (Dual SIM) -Blue', 13999, '-26%', 'https://www.jumia.co.ke/y7-prime-2018-5.99-3gb-ram-32gb-rom-camera-13-mp-dual-sim-blue-huawei-mpg131424.html'), ('https://ke.jumia.is/2F8dcH6lcghNHfg-5O3g4aCjJj8=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/74/907441/1.jpg?4766', 'OPPO', 'A3s, 2GB +16GB (Dual SIM)  - Red', 'A3s, 2GB +16GB (Dual SIM)  - Red', 12499, '-31%', 'https://www.jumia.co.ke/a3s-2gb-16gb-dual-sim-red-oppo-mpg118408.html'), ('https://ke.jumia.is/5wgtjcNHSHlDe-_VCYWDuoj2nJA=/fit-in/220x220/filters:fill(white):sharpen(1,0,false):quality(100)/product/29/613701/1.jpg?6491', 'Huawei', '', 'Y5 Prime 2018, 5.45", 16GB+2GB, (Dual SIM), Black.', 9199, '-29%', 'https://www.jumia.co.ke/y5-prime-2018-5.45-16gb-2gb-ram-13mp-camera-4g-dual-sim-black-huawei-mpg124392.html')]

def DatabaseProvisioning():
	smartphones = ["https://www.jumia.co.ke/mobile-phones/samsung/", "https://www.jumia.co.ke/mobile-phones/huawei/",	"https://www.jumia.co.ke/mobile-phones/apple/",	"https://www.jumia.co.ke/android-phones/nokia_1/?price=7000-97011",	"https://www.jumia.co.ke/mobile-phones/tecno/?sort=Price%3A%20High%20to%20Low&dir=desc",	"https://www.jumia.co.ke/mobile-phones/oppo/", "https://www.jumia.co.ke/mobile-phones/infinix/", "https://www.jumia.co.ke/smartphones/xiaomi/", "https://www.jumia.co.ke/smartphones/sony/"]
	tablets = ["https://www.jumia.co.ke/tablets/apple/?price=5000-117700", "https://www.jumia.co.ke/tablets/samsung/", "https://www.jumia.co.ke/tablets/huawei/", "https://www.jumia.co.ke/tablets/lenovo/", "https://www.jumia.co.ke/tablets/amazon/"]
	laptops = ["https://www.jumia.co.ke/laptops/dell/?sort=Price%3A%20High%20to%20Low&dir=desc", "https://www.jumia.co.ke/laptops/apple/", "https://www.jumia.co.ke/laptops/brand-asus/", "https://www.jumia.co.ke/laptops/hp/", "https://www.jumia.co.ke/laptops/lenovo/"]
	tvs = ["https://www.jumia.co.ke/televisions/sony/", "https://www.jumia.co.ke/televisions/samsung/", "https://www.jumia.co.ke/televisions/tcl/", "https://www.jumia.co.ke/televisions/lg/", "https://www.jumia.co.ke/televisions/skyworth/", "https://www.jumia.co.ke/televisions/hisense/", "https://www.jumia.co.ke/televisions/nasco/", "https://www.jumia.co.ke/televisions/haier--mooka", "https://www.jumia.co.ke/televisions/syinix/", "https://www.jumia.co.ke/televisions/vision-plus/"]
	smartwatches = ["https://www.jumia.co.ke/smart-watches/apple", "https://www.jumia.co.ke/smart-watches/huawei", "https://www.jumia.co.ke/smart-watches/mi", "https://www.jumia.co.ke/smart-watches/lenovo"]

	device_list = [smartphones, tablets, laptops, tvs, smartwatches]
	device_cat_list = ["smartphones", "tablets", "laptops", "tvs", "smartwatches"]

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
			fields = ("img_url", "brand", "name", "price", "discount", "link")
		for device in device_list:	
			for link in device:
				device_page = sapi.storeJumia(link)
				for i in device_page:
						#img = imgscraper.JumiaImgScraper(i[5])
						#corr_link = urllib.parse.quote((i[5]), safe='')
						#corr_link = "https://c.jumia.io/?a=146734&c=9&p=r&E=kkYNyk2M4sk%3D&ckmrdr=" + corr_link + "&utm_campaign=146734"
						executionInsert = "INSERT INTO "+device_cat_list[j]+"(img_url, brand, name, price, discount, link) VALUES(%(url)s, %(br)s, %(nm)s, %(prc)s, %(dnt)s, %(lnk)s)"
						cur.execute(executionInsert, ({"url":i[0], "br":i[1], "nm":i[2], "prc":i[3], "dnt":i[4], "lnk":i[5]}))
			j = j + 1

DatabaseProvisioning()

		
		



