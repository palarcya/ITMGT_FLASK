from flask import Flask, redirect
from flask import Flask, flash
from flask import render_template
from flask import request
from flask import session
from bson.json_util import loads, dumps
from flask import make_response
import database as db
import authentication
import logging
import ordermanagement as om

app = Flask(__name__)
# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

#app route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

#app route for authentication
@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return render_template('loginfailed.html')
#THIS MAKES IT WORK YEHEY for wrong users and no field input
    try:
        return users[USERNAME]
    except KeyError:
        return render_template('loginfailed.html')

#app route logout
@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')

#app route add to Cart
@app.route('/addtocart') #this function adds 1 item to the cart from an individual product page
def addtocart():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()

    # A click to add a product translates to a
    # quantity of 1 for now
    item["qty"] = 1
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]
    item["code"] = code

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/additem', methods=["POST"]) #this routes to my html code
def additem():
    cart = session["cart"]
    code = request.form.get('code')
    qty = int(request.form.get('qty'))
    unit_price = request.form.get('price')
    product = db.get_product(int(code))

    for item in cart.values():
        if item["code"] == code:
            item["qty"] = qty
            item["subtotal"] = product["price"]*qty
            cart[code]=item
            session["cart"]=cart
    return render_template("cart.html")

@app.route('/removeitem', methods=["POST"])
def removeitem():
    cart = session["cart"]
    code = request.form.get('code')
    del cart[code]
    session["cart"]=cart
    return render_template("cart.html")

#app route for Cart
@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route('/checkout')
def checkout():
    # clear cart in session memory upon checkout
    om.create_order_from_cart()
    session.pop("cart",None)
    return redirect('/ordercomplete')

@app.route('/ordercomplete')
def ordercomplete():
    return render_template('ordercomplete.html')

@app.route("/pastorders",methods=["GET"])
def pastorders():
    pastorder_list = db.get_pastorders()
    return render_template("pastorders.html", page="Past Orders",pastorder_list=pastorder_list)

@app.route('/')
def index():
    return render_template('index.html', page="Index")

@app.route('/products')
def products():
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    return render_template('productdetails.html', code=code, product=product)

@app.route('/branches')
def branches():
    branch_list = db.get_branches()
    return render_template('branches.html', page="Branches", branch_list=branch_list)

@app.route('/branchdetails')
def branchdetails():
    code = request.args.get('code', '')
    branch = db.get_branch(int(code))
    return render_template('branchdetails.html', code=code, branch=branch)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")

@app.route("/changepassword",methods=["GET","POST"])
def changepassword():
    username = session["user"]["username"]
    password = db.get_password(username)
    currentpassword = request.form.get("currentpassword")
    newpassword = request.form.get("newpassword")
    updatepassword = None
    error = None

    if currentpassword == None:
        print(currentpassword)
        error=None
    elif currentpassword == password:
        print(currentpassword)
        updatepassword=db.update_password(username,newpassword)
    elif currentpassword != password:
        print(currentpassword)
        error="Current Password Does Not Match."

    return render_template('changepassword.html', page="Change Password",updatepassword=updatepassword,error=error)

@app.route('/api/products',methods=['GET'])
def api_get_products():
    resp = make_response( dumps(db.get_products()) )
    resp.mimetype = 'application/json'
    return resp

@app.route('/api/products/<int:code>',methods=['GET'])
def api_get_product(code):
    resp = make_response(dumps(db.get_product(code)))
    resp.mimetype = 'application/json'
    return resp
