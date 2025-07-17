from app import db, app, Question, User, Record

with app.app_context():
    # 1. 刪除資料表（不影響其他表）
    Record.__table__.drop(db.engine)

    # 2. 重建資料表（使用目前修改後的欄位定義）
    Record.__table__.create(db.engine)

    print("資料表已重建")
