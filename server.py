
import json
from math import prod


from flask import Flask, Response, abort, request
from aboutme import me
from mock_data import catalog  # import data
from config import db
from bson import ObjectId, objectid
from flask_cors import CORS


app = Flask('organika')
CORS(app)


@app.route("/", methods=['GET'])
def home():
    return "This is home page!!"


# Creat an about endpoint to return your name


@app.route("/about", methods=['GET'])
def about():
    return me["first"] + " " + me["last"]


@app.route("/myaddress")
def address():
    return f'{me["address"]["number"]}{me["address"]["street"]}'


#####################################################
#################### API End Point ##################
#####################################################

@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    result = []
    cursor = db.products.find({})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        result.append(prod)
    return json.dumps(result)


@app.route("/api/catalog", methods=["POST"])
def saveProduct():

    try:
        product = request.get_json()
        error = ""
        # title, 5 chars long
        if not "title" in product or len(product["title"]) < 5:
            error += "title should have at least 5 chars"

        # must have an image
        if not "image" in product:
            error += "must have an image"
        if not "price" in product or product["price"] < 1:
            error += "price should be greater than 0"
        if error:
            return abort(400, error)
        # must have a price, price should be greater than 0
        db.products.insert_one(product)
        product["_id"] = str(product["_id"])
        print(product)
        return json.dumps(product)
    except:
        return abort(500, "unexpect error")


@app.route("/api/catalog/count", methods=["GET"])
def get_count():
    # Here... Count how many products are in list catalog
    cursor = db.products.find({})
    num_items = 0
    for prod in cursor:
        num_items += 1
    # counts = len(catalog)
    return json.dumps(num_items)  # return the value


@app.route("/api/product/<id>", methods=["GET"])
def get_product(id):
    try:
        if not ObjectId.is_valid(id):
            return abort(400, " Invalid id")

        product = db.products.find_one({"_id": ObjectId(id)})
        if not product:
            return abort(400, "product not found")
        product["_id"] = str(product["_id"])
        return json.dumps(product)
    except:
        return("Can't find ID")
    # return json.dumps(id)
    # return abort(404, " ID does not match any product")


# @app.route("/api/catalog/total", methods=["GET"])

@app.get("/api/catalog/total")
def get_total():
    # Here... Count how many products are in list catalog
    total = 0
    cursor = db.products.find({})
    for prod in cursor:
        total = total + prod["price"]
    return json.dumps(total)  # return the value


@app.get("/api/products/<category>")
def get_by_cate(category):
    list = []
    cursor = db.products.find({"category": category})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        list.append(list)
    return json.dumps(prod)
    # return abort(404, "there no product")  # return the value

# get the list of category

# POST method to create new products


@app.get("/api/categories")
def get_listcategory():
    list = []
    cursor = db.products.find({})
    for pro in cursor:
        if pro["category"] not in list:
            list.append(pro["category"])
    return json.dumps(list)

# get the cheapest product


@app.get("/api/product/cheapest")
def get_cheapestProduct():
    # low = 20
    cursor = db.products.find({})
    result = cursor[0]
    for prod in cursor:
        if prod["price"] < result["price"]:
            result = prod
    result["_id"] = str(result["_id"])
    return json.dumps(result)


@app.get("/api/exercise1")
def get_exe1():
    nums = [123, 123, 654, 124, 8865, 532, 4768, 8476, 45762,
            345, -1, 234, 0, -12, -456, -123, -865, 532, 4768]
    solution = {}

    # print the lowest number
    solution["a"] = min(nums)

    # count and print how many numbers are lowe than 500
    count = 0
    listLower500 = []
    for result in nums:
        if result < 500:
            listLower500.append(result)
            count += 1
    solution["b"] = count, listLower500

    # sum and print all the negatives
    total = 0
    list_negative = []
    for result in nums:
        if result < 0:
            list_negative.append(result)
            total += result
    solution["c"] = total, list_negative

    # return the sum of numbers except negatives
    total2 = 0
    list_positive = []
    for result in nums:
        if result > 0:
            list_positive.append(result)
            total2 += result
    solution["d"] = total2, list_positive
    return json.dumps(solution)

# get all


@app.route("/api/coupon", methods=["GET"])
def get_bcoupon():
    result = []
    cursor = db.coupons.find({})
    for cp in cursor:
        cp["_id"] = str(cp["_id"])
        cp["test"] = 1
        result.append(cp)
    return json.dumps(result)
# get save coupon code


@app.route("/api/coupon", methods=["POST"])
def save_Coupon():
    try:
        coupon = request.get_json()
        if not "code" in coupon or len(coupon["code"]) < 5:
            return abort(400, "Coupon should have coupon and longer than 5 character")
        if not "discount" in coupon or coupon["discount"] < 1:
            return abort(400, "Coupon should have Disocunt")
         # querry the database check duplicate coupon
        exist = db.coupons.find_one({"code": coupon["code"]})
        if exist:
            return Response("same coupon code", status=400)
        db.coupons.insert_one(coupon)
        coupon["_id"] = str(coupon["_id"])
        return json.dumps(coupon)

    except Exception as e:
        print(e)
        return Response("unexpect error", status=500)

# get cc by code


@app.route("/api/coupon/<code>", methods=["GET"])
def get_coupon(code):
    list = []
    if len(code) < 4:
        return abort(400, "the code should have 5 character")
    coupon = db.coupons.find_one({"code": code})
    if not coupon:
        return abort(404, "Coupon not found")
    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)


app.run(debug=True)
