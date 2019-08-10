import os
import psycopg2


DATABASE_URL = os.environ['DATABASE_URL']
#con = psycopg2.connect(database="jjtestdb", user="postgres", password="hieg") #for local work
con =  psycopg2.connect(DATABASE_URL, sslmode='require')
with con:

    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS trained_counter")
    cur.execute("CREATE TABLE trained_counter(counter CHAR(1))")
    cur.execute("INSERT INTO trained_counter VALUES(0)")
    
    # if '0' in count:
    #     print("success")
    # else:
    #     print("fail")

