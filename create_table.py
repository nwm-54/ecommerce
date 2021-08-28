import sqlite3
conn = sqlite3.connect('ecommerce.db')
c = conn.cursor()


# CREATE THE TABLE, NEED TO RUN ONCE ONLY
# c.execute("DROP TABLE accounts")
# c.execute("""CREATE TABLE accounts(
#     email VARCHAR PRIMARY KEY, 
#     password VARCHAR NOT NULL, 
#     orders VARCHAR)""")
# c.execute("INSERT INTO accounts VALUES('kelly@gmail.com','kelly',' ')")
# c.execute("INSERT INTO accounts VALUES('john@gmail.com','john',' ')")
# c.execute("INSERT INTO accounts VALUES('tom@gmail.com','tom',' ')")


# CREATE THE TABLE, NEED TO RUN ONCE ONLY
# c.execute("DROP TABLE items")
# c.execute("""CREATE TABLE items(
#     id int  PRIMARY KEY, 
#     name VARCHAR NOT NULL,
#     description VARCHAR , 
#     ref VARCHAR,
#     price VARCHAR NOT NULL,
#     day_to_arrive INTERGER NOT NULL)""")
# c.execute("INSERT INTO items (id,name, description, ref, price,day_to_arrive) VALUES(1,'Cap','A baseball cap','static/img/products/hat.jpg',15,3)")
# c.execute("INSERT INTO items (id,name, description, ref, price,day_to_arrive) VALUES(2,'Hoodies','A black hooldies','static/img/products/hoodies.jpg',35,4)")
# c.execute("INSERT INTO items (id,name, description, ref, price,day_to_arrive) VALUES(3,'T-shirt','A white shirt','static/img/products/tshirt.jpg',20,5)")
# c.execute("INSERT INTO items (id,name, description, ref, price,day_to_arrive) VALUES(4,'Shoes','A pair of shoes','static/img/products/shoes.jpg',70,6)")

# CREATE THE RATINGS AND REVIEWS TABLE, NEED TO RUN ONCE ONLY
# c.execute("""CREATE TABLE ratings_reviews(
#     id int PRIMARY KEY,
#     product_id int NOT NULL, 
#     account_email VARCHAR NOT NULL,
#     rating INTEGER NOT NULL,
#     review VARCHAR NOT NULL)""")
# c.execute("INSERT INTO ratings_reviews (id, product_id, account_email, rating, review) VALUES(1,'1','john@gmail.com','4','Good cap')")
# c.execute("INSERT INTO ratings_reviews (id, product_id, account_email, rating, review) VALUES(2,'1','kelly@gmail.com','5','Perfect caps for a sunny day')")
# c.execute("INSERT INTO ratings_reviews (id, product_id, account_email, rating, review) VALUES(3,'2','tom@gmail.com','4','Good Hoodies')")
# c.execute("INSERT INTO ratings_reviews (id, product_id, account_email, rating, review) VALUES(4,'2','kelly@gmail.com','5','Perfect hoodies for a sunny day')")
# c.execute("INSERT INTO ratings_reviews (id, product_id, account_email, rating, review) VALUES(5,'3','john@gmail.com','4','Good T-shirt')")
# c.execute("INSERT INTO ratings_reviews (id, product_id, account_email, rating, review) VALUES(6,'3','tom@gmail.com','5','Perfect T-shirt for a hiking')")

# c.execute("INSERT INTO ratings_reviews (product_id, account_email, rating, review) VALUES('1','tom@gmail.com','5','Perfect T-shirt for a hiking in the morning')")

#PRINT ALL AVAILABLE ACCOUNTS
# email = 'kelly@gmail.com'
# a = c.execute("SELECT orders FROM accounts WHERE email=(?)",(email,)).fetchone()
# print(a[0])
# parse_str = a[0]+ '2,2,4/17/2019,4/23/2019,$25 '

#' '+items_cart['id']+'/'+items_cart['count']+'/'+items_cart['ordered_date']+'/'+items_cart['arrived_date']+'/'+items_cart['total']+' '
# c.execute("UPDATE accounts SET orders=(?) WHERE email=(?)",(parse_str, email))
# parse_str = 'QELVAF,1,2,04/21/2021,04/24/2021,$30.00 QELVAF,2,2,04/21/2021,04/25/2021,$70.00 QELVAF,1,2,04/21/2021,04/24/2021,$30.00 QELVAF,2,2,04/21/2021,04/25/2021,$70.00 S90QHE,4,2,04/21/2021,04/27/2021,$140.00 QSNQUN,3,3,04/21/2021,04/26/2021,$60.00 KKSPCK,1,1,05/19/2021,05/22/2021,$15.00 QINDKU,1,2,05/19/2021,05/22/2021,$30.00 E2RU7B,1,6,05/23/2021,05/26/2021,$90.00 E2RU7B,1,6,05/23/2021,05/26/2021,$90.00 VPEMD0,2,10,05/23/2021,05/27/2021,$350.00 63M7CR,1,3,05/31/2021,06/03/2021,$45.00 CVUX8A,3,2,05/31/2021,06/05/2021,$40.00 '
# email = 'kelly@gmail.com'
c.execute("UPDATE accounts SET orders=(?) WHERE email=(?)",(parse_str, email))
a = c.execute("SELECT * FROM accounts ").fetchall()
# email='kelly@gmail.com'
# value = c.execute("SELECT * FROM accounts WHERE email=(?)",(email,)).fetchone()
# columns_name = ['email','password','cart']
# products = []
# item_dict = {}
# for col, data in zip(columns_name, value):
#     item_dict[col] = data
# products.append(item_dict)
# print(products[0]['cart'].split(' '))
print(a)
# value = c.execute("SELECT * FROM ratings_reviews WHERE product_id LIKE ?",(1,)).fetchall()
# rating_sum = 0
# reviews = []
# for re in value:
#     rating_sum += re[-2]
#     reviews.append([re[-3].split('@')[0], re[-1]])
# print(reviews)
# print(rating_sum)

#SAVE TO DB
conn.commit()

#CLOSE
conn.close()

# def add_orders_to_accounts(items_cart, email):
#     print('ADDING ORDERS')
#     print(items_cart)
#     conn = sqlite3.connect('ecommerce.db')
#     c = conn.cursor()
#     prev_orders = c.execute("SELECT orders FROM accounts WHERE email=(?)",(email,)).fetchone()
#     parse_str = str(prev_orders[0])
#     for item in items_cart:
#         print('ITEM', item)
#         print(parse_str)
#         parse_str += str(item['id'])+','+str(item['count'])+','+str(item['ordered_date'])+','+str(item['arrived_date'])+','+str(item['total'])+' '
#     print('FINAL PARSE STR',parse_str)
#     c.execute("UPDATE accounts SET orders=(?) WHERE email=(?)",(parse_str, email))
#     a = c.execute("SELECT orders FROM accounts WHERE email=(?)",(email,)).fetchall()
#     print('FROM DB UPDATE ', a)
#     conn.commit()
#     conn.close()


# items_cart=[{'id': 1, 'name': 'Cap', 'description': 'A baseball cap', 'ref': 'static/img/products/hat.jpg', 'price': '15', 'day_to_arrive': 3, 'count': 2, 'ordered_date': '04/18/2021', 'arrived_date': '04/21/2021', 'total': '$30.00'},{'id': 2, 'name': 'Hoodies', 'description': 'A black hoodies', 'ref': 'static/img/products/hoodies.jpg', 'price': '35', 'day_to_arrive': 4, 'count': 1, 'ordered_date': '04/18/2021', 'arrived_date': '04/21/2021', 'total': '$35.00'}]
# add_orders_to_accounts(items_cart, email)


# conn = sqlite3.connect('ecommerce.db')
# c = conn.cursor()