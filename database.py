from MySQLdb import connect, Error

# подключаемся к бд
try:
    with connect(
        host='localhost',
        user='kravchen14',
        password='80LsDF3C',
        database='kravchen14',
    ) as connection:
        create_db = "CREATE DATABASE users"
        with connection.cursor() as cursor:
            cursor.execute(create)
except Error as e:
    print("Ошибка", e)

# создаем таблицы
create_it_table = """
CREATE TABLE it(
    id INT PRIMARY KEY,
    name VARCHAR(100),
    field VARCHAR(100)
)
"""

create_nko_table = """
CREATE TABLE nko(
    id INT PRIMARY KEY,
    title VARCHAR(100)
)
"""

create_moderator_table = """
CREATE TABLE it(
    id INT PRIMARY KEY,
    key VARCHAR(100)
)
"""
with connection.cursor() as cursor:
    cursor.execute(create_it_table)
    cursor.execute(create_nko_table)
    cursor.execute(create_moderator_table)
    connection.commit()

insert_it_query = """
INSERT INTO it
(id, name, field)
VALUES ( %s, %s, %s)
"""
insert_nko_query = """
INSERT INTO nko
(id, title)
VALUES ( %s, %s)
"""
insert_moderator_query = """
INSERT INTO nko
(id, key)
VALUES ( %s, %s)
"""