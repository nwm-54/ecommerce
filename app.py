from flask import Flask, render_template, jsonify, request, url_for, session, redirect
import database as db
from datetime import date, time, datetime,timedelta  
import math
import random
import string
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
PORT = 3000
app = Flask(__name__)
app._static_folder='static/'
app.secret_key = "super secret key"
items_cart2 = []

#EMAIL AND PASSWORD FOR ECOMMERCE STORE GMAIL ACCOUNT - FOR SENDING EMAIL TO CUSTOMER
sender = 'ecommerce220.spring2021@gmail.com'
sender_password = 'ecommerce220'

#IMPLEMENT INDEX PAGE
@app.route("/", methods=["GET","POST"])
def index():
    print('from index')
    if request.method == "POST":
        # IMPLEMENT SEARCH
        # if 'search' in request.form:
        key = request.form['search']
        search_products = db.retrieve_products_by_key(key)
        
        return render_template("index.html", products = search_products, login=session['login_status'], cart_item=[])
    else:
        #IF NO SEARCH KEY, DISPLAY ALL PRODUCTS
        session['all_products'] = db.retrieve_all_products()
        #view as guest
        if 'email' not in session:
            session['login_status'] = False
            return render_template("index_guest.html",products = session['all_products'],login=session['login_status'], cart_item=[])
        else:
            #view as member
            session['login_status'] = True
        return render_template("index.html",products = session['all_products'],login=session['login_status'], cart_item=[])
#ABOUT US PAGE
@app.route('/about_us', methods=['GET'])
def about_us():
    return render_template('about_us.html')
#IMPLEMENT SEE ORDERS HISTORY
@app.route("/previous_orders", methods=['GET', "POST"])
def previous_orders():
    orders = db.retrieve_prev_orders_from_accounts(session['email'])
    today = date.today().strftime("%m/%d/%Y")
    print(orders)
    for order in orders:
        delivery_date = order['arrived_date']
        if today>delivery_date:
            order['status'] = 1 #delivered
        else:
            order['status'] = 0 #not yet
    return render_template("previous_orders.html", asd=orders)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
def send_email_protocol(sender, sender_password, receiver, message):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender, sender_password)  
    s.sendmail(sender, receiver, message.as_string())
    s.quit()
#SENDING PASSWORD RECOVERY EMAIL
def send_password_recovery_email(user_email):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Recovery"
    message["From"] = sender
    user_email = 'thanhngocnguyentuong@gmail.com'
    message["To"] = user_email
    code = id_generator(size=20)
    url = 'http://localhost:{}/password_recovery/{}'.format(PORT, code)
    session['code'] = code
    html = """\
    <html>
    <body style="max-width: 300px;margin: auto;">
        <p> Follow the following link to reset your password</p>
        <a href="{}">{}</a>
    </body>
    </html>
    """.format(url, url)
    part2 = MIMEText(html, "html")
    message.attach(part2)
    send_email_protocol(sender, sender_password, user_email, message)
#SENDING ORDER CONFIRMATION EMAIL
def send_confirm_email(user_email, asd):
    print('in send confirm email')
    message = MIMEMultipart("alternative")
    message["Subject"] = "Order confirmation"
    message["From"] = sender
    message["To"] = user_email
    items = []
    for img_count,item in enumerate(asd):
        img_ref = './'+item['ref'].replace('\\','/')
        fp = open(img_ref, 'rb')
        msgImage = MIMEImage(fp.read(), _subtype='jpg')
        fp.close()
        msgImage.add_header('Content-ID', '<{}>'.format(img_count))
        message.attach(msgImage)
        items.append('<tr ;margin: auto;"><h4>Order Number <b>{}</b></h4><img src=cid:{} alt="Denim Jeans" style="width:100%;border-radius: 3px;"><h2 style="color:black;margin=0; text-align=center;">{}</h2><p stype="font-size=1em;color: black;margin=0px;">Quantity: {}</p><p style="color: black;font-size: 0.65em;margin=0;">Total ${}.00</p><p><button style="border: none;outline: 0;border-radius: 3px;background: #66d7d7;color: white;text-align: center;cursor: pointer;width: 100%;font-size: 1em;">Arrived on {}</button></p> </tr>'.format(item['order_number'], img_count, item['name'], item['count'], item['total'], item['arrived_date']))
    items = ''.join(items)
    html = """\
    <html>
    <body style="max-width: 300px;margin: auto;">
        <h3> Thank you for purchasing from our store </h3>
        <table>
            <tbody>{}</tbody>
        </table>
    </body>
    </html>
    """.format(items)
    part2 = MIMEText(html, "html")
    message.attach(part2)
    print('sending email to {} CONTENT {}'.format(user_email, items))
    send_email_protocol(sender, sender_password, user_email, message)
    print('done sending confirm email')

#IMPLEMENT CHECKOUT/TRACKING
@app.route("/checkout", methods=['GET', "POST"])
def checkout():
    print('in checkout')
    print(request.method)
    if request.method == 'POST':
        print('POST at checkout')
        order_number = id_generator()
        if request.json is not None:
            shopping_cart = request.json
            for item in shopping_cart:
                item_dict = db.retrieve_products_by_name(item['name'])
                item_dict['order_number'] = order_number
                item_dict['count'] = item['count']
                item_dict['ordered_date'] = date.today().strftime("%m/%d/%Y")
                datetime_arrive = date.today() + timedelta(days=item_dict['day_to_arrive'])
                item_dict['arrived_date'] = datetime_arrive.strftime("%m/%d/%Y")
                item_dict['total'] = '$'+item['total']
                global items_cart2
                items_cart2.append(item_dict)
            session['shopping_cart'] = items_cart2
            db.add_orders_to_accounts(items_cart2, session['email'])

            #sending confirm email
            send_confirm_email(session['email'],session['shopping_cart'])
            return render_template("checkout.html", asd=session['shopping_cart'])
    return render_template("checkout.html", asd=items_cart2)

#CANCEL ORDERS
@app.route("/cancel_orders", methods=["POST"])
def cancel_orders():
    if request.method =='POST':
        item_id = db.products_get_id_from_name(request.json['item_name'])[0]
        removed_order = db.cancel_orders_from_accounts(session['email'], str(request.json['order_number']), str(item_id))
        print('delete order ', request.json['order_number'], request.json['item_name'])
    return redirect(url_for('previous_orders'))
#IMPLEMENT LOGOUT
@app.route("/logout", methods=["GET","POST"])
def logout():
    print('user loggout')
    if 'email' in session:
            session.pop('email', None)
    if 'shopping_cart' in session:
        session.pop('shopping_cart', None)
    session['login_status'] = False
    return redirect(url_for('index', products=session['all_products'] ))

#IMPLEMENT REGISTRATION
@app.route("/register", methods=["GET","POST"])
def register_form():
    if request.method == "POST":
        email_inp = request.form.get("email")
        password_inp = request.form.get("password")
        if len(email_inp) == 0 or len(password_inp) == 0 :
            return render_template("register.html", message="missing_info")

        email_check, password_check = db.retrieve_account(email_inp, password_inp)

        if email_check is not None:
            return render_template("register.html", message="email_exists")
        else:
            db.add_account(email_inp, password_inp)
            session['email'] = email_inp
            session['login_status'] = True
            return redirect(url_for('index', login=True))
            # return render_template("index.html")
    else:
        return render_template("register.html", message="")

#WHEN USERS FORGET PASSWORD
@app.route("/password_recovery/<string:code>", methods=['GET', 'POST'])
def password_recovery(code):
    print('session ', session)
    if code == session['code'] and 'email_forgot_pwd' in session:
        old_password = db.account_retrieve_password(session['email_forgot_pwd'])
        print('request method from pass recovery ', request.method)
        if request.method == "GET":
            return render_template('password_reset.html', user_email=session['email_forgot_pwd'], old_password=old_password)
        # else:#if request.method =='POST':
        new_password = request.form.get("password")
        db.account_update_password(session['email_forgot_pwd'], new_password)
        print('password upate from {} to {}'.format(old_password, new_password))
        print(session['email']+' login successfully')
        session['email'] = session['email_forgot_pwd']
        session['login_status'] = True
        return redirect(url_for('index',products=session['all_products'] ))
    return render_template('forgot_password.html', message='Error')
            
#IMPLEMENT LOGIN
@app.route("/login", methods=["GET","POST"])
def login_form():
    if request.method == "POST":
        email_inp = request.form.get("email")
        if 'login' in request.form:
            print('in login')
            password_inp = request.form.get("password")
            email_check, password_check = db.retrieve_account(email_inp, password_inp)

            if len(email_inp)==0 or len(password_inp)==0:
                return render_template("login.html", message="missing_info")
            elif email_check == email_inp and password_check == password_inp: 
                session['email'] = email_inp
                session['login_status'] = True
                print('login successfully')
                return redirect(url_for('index',products=session['all_products'] ))
            else:
                return render_template("login.html", message="failed_login")
        else: # 'forget' in request.form:
            print('in forget')
            if db.account_check_exist(email_inp):
                session['email_forgot_pwd'] = email_inp
                send_password_recovery_email(email_inp)
                return render_template('forgot_password.html', message="A recovery link was sent to your email. Please use the link to reset your password")
            return render_template("forgot_password.html", message="Cannot find email in the database. Please sign up.")
    else:
        return render_template("login.html", message="")

#VIEW PRODUCT INFO
@app.route("/view_product/<int:id>", methods=["GET",'POST'])
def product_info(id):
    if request.method == 'POST':
        print('IN POST')
        user_rating = int (request.form.getlist('rating')[0])
        user_review = request.form['review_text_field']
        print(user_rating)
        print(user_review)
        db.products_add_user_review(session['email'], id, user_rating, user_review)
    info = db.retrieve_products_by_id(id)
    ratings, reviews = db.get_ratings_reviews_by_id(id)
    ratings = str(math.floor(float(ratings)))
    #ratings and reviews LOOKS LIKE THIS:
    # ratings = 4.5/5
    # reviews = [['john', 'Good cap'], ['kelly', 'Perfect caps for a sunny day']]
    #Ex ['john', 'Good cap'] = #name of reviewer, #review
    has_user = False
    if session['login_status']: #user is logged in
        has_user = True
    return render_template("product_info.html", info = info, ratings=ratings, reviews=reviews, has_user=has_user)

#VIEW CONTACT INFO
@app.route("/contacts", methods=["GET"])
def contacts():
    return render_template("contacts.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=PORT, debug=True)
