from app import db, app, User

with app.app_context():
    new_user = User(username="yumik", password="3310")
    new_user = User(username="Amy", password="1111")
    new_user = User(username="Mike", password="1314")
    new_user = User(username="Vivi", password="7879")
    db.session.add(new_user)
    print("帳密新增完成")
    db.session.commit()

#id=1, username="yumik", pwd="3310"
#id=2, username="Amy", password="1111"
#id=3, username="Mike", password="1314"
#id=4, username="Vivi", password="7879"