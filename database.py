import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

products_db = myclient["products"]


order_management_db = myclient["order_management"]


def get_product(code):
    products_coll = products_db["products"]
    product = products_coll.find_one({"code":code},{"_id":0})
    return product

def get_products():
    product_list = []
    products_coll = products_db["products"]
    for p in products_coll.find({},{"_id":0}):
        product_list.append(p)
    return product_list


#get branches database

def get_branch(code):
    branches_coll = products_db["branches"]
    branch = branches_coll.find_one({"code":code})
    return branch

def get_branches():
    branch_list = []
    branches_coll = products_db["branches"]
    for b in branches_coll.find({}):
        branch_list.append(b)
    return branch_list

def get_user(username):
    customers_coll = order_management_db['customers']
    user=customers_coll.find_one({"username":username})
    return user

#order creation
def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert(order)

#past orders
def get_pastorders():
    pastorder_list = []
    orders_coll = order_management_db["orders"]
    orderdetails_coll=orders_coll["details"]
    for u in orders_coll.find({},{"details":1}):
        for v in u["details"]:
            pastorder_list.append(v)
    return pastorder_list

#get password
def get_user(username):
    customers_coll = order_management_db['customers']
    user=customers_coll.find_one({"username":username})
    return user
def get_password(username):
    return get_user(username)["password"]
def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert(order)
def update_password(username,newpassword):
    customers_coll = order_management_db["customers"]
    updatepassword = customers_coll.update_one({"username":username}, {"$set":{"password":newpassword}})
    return updatepassword
