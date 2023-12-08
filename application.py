from flask import Flask, render_template , url_for, request, redirect , flash, session, jsonify
from database import DBhandler
import hashlib


app = Flask(__name__)
app.config["SECRET_KEY"]="helloosp"
DB = DBhandler()


@app.route('/')
def index():
    return redirect(url_for('view_list'))



@app.route('/mypage')
def mypage():
    return render_template('mypage.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route("/product-add") 
def productAdd():
    return render_template('product_add.html')

@app.route("/header")
def headerBefore():
    return render_template('layout/header.html')
@app.route("/header-only")
def headerAfter():
    return render_template('layout/header_only.html')
@app.route("/footer")
def footerEnter():
    return render_template('layout/footer.html')



@app.route("/add-product", methods=["POST"])
def add_product():
    image_file = request.files["img_path"]
    image_file.save("static/img/{}".format(image_file.filename))
    data = {
        "product_description": request.form.get("product-description"),
        "product_place": request.form.get("product-place"),
        "product_number": request.form.get("product-number"),
        "product_category": request.form.get("product-category"),
        "start_date": request.form.get("start-date"),
        "end_date": request.form.get("end-date"),
        "img_path": "static/img/" + image_file.filename
    }
    user_id = session.get('id')
    product_description = f"{user_id} 상품 설명 : {data['product_description']}"
    data["product_description"] = product_description

    DB.insert_item(product_description, data, image_file.filename)

    return redirect(url_for('view_list'))

@app.route("/view-list", methods=["GET"])
def view_list():
    page = request.args.get("page", 0, type=int)
    per_page = 6
    per_row = 3
    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    data = DB.get_items()
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    row_data = [list(data.items())[i * per_row:(i + 1) * per_row] for i in range((end_idx - start_idx) // per_row)]

    return render_template("product_list.html", row_data=row_data, limit=per_page, page=page, page_count=int((item_counts / per_page) + 1), total=item_counts)





@app.route("/view_detail/<name>/")
def view_item_detail(name):
        data = DB.get_item_byname(str(name))
        #return render_template("detail.html", name=name, data=data)
        #product_id = f"{data['user_id']}_{name}"
        return render_template("product_detail.html", name=name, data=data)
        #return render_template("product_detail.html", name=name, data=data, product_id=product_id)
    

    
@app.route("/product-detail")
def productDetail():
    return render_template('product_detail.html')

@app.route("/myparticipation", methods=["GET"])  
def my_participate(): 
    product_description = request.args.get('product_description')
    product_number = request.args.get('product_number')
    data = {
        'product_description': product_description,
        'product_number': product_number
    }
    return render_template("myparticipation.html", data=data)  



@app.route("/mygongGu", methods=["GET"])
def my_gonggu():
    user_id = session.get('id')  
    all_items = DB.get_items()  
    user_items = {key: value for key, value in all_items.items() if key.startswith(f"{user_id} ")}


    per_page = 6
    per_row = 3
    page = request.args.get("page", 0, type=int)
    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    item_counts = len(user_items)
    user_items = dict(list(user_items.items())[start_idx:end_idx])
    row_data = [list(user_items.items())[i * per_row:(i + 1) * per_row] for i in range((end_idx - start_idx) // per_row)]

    print(user_items)
    print(all_items)
    return render_template("product_list.html", row_data=row_data, limit=per_page, page=page, page_count=int((item_counts / per_page) + 1), total=item_counts)





@app.route("/parti-product") 
def partiProduct():
    return render_template("parti_product.html")

@app.route("/written-review")
def writtenReview():
    return render_template("written_review.html")

@app.route("/my-review")
def myReview():
    return render_template('my_review.html')


@app.route("/review-add") 
def reviewAdd():
    return render_template('review_add.html')

@app.route("/review-detail")
def reviewDetail():
    return render_template('review_detail.html')

@app.route("/reviews-list")
def reviewList():
    return render_template('all_review_check.html')

@app.route("/signup1")
def signup1():
    return render_template('signup1.html')

@app.route("/signup2", methods=["GET", "POST"])
def signup2():
    if request.method == "POST":
        return redirect(url_for('signup1'))
    return render_template('signup2.html')



@app.route("/signup1_post", methods=['POST'])
def register_user():
    data = request.form
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    
    if DB.insert_user(data, pw_hash):
        return render_template('signup3.html')
    else:
        flash("이미 존재하는 아이디입니다!")
        return redirect(url_for('signup1'))
    
@app.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['password']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return redirect(url_for('index'))
    else:
        flash("존재하지 않는 정보입니다! 다시 로그인을 시도해주세요.")
        return redirect(url_for('login'))

@app.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('index'))

@app.route("/reg_review_init/<name>/")
def reg_review_init(name):
    return render_template("review_add.html", name=name)

@app.route("/reg_review", methods=['POST'])
def reg_review():
    print(request.files)
    image_file = request.files.get("img_path")
    image_file.save("static/img/{}".format(image_file.filename))
    
    # 'reviewStar' 키가 없을 경우 기본값으로 '0' 사용
    rate = request.form.get('reviewStar', '0')

    data = {
        'name': request.form['name'],
        'title': request.form['title'],
        'rate': rate,
        'review': request.form['reviewContents'],
        "img_path": "static/img/" + image_file.filename
    }
    DB.reg_review(data, image_file.filename)
    return redirect(url_for('view_review'))



    # 그룹 과제 2 전체리뷰조회화면 추가
@app.route("/review")
def view_review():
    page = request.args.get("page", 0, type=int)
    per_page=3 # item count to display per page
    per_row=3# item count to display per row
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    data = DB.get_reviews() #read the table
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    row_data = [list(data.items())[i * per_row:(i + 1) * per_row] for i in range(per_page // per_row)]
    return render_template(
        "all_review_check.html",
        row_data=row_data, limit=per_page,page=page, page_count=int((item_counts/per_page)+1),total=item_counts)

# 그룹 과제2 리뷰상세 조회 화면 함수 구현

@app.route("/view_review_detail/<review_name>/")
def view_review_detail(review_name):
    review_data = DB.get_review_byname(review_name)
    if review_data:
        return render_template("review_detail.html", review=review_data)
    else:
        flash("Review not found!")
        return redirect(url_for('view_review'))
    
@app.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    my_heart = DB.get_heart_byname(session['id'], name)
    return jsonify({'my_heart': my_heart})

@app.route('/like/<name>/', methods=['POST'])
def like(name):
    my_heart = DB.update_heart(session['id'],'Y',name)
    return jsonify({'msg': '위시 상품에 등록되었습니다!'})

@app.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    my_heart = DB.update_heart(session['id'],'N',name)
    return jsonify({'msg': '위시 상품에서 제외되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)