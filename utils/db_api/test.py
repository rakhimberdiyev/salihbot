from sqlite3 import DatabaseError
from sqlite import Database


def test():
    db = Database(path_to_db='test.db')
    db.create_table_users()
    try:
        db.add_user(43453253)
    except DatabaseError as e:
        print(e)
    # db.add_user(2, "olim", "olim@gmail.com", 'uz')
    # db.add_user(3, 1, 1)
    # db.add_user(4, 1, 1)
    # db.add_user(5, "John", "john@mail.com")

    try:
        users = db.select_all_users()
        for i in users:
            print(i[0])
    except Exception as e:
        print(e)
    print(f"Barcha fodyalanuvchilar: {users}")

    user = db.select_user(user_id=43453253, id=1)
    print(f"Bitta foydalanuvchini ko'rish: {user}")



test()