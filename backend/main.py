from backend import app
from backend.api import detail, search


@app.route("/search")
def find():
    return search.find()


# @app.route("/get-list-manufacturer")
# def get_list_manufacturer():
#     return search.get_list_manufacturer()


# @app.route("/detail/<string:id_product>")
# def detail_product(id_product):
#     return detail.detail_product(id_product)


# @app.route("/get-same-range-price/<int:price>")
# def same_price(price):
#     return detail.get_list_same_price(price)


# @app.route("/get-same-range-manufacturer/<string:manufacturer>")
# def same_manufacturer(manufacturer):
#     return detail.get_list_same_manufacturer(manufacturer)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5420)
