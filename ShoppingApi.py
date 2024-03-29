"""This is a module that provide Api for ites in stock for choosen kenyan online Malls"""
try:
	import requests, lxml
	from bs4 import BeautifulSoup
except ImportError:
	raise ImportError


def getDigits(extra):

	"""function to remove any other character from a price and return only the digits"""
	try:
		return int(''.join(ele for ele in extra if ele.isdigit()))
	except ValueError:
		return 0



"""A class to parse single item data fetched from jumia website it takes the item to be parsed as its only argument"""
class BaseMalls():
	__secretCount = 0
	
	
	def __count(self):
		self.__secretCount += 1
	 
	
	def __init__(self,single_item):
		"""pass an argument of a single item to be parsed"""
		self.__count()
		pass
		
	
	def itemImage(self):
		"""returns the imageUrl of the items image"""
		pass		
	

	def itemBrand(self):
		"""return the brand of the item"""
		pass

	def imageAlt(self):
		"""return the alt of the image received"""
		pass

	def itemName(self):
		"""return the name of the item"""
		pass


	def  itemPrice(self):
		"""the return price of an item as a double without the currency value"""
		pass

	def itemLink(self):
		"""return the itemLink """
		pass 


"""A class to parse single item data fetched from jumia website it takes the item to be parsed as its only argument"""
class jumia(BaseMalls):
	def __init__(self,single_item):
		super().__init__(single_item)
		self.single_item = single_item
	
	def itemImage(self):
		"""returns the imageUrl of the items image"""
		return self.single_item.find(attrs={"width":"220"})["data-src"]		
	

	def itemBrand(self):
		"""return the brand of the item"""
		return self.single_item.find(attrs={"class":"brand"}).find(text=True).strip()

	def imageAlt(self):
		"""return the alt of the image received"""
		return self.single_item.find(attrs={"class":"image"})["alt"]

	def itemName(self):
		"""return the name of the item"""
		return self.single_item.find(attrs={"class":"name"}).find(text=True).strip()

	def itemDiscount(self):
		"""return the discount on the item"""
		if self.single_item.find(attrs={"class":"sale-flag-percent"}) is None:
			return -1
		else:
			return self.single_item.find(attrs={"class":"sale-flag-percent"}).find(text=True).strip() #removed all the .encode("utf-8") ; these led to the tuple elements to be in binary format

	def  itemPrice(self):
		"""the return price of an item as a double without the currency value"""
		phone_price=self.single_item.find(attrs={"class":"price"}).find(attrs={"dir":"ltr"}).find(text=True)
		return getDigits(phone_price)

	def itemLink(self):
		"""return the itemLink """
		
		return self.single_item.find(attrs={"class":"link"})["href"].strip()


class kilimall(BaseMalls):
	def itemImage(self):
		"""returns the imageUrl of the items image"""
		return self.single_item.find(attrs={"class":"goods-pic"}).find("img")["src"].encode("utf-8")



	def itemName(self):
		"""return the name of the item"""
		return self.single_item.find(attrs={"class":"goods-pic"}).find("img")["title"].encode("utf-8")
	
	def  itemPrice(self):
		"""return the price of the item as a double"""
		phone_price=self.single_item.find(attrs={"class":"sale-price"}).find(text=True)
		return getDigits(phone_price)#
	
	def itemLink(self):
		"""return the image_link of the item"""
		return self.phone_link.strip().encode("utf-8")#




def storeJumia(url):	

	"""Takes a url of a page from jumia and return a list a containing tuples of all items in that page"""
	fetched_items=requests.get(url)
	if fetched_items.status_code!=200:
		
		print("Error getting page: {}.".format(url))
		pass
	try:
		soup=BeautifulSoup(fetched_items.text,"lxml")
		item_list=soup.find_all(attrs={"class":"sku -gallery"})
		offer_list=soup.find_all(attrs={"class":"sku -gallery -has-offers"})
		if item_list!=None and offer_list!=None:
			all_items=item_list+offer_list
	except AttributeError:
		
		raise AttributeError
	
	items=[]
	for i in all_items:
		store=jumia(i)
		# if store.itemDiscount() is None:
		#	single_item=(store.itemImage(),store.itemBrand(),store.imageAlt(),store.itemName(),store.itemPrice(),store.itemLink())	
		# else:
		single_item=(store.itemImage(), store.itemBrand(),store.itemName(), store.itemPrice(), store.itemDiscount(), store.itemLink()) # removed store.imageAlt()
		items.append(single_item)
				
	return items 
def storeKilimall(url):
	"""Takes a url of a page from kilimall and return a list a containing tuples of all items in that page"""
	fetched_items=requests.get(url)
	if fetched_items.status_code!=200:
		print("Error getting page.")
		pass
	try:
		soup=BeautifulSoup(fetched_items.text,"lxml")
		item_list=soup.find("ul",attrs={"class":"list_pic"}).find_all("li",attrs={"class":"item"})
	except AttributeError:
		raise AttributeError
	items=[]
	for i in item_list:
		store=kilimall(i)
		single_item=(store.itemImage(),store.itemAlt(),store.itemName(),store.itemPrice(),store.itemLink())	
		items.append(single_item)
				
	return items


#jumia_gh_comp_acc = storeJumia("https://www.jumia.co.ke/groceries/")

#print(jumia_gh_comp_acc)

#for i in jumia_gh_comp_acc:
#	if i[4] > 200:
#		print("{} {}, price: {} GHS".format(i[1],i[2],i[4]))
