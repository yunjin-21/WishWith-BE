import pyrebase
import json

class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)
            firebase = pyrebase.initialize_app(config)
            self.db = firebase.database()

    def insert_item(self, name, data):
        item_info = {
            "product_description": data['product_description'],
            "product_place": data['product_place'],
            "product_number": data['product_number'],
            "product_category": data['product_category'],
            "start_date": data['start_date'],
            "end_date": data['end_date'],
        }
        self.db.child("item").child(name).set(item_info)
        print(data)
        return True
    
    def insert_user(self, data, password1):
        user_info = {
            "name": data['name'],
            "email": data['email'],
            "phone": data['phone'],
            "id": data['id'],
            "password": password1,
        }
        if self.user_duplicate_check(str(data['email'])) and password1!=data['password2']:
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False

    def user_duplicate_check(self, email_string):
        users = self.db.child("user").get()
        print("users###",users.val())
        if str(users.val()) == "None":
            return True
        else:
            for res in users.each():
                value = res.val()
                if value['email'] == email_string:
                    return False
                return True
            
    def insert_user2(self, data):
        user_info = {
            "nickname": data['nickname'],
            "profile-img": data['profile-img']
        }
        self.db.child("user").push(user_info)
        return True