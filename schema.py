import sqlite3

connection = sqlite3.connect('ebook.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(email VARCHAR(50) PRIMARY KEY,password VARCHAR(50),subscription VARCHAR(50),subscription_start_date VARCHAR(100),subscription_end_date VARCHAR(100))""")
# cursor.execute(
#     """
#   DROP TABLE users;"""


# )


cursor.execute(
    """
  CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name VARCHAR(50),
    product_price VARCHAR(50),
    availability INTEGER
  )"""


)

cursor.execute(
    """
  CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT,
    product_name TEXT,
    product_link TEXT,
    product_image_url TEXT,
    product_price VARCHAR(100),
    email VARCHAR(50)
  );"""
)

cursor.execute(
    """
  CREATE TABLE IF NOT EXISTS history (
    
    product_id TEXT,
    product_name TEXT,
    product_link TEXT,
    product_image_url TEXT,
    downloadLink TEXT,
    email VARCHAR(50)
  );"""
)

# cursor.execute(
#     """
#   DROP TABLE history;"""


# )

# cursor.execute(
#     """
#   DROP TABLE products;"""


# )
# cursor.execute(
#     """
#   DROP TABLE cart;"""


# )


# cursor.execute("""INSERT INTO products(product_name,product_price,availability) VALUES("50 Inch TV","300",10)""")

# cursor.execute(
#     """
#     INSERT INTO products(product_name,product_price,availability) VALUES("MP3 player","15",10);"""
# )

# cursor.execute(
#     """
#     INSERT INTO products(product_name,product_price,availability) VALUES("Headphones","8",10);"""
# )

# cursor.execute(
#     """
#     INSERT INTO products(product_name,product_price,availability) VALUES("Earphones","5",10);"""
# )

# cursor.execute(
#     """
#     INSERT INTO products(product_name,product_price,availability) VALUES("Laptop","500",10);"""
# )

# cursor.execute(
#     """
#     INSERT INTO products(product_name,product_price,availability) VALUES("Computer","700",10);"""
# )

# cursor.execute(
#     """
#     INSERT INTO products(product_name,product_price,availability) VALUES("Phone","400",10);"""
# )

# cursor.execute(
#     """
#     INSERT INTO products(product_name,product_price,availability) VALUES("Games Console","10",10);"""
# )

# cursor.execute(
#     """
#     INSERT INTO products(product_name,product_price,availability) VALUES("Radio","20",10);"""
# )

# cursor.execute(
#     """
#     INSERT INTO products(product_name,product_price,availability) VALUES("Speaker","450",10);"""
# )

# cursor.execute(
#     """
#     INSERT INTO products(product_name,product_price,availability) VALUES("Projector","50",10);"""
# )

# cursor.execute(
#     """
#     INSERT INTO products(product_name,product_price,availability) VALUES("Camera","5000",10);"""
# )
connection.commit()
