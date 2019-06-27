try:
    import ShoppingApi
except ImportError:
    raise ImportError

def search_url_generator(search_term, sort="popularity", direction="desc", price, ):
    queryS = search_term.replace(" ", "+")
    fil = user_input_filter.split()

    url = "jumia.com.gh/catalog/?q={}&sort={}&dir={}&{}".format(queryS, sort, direction, price)
    return url

def category_url_generator():
    queryC = 

# i need to take the filter list and pass each item into the url variable. the buttons in the chat interface can have direct values as the payload, e.g. price-discount=50-100

user_input = input("What are you looking for? ")
user_input_sort = input("You can sort by popularity, price (low to hi) and (hi to low): ")
user_input_filter = input("You may choose filters here: ")
print(search_url_generator(search_term=user_input, sort=user_input_sort, filter=user_input_filter))

