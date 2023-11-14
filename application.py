from flask import Flask, render_template , request
from database import DBhandler
import sys
app = Flask(__name__)
DB = DBhandler()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')
@app.route('/login')
def login():
    return render_template('login.html')





@app.route("/product-add") 
def productAdd():
    return render_template('product_add.html')


@app.route("/add-product-post", methods=["POST"])
def registerproduct():
    data = {
        "product_description": request.form.get("product-description"),
        "product_place": request.form.get("product-place"),
        "product_number": request.form.get("product-number"),
        "product_category": request.form.get("product-category"),
        "start_date": request.form.get("start-date"),
        "end_date": request.form.get("end-date")
    }
    DB.insert_item(data['product_category'], data)
    return render_template("products_list.html", data=data)





@app.route("/product-detail")
def productDetail():
    return render_template('product_detail.html')

@app.route("/products-list")
def productsList():
    return render_template('products_list.html')

@app.route("/review-add") 
def reviewAdd():
    return render_template('review_add.html')

@app.route("/review-detail")
def reviewDetail():
    return render_template('review_detail.html')

@app.route("/reviews-list")
def reviewList():
    return render_template('reviews_list.html')



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)