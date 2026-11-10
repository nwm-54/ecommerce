import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

#add new account to accounts table
def add_account(email, password):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute("INSERT INTO accounts VALUES (?,?,?)",(email, generate_password_hash(password),''))
    conn.commit()
    conn.close()
def account_retrieve_password(email):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    pw = c.execute("SELECT password FROM accounts WHERE email=(?)",(email,)).fetchone()
    conn.commit()
    conn.close()
    if pw is None:
        return None
    return pw[0]
#Return True when the password matches the salted hash stored for this email
def verify_account(email, password):
    stored = account_retrieve_password(email)
    if stored is None:
        return False
    return check_password_hash(stored, password)
#Check if registered email is already exist - cannot have duplicate email in database
def account_check_exist(email):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    email = c.execute("SELECT email FROM accounts WHERE email=(?)",(email,)).fetchone()
    conn.commit()
    conn.close()
    return True if email is not None else False
#Update password for account
def account_update_password(email, new_password):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute("UPDATE accounts SET password=(?) WHERE email=(?)",(generate_password_hash(new_password), email))
    conn.commit()
    conn.close()
def cancel_orders_from_accounts(email, order_number, item_id):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    prev_orders = c.execute("SELECT orders FROM accounts WHERE email=(?)",(email,)).fetchone()    
    removed_order = ''
    parse_str = str(prev_orders[0]).strip().split(' ')
    for index_order, order in enumerate(parse_str):
        if order_number == str(order.split(',')[0]) and item_id == str(order.split(',')[1]):
            removed_order = parse_str.pop(index_order)
            parse_str_update = ' '.join(parse_str)
            c.execute("UPDATE accounts SET orders=(?) WHERE email=(?)",(parse_str_update, email))
            break
    conn.commit()
    conn.close()
    return removed_order

def add_orders_to_accounts(items_cart, email):
    print('ADDING ORDERS')
    print(items_cart)
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    prev_orders = c.execute("SELECT orders FROM accounts WHERE email=(?)",(email,)).fetchone()
    parse_str = str(prev_orders[0])
    for item in items_cart:
        if parse_str[-1] != ' ':
            parse_str += ' '
        parse_str += str(item['order_number'])+','+ str(item['id'])+','+str(item['count'])+','+str(item['ordered_date'])+','+str(item['arrived_date'])+','+str(item['total'])+' '
    c.execute("UPDATE accounts SET orders=(?) WHERE email=(?)",(parse_str, email))
    a = c.execute("SELECT orders FROM accounts WHERE email=(?)",(email,)).fetchall()
    conn.commit()
    conn.close()
def products_get_id_from_name(name):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    item_id = c.execute("SELECT id FROM items WHERE name=(?)",(name,)).fetchone()
    conn.commit()
    conn.close()
    return item_id
def retrieve_prev_orders_from_accounts(email):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    orders = c.execute("SELECT orders FROM accounts WHERE email=(?)",(email,)).fetchone()
    conn.commit()
    conn.close()
    items = []
    orders = orders[0].strip().split(' ')
    for order in orders:
        if len(order)>1:
            item = {}
            item['order_number'], item['id'], item['count'], item['ordered_date'], item['arrived_date'], item['total'] = order.split(',')
            # print(retrieve_products_by_id(item['id'])['ref'])
            item['ref'] = retrieve_products_by_id(item['id'])['ref']
            item['name'] = retrieve_products_by_id(item['id'])['name']
            items.append(item)
    return items
#look up account in accounts table
#return email, password if exists
def retrieve_account(email, password):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    acc = c.execute("SELECT * FROM accounts WHERE email=(?)",(email,)).fetchall()
    conn.commit()
    conn.close()
    if acc:
        return acc[0][0], acc[0][1] #email, password
    return None, None #email not exist in the table
def products_add_user_review(email, product_id, rating, review): 
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute("INSERT INTO ratings_reviews (product_id, account_email, rating, review) VALUES(?,?,?,?)", (product_id, email, rating, review))
    conn.commit()
    conn.close()

#retrieve all available products in items table
#return a list of key-value pair products
def retrieve_all_products():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    values = c.execute("SELECT * FROM items ").fetchall()
    columns_name = ['id','name','description','ref','price','days_to_arrive']
    products = []
    for value in values:
        item_dict = {}
        for col, data in zip(columns_name, value):
            item_dict[col] = data
        products.append(item_dict)
    conn.commit()
    conn.close()
    return products

def retrieve_account_by_email(email):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    value = c.execute("SELECT * FROM accounts WHERE email=(?)",(email,)).fetchone()
    columns_name = ['email','password','orders']
    products = []
    item_dict = {}
    for col, data in zip(columns_name, value):
        item_dict[col] = data
    products.append(item_dict)
    conn.commit()
    conn.close()
    return products
#retrieve products by search key
#return a list of key-value pair products
def retrieve_products_by_key(key):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    values = c.execute("SELECT * FROM items WHERE LOWER(name) LIKE ?",('%'+key.lower()+'%',)).fetchall()
    columns_name = ['id','name','description','ref','price']
    products = []
    for value in values:
        item_dict = {}
        for col, data in zip(columns_name, value):
            item_dict[col] = data
        products.append(item_dict)
    conn.commit()
    conn.close()
    return products

def retrieve_products_by_name(name):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    value = c.execute("SELECT * FROM items WHERE name LIKE ?",(name,)).fetchone()
    columns_name = ['id','name','description','ref','price', 'day_to_arrive']
    item_dict = {}
    for col, data in zip(columns_name, value):
        item_dict[col] = data
    conn.commit()
    conn.close()
    return item_dict

#look up for a product by id
#return a lkey-value pair product
def retrieve_products_by_id(id):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    value = c.execute("SELECT * FROM items WHERE id LIKE ?",(id,)).fetchone()
    print(value)
    columns_name = ['id','name','description','ref','price']
    item_dict = {}
    for col, data in zip(columns_name, value):
        item_dict[col] = data
    conn.commit()
    conn.close()
    return item_dict

def get_ratings_reviews_by_id(id):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    value = c.execute("SELECT * FROM ratings_reviews WHERE product_id LIKE ?",(id,)).fetchall()
    if len(value)==0:
        return 0, [[]]
    # columns_name = ['id', 'product_id', 'account_email', 'rating', 'review']
    rating_sum = 0
    reviews = []
    for re in value:
        rating_sum += re[-2]
        reviews.append([re[-3].split('@')[0], re[-1]])
    return rating_sum/len(value), reviews


#Return True when the value is a werkzeug password hash, not a clear-text password
def _is_password_hash(value):
    return value.split(':', 1)[0] in ('pbkdf2', 'scrypt')

#Create the tables and seed the product catalog when the database is new.
#No account row is seeded, so the repository holds no account password.
def init_db():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS accounts(
        email VARCHAR PRIMARY KEY,
        password VARCHAR NOT NULL,
        orders VARCHAR)""")
    c.execute("""CREATE TABLE IF NOT EXISTS items(
        id int PRIMARY KEY,
        name VARCHAR NOT NULL,
        description VARCHAR,
        ref VARCHAR,
        price VARCHAR NOT NULL,
        day_to_arrive INTERGER NOT NULL)""")
    c.execute("""CREATE TABLE IF NOT EXISTS ratings_reviews(
        id int PRIMARY KEY,
        product_id int NOT NULL,
        account_email VARCHAR NOT NULL,
        rating INTEGER NOT NULL,
        review VARCHAR NOT NULL)""")
    if c.execute("SELECT COUNT(*) FROM items").fetchone()[0] == 0:
        c.executemany("INSERT INTO items (id,name,description,ref,price,day_to_arrive) VALUES(?,?,?,?,?,?)", [
            (1, 'Cap', 'A baseball cap', 'static/img/products/hat.jpg', 15, 3),
            (2, 'Hoodies', 'A black hooldies', 'static/img/products/hoodies.jpg', 35, 4),
            (3, 'T-shirt', 'A white shirt', 'static/img/products/tshirt.jpg', 20, 5),
            (4, 'Shoes', 'A pair of shoes', 'static/img/products/shoes.jpg', 70, 6),
        ])
    #Move any clear-text password written by an older version to a salted hash
    for email, password in c.execute("SELECT email, password FROM accounts").fetchall():
        if not _is_password_hash(password):
            c.execute("UPDATE accounts SET password=(?) WHERE email=(?)", (generate_password_hash(password), email))
    conn.commit()
    conn.close()

init_db()
