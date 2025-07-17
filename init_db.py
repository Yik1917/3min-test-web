from app import db, app, Record  # 匯入 Flask app 與資料表

# 啟用應用程式的 context
with app.app_context():
    db.create_all()
    print("資料庫初始化完成")
