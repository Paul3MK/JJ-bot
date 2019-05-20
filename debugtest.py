"""import psycopg2

slot_value = input("What's your choice of smartphone brand? ")

con = psycopg2.connect(database="jjtestdb", user="postgres", password="hieg")
off = 0
with con:

    cur = con.cursor()
    
    for i in range(0, 9):
        cur.execute("SELECT * FROM smartphones WHERE brand=%s LIMIT 1 OFFSET %s", (slot_value, off))
        returned_phone = cur.fetchone()
        off += 1
        if returned_phone == None:
            break
        print("{}\n{}\n{}\n{}\n{}\n{}, it works!!".format(returned_phone[0], returned_phone[1], returned_phone[2], returned_phone[3], returned_phone[4], returned_phone[5]))
"""

brand_dict = {"smartphones":"smartphoneBrand", "tablets":"tabletBrand", "laptops":"laptopBrand", "tvs":"tvBrand", "smartwatches":"smartwatchBrand"}

tCat = ['smartphones', 'tablets', 'laptops', 'tvs', 'smartwatches']

for category in tCat:
    print(brand_dict[category])
